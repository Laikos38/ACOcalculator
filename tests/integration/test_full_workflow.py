"""
Tests de integración para el flujo completo del sistema.
"""
import pytest
import os
import csv
from src.utils.config_loader import ConfigLoader
from src.managers.tp_manager import TPManager
from src.managers.parcial_manager import ParcialManager
from src.generators.report_generator import ReportGenerator
from tests.factories import CSVFileFactory, MoodleGradeFactory


@pytest.mark.integration
class TestFullWorkflow:
    """Tests del flujo completo: desde CSVs hasta planilla final."""
    
    @pytest.fixture
    def setup_full_environment(self, test_config_path, test_dirs):
        """Configura un entorno completo para tests de integración."""
        os.chdir(test_dirs['root'])
        config = ConfigLoader(test_config_path)
        
        # Crear managers
        tp_manager = TPManager(config)
        exam_manager = ParcialManager(config)
        report_generator = ReportGenerator(config)
        
        # Crear archivos CSV de prueba
        input_dir = test_dirs['input']
        
        # TPs
        for tp_num in range(1, 3):  # TP1 y TP2
            tp_file = os.path.join(input_dir, f"TP{tp_num}_1K2.csv")
            CSVFileFactory.create_tp_file(tp_file, "1K2", tp_num, num_students=10)
        
        # Parciales
        for parcial_num in range(1, 3):  # Parcial1 y Parcial2
            parcial_file = os.path.join(input_dir, f"Parcial{parcial_num}_1K2.csv")
            CSVFileFactory.create_parcial_file(parcial_file, "1K2", parcial_num, num_students=10)
        
        return {
            'config': config,
            'tp_manager': tp_manager,
            'exam_manager': exam_manager,
            'report_generator': report_generator,
            'dirs': test_dirs
        }
    
    def test_flujo_completo_tps_a_reporte(self, setup_full_environment):
        """
        Test del flujo completo:
        1. Merge de TPs
        2. Merge de Parciales
        3. Generación de reporte final
        """
        env = setup_full_environment
        
        # Paso 1: Mergear TPs
        env['tp_manager'].merge_tps("1K2")
        
        # Verificar archivo de TPs unificado (ahora en subcarpeta 'tps')
        tps_file = os.path.join(env['dirs']['output'], "1K2", "tps", "TPs_1K2_unificado.csv")
        assert os.path.exists(tps_file)
        
        # Paso 2: Unificar Parciales
        env['exam_manager'].merge_exams("1K2")
        
        # Verificar archivo de Parciales unificado (ahora en subcarpeta 'parciales')
        parciales_file = os.path.join(env['dirs']['output'], "1K2", "parciales", "Parciales_1K2_unificado.csv")
        assert os.path.exists(parciales_file)
        
        # Paso 3: Generar reporte final (sin interacción del usuario)
        # Nota: ReportGenerator requiere xlwt que ya está instalado
        env['report_generator'].generate_final_report("1K2", env['tp_manager'], env['exam_manager'])
        
        # Verificar archivo final
        final_file = os.path.join(env['dirs']['output'], "1K2", "Planilla_Final_1K2.xls")
        assert os.path.exists(final_file)
    
    def test_multiples_intentos_se_procesan_correctamente(self, setup_full_environment):
        """Debe procesar correctamente estudiantes con múltiples intentos."""
        env = setup_full_environment
        input_dir = env['dirs']['input']
        
        # Crear archivo con múltiples intentos para un estudiante
        tp_file = os.path.join(input_dir, "TP3_1K2.csv")
        CSVFileFactory.create_moodle_csv_with_attempts(
            tp_file,
            {"10001": 4, "10002": 2}  # 4 y 2 intentos respectivamente
        )
        
        # Mergear TPs
        env['tp_manager'].merge_tps("1K2")
        
        # Leer resultado (ubicación actualizada a subcarpeta 'tps')
        tps_file = os.path.join(env['dirs']['output'], "1K2", "tps", "TPs_1K2_unificado.csv")
        with open(tps_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = {row["Número de ID"]: row for row in reader}
        
        # Verificar que los intentos se cuentan correctamente
        assert "10001" in rows
        assert rows["10001"]["TP3_Intentos"] == "4"
        
        assert "10002" in rows
        assert rows["10002"]["TP3_Intentos"] == "2"


@pytest.mark.integration
@pytest.mark.slow
class TestPerformance:
    """Tests de rendimiento del sistema."""
    
    def test_procesa_muchos_estudiantes(self, test_config_path, test_dirs):
        """Debe procesar eficientemente archivos con muchos estudiantes."""
        os.chdir(test_dirs['root'])
        config = ConfigLoader(test_config_path)
        tp_manager = TPManager(config)
        
        # Crear archivo grande (100 estudiantes)
        input_dir = test_dirs['input']
        tp_file = os.path.join(input_dir, "TP1_1K2.csv")
        CSVFileFactory.create_tp_file(tp_file, "1K2", 1, num_students=100)
        
        # Mergear - no debe tardar mucho
        import time
        start = time.time()
        tp_manager.merge_tps("1K2")
        duration = time.time() - start
        
        # Debe completarse en menos de 5 segundos
        assert duration < 5.0
        
        # Verificar que se procesaron todos (ubicación 'tps')
        output_file = os.path.join(test_dirs['output'], "1K2", "tps", "TPs_1K2_unificado.csv")
        with open(output_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 100

