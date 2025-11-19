"""
Tests unitarios para TPManager.
"""
import pytest
import os
import csv
from src.managers.tp_manager import TPManager
from src.utils.config_loader import ConfigLoader
from tests.factories import CSVFileFactory


@pytest.mark.unit
class TestTPManager:
    """Tests para la clase TPManager."""
    
    @pytest.fixture
    def tp_manager(self, test_config_path, test_dirs):
        """Crea una instancia de TPManager para tests."""
        # Actualizar config con directorios de test
        os.chdir(test_dirs['root'])
        config = ConfigLoader(test_config_path)
        return TPManager(config)
    
    def test_inicializacion(self, tp_manager):
        """Debe inicializarse correctamente."""
        assert tp_manager.tp_count == 4
        assert tp_manager.tp_prefix == "TP"
        assert tp_manager.source_dir == "test_inputs"
        assert tp_manager.output_dir == "test_outputs"
    
    def test_merge_tps_crea_archivo(self, tp_manager, test_dirs):
        """Debe crear archivo unificado de TPs."""
        # Crear archivos de TP de prueba
        input_dir = test_dirs['input']
        
        # Crear TP1 y TP2 con datos
        tp1_file = os.path.join(input_dir, "TP1_1K2.csv")
        tp2_file = os.path.join(input_dir, "TP2_1K2.csv")
        
        CSVFileFactory.create_tp_file(tp1_file, "1K2", 1, num_students=5)
        CSVFileFactory.create_tp_file(tp2_file, "1K2", 2, num_students=5)
        
        # Ejecutar merge
        tp_manager.merge_tps("1K2")
        
        # Verificar que se creó el archivo unificado
        output_file = os.path.join(test_dirs['output'], "1K2", "TPs_1K2_unificado.csv")
        assert os.path.exists(output_file)
        
        # Verificar contenido
        with open(output_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
        assert len(rows) > 0
        # Verificar que tiene columnas de intentos
        assert "TP1_Intentos" in rows[0]
        assert "TP2_Intentos" in rows[0]


@pytest.mark.unit
class TestTPManagerAttempts:
    """Tests específicos para el conteo de intentos."""
    
    @pytest.fixture
    def tp_manager(self, test_config_path, test_dirs):
        """Crea una instancia de TPManager para tests."""
        os.chdir(test_dirs['root'])
        config = ConfigLoader(test_config_path)
        return TPManager(config)
    
    def test_cuenta_intentos_multiples(self, tp_manager, test_dirs):
        """Debe contar correctamente múltiples intentos."""
        input_dir = test_dirs['input']
        
        # Crear archivo con múltiples intentos
        tp_file = os.path.join(input_dir, "TP1_1K2.csv")
        
        # Estudiante con 3 intentos
        CSVFileFactory.create_moodle_csv_with_attempts(
            tp_file,
            {"10001": 3, "10002": 2, "10003": 1}
        )
        
        # Ejecutar merge
        tp_manager.merge_tps("1K2")
        
        # Leer resultado
        output_file = os.path.join(test_dirs['output'], "1K2", "TPs_1K2_unificado.csv")
        
        with open(output_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Verificar intentos
        student_attempts = {row["Número de ID"]: row["TP1_Intentos"] for row in rows}
        
        assert student_attempts.get("10001") == "3"
        assert student_attempts.get("10002") == "2"
        assert student_attempts.get("10003") == "1"

