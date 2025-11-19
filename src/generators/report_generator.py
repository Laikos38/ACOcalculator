"""
Módulo para generar planillas finales consolidadas.
"""
import os
import csv
from typing import Dict, Set
from ..utils import ConfigLoader


class ReportGenerator:
    """Clase para generar planillas finales consolidadas en formato XLS."""
    
    def __init__(self, config: ConfigLoader):
        """
        Inicializa el generador de reportes.
        
        Args:
            config: Instancia de ConfigLoader con la configuración del sistema
        """
        self.config = config
        self.output_dir = config.get_output_dir()
        self.encoding = config.get_csv_encoding()
        self.output_format = config.get_output_format()
        self.tp_count = config.get_cantidad_tps()
        self.exam_count = config.get_cantidad_parciales()
        self.makeup_count = config.get_cantidad_recuperatorios()
        self.tp_prefix = config.get_tp_prefix()
        self.exam_prefix = config.get_parcial_prefix()
        self.makeup_prefix = config.get_recuperatorio_prefix()
    
    def generate_final_report(self, course: str, tp_manager=None, exam_manager=None):
        """
        Genera una planilla final consolidada combinando TPs y Parciales en formato XLS.
        Incluye tanto las notas decimales de Moodle como las notas convertidas a enteros.
        
        Args:
            course: Código del curso (ej: "1K2", "1K4")
            tp_manager: Instancia de TPManager (para generar merges si es necesario)
            exam_manager: Instancia de ParcialManager (para generar merges si es necesario)
        """
        try:
            import xlwt
        except ImportError:
            print("❌ Error: Se requiere la librería 'xlwt' para generar archivos XLS.")
            print("   Instálala con: pip install xlwt")
            return
        
        # Directorio de salida específico del curso (normalizar a mayúsculas)
        course = course.upper()
        output_course_dir = os.path.join(self.output_dir, course)
        
        # Archivos mergeados de TPs y Parciales
        tps_file = os.path.join(output_course_dir, f"{self.tp_prefix}s_{course}_unificado.csv")
        exams_file = os.path.join(output_course_dir, f"{self.exam_prefix}es_{course}_unificado.csv")
        
        # Variables para controlar qué datos están disponibles
        tps_data = {}
        exams_data = {}
        has_tps = False
        has_exams = False
        
        # Intentar obtener datos de TPs
        if not os.path.exists(tps_file):
            print(f"⚠️ No se encontró el archivo de TPs unificado: {tps_file}")
            if tp_manager:
                generate = input("¿Quieres unificar los TPs ahora? (S/n) [S]: ").strip().lower()
                if generate == '' or generate == 's':
                    tp_manager.merge_tps(course)
                    if os.path.exists(tps_file):
                        tps_data = self._read_csv_as_dict(tps_file)
                        has_tps = True
                    else:
                        print("⚠️ No hay datos de TPs disponibles. Continuando sin TPs...")
                else:
                    print("⚠️ Continuando sin datos de TPs...")
            else:
                print("⚠️ Continuando sin datos de TPs...")
        else:
            tps_data = self._read_csv_as_dict(tps_file)
            has_tps = True
        
        # Intentar obtener datos de Parciales
        if not os.path.exists(exams_file):
            print(f"⚠️ No se encontró el archivo de Parciales unificado: {exams_file}")
            if exam_manager:
                generate = input("¿Quieres unificar los Parciales ahora? (S/n) [S]: ").strip().lower()
                if generate == '' or generate == 's':
                    exam_manager.merge_exams(course)
                    if os.path.exists(exams_file):
                        exams_data = self._read_csv_as_dict(exams_file)
                        has_exams = True
                    else:
                        print("⚠️ No hay datos de Parciales disponibles. Continuando sin Parciales...")
                else:
                    print("⚠️ Continuando sin datos de Parciales...")
            else:
                print("⚠️ Continuando sin datos de Parciales...")
        else:
            exams_data = self._read_csv_as_dict(exams_file)
            has_exams = True
        
        # Combinar todos los IDs únicos
        all_ids = set(tps_data.keys()) | set(exams_data.keys())
        
        if not all_ids:
            print("⚠️ No hay datos de alumnos para generar la planilla final.")
            print("   Asegúrate de tener al menos un archivo de TP o Parcial con datos.")
            return
        
        # Informar al usuario sobre qué datos se incluirán
        print("")
        print(f"📊 Generando planilla final con:")
        if has_tps:
            print(f"   ✅ {len(tps_data)} alumnos con datos de TPs")
        else:
            print(f"   ⚠️  Sin datos de TPs (columnas estarán vacías)")
        if has_exams:
            print(f"   ✅ {len(exams_data)} alumnos con datos de Parciales")
        else:
            print(f"   ⚠️  Sin datos de Parciales (columnas estarán vacías)")
        print("")
        
        # Crear libro de Excel
        wb = xlwt.Workbook()
        ws = wb.add_sheet(f'Notas {course}')
        
        # Estilo para el encabezado
        header_style = xlwt.easyxf('font: bold on; align: horiz center')
        
        # Definir columnas dinámicamente
        columns = ["Apellido(s)", "Nombre", "Número de ID"]
        
        # Agregar columnas de TPs (con intentos)
        for i in range(1, self.tp_count + 1):
            columns.extend([
                f"{self.tp_prefix}{i}",
                f"{self.tp_prefix}{i}_Nota",
                f"{self.tp_prefix}{i}_Intentos"
            ])
        
        # Agregar columnas de Parciales
        for i in range(1, self.exam_count + 1):
            columns.extend([
                f"{self.exam_prefix}{i}",
                f"{self.exam_prefix}{i}_Nota"
            ])
        
        # Agregar columnas de Recuperatorios
        for i in range(1, self.makeup_count + 1):
            columns.extend([
                f"{self.makeup_prefix}{i}",
                f"{self.makeup_prefix}{i}_Nota"
            ])
        
        # Escribir encabezados
        for col, column in enumerate(columns):
            ws.write(0, col, column, header_style)
        
        # Escribir datos
        row = 1
        for student_id in sorted(all_ids):
            # Obtener datos de TPs (si existen)
            tp_data = tps_data.get(student_id, {})
            # Obtener datos de Parciales (si existen)
            exam_data = exams_data.get(student_id, {})
            
            # Obtener información básica (priorizar TPs, luego Parciales)
            last_name = tp_data.get("Apellido(s)", exam_data.get("Apellido(s)", ""))
            first_name = tp_data.get("Nombre", exam_data.get("Nombre", ""))
            
            # Escribir fila
            col_idx = 0
            ws.write(row, col_idx, last_name)
            col_idx += 1
            ws.write(row, col_idx, first_name)
            col_idx += 1
            ws.write(row, col_idx, student_id)
            col_idx += 1
            
            # TPs (con intentos)
            for i in range(1, self.tp_count + 1):
                ws.write(row, col_idx, tp_data.get(f"{self.tp_prefix}{i}", ""))
                col_idx += 1
                ws.write(row, col_idx, tp_data.get(f"{self.tp_prefix}{i}_Nota", ""))
                col_idx += 1
                ws.write(row, col_idx, tp_data.get(f"{self.tp_prefix}{i}_Intentos", ""))
                col_idx += 1
            
            # Parciales
            for i in range(1, self.exam_count + 1):
                ws.write(row, col_idx, exam_data.get(f"{self.exam_prefix}{i}", ""))
                col_idx += 1
                ws.write(row, col_idx, exam_data.get(f"{self.exam_prefix}{i}_Nota", ""))
                col_idx += 1
            
            # Recuperatorios
            for i in range(1, self.makeup_count + 1):
                ws.write(row, col_idx, exam_data.get(f"{self.makeup_prefix}{i}", ""))
                col_idx += 1
                ws.write(row, col_idx, exam_data.get(f"{self.makeup_prefix}{i}_Nota", ""))
                col_idx += 1
            
            row += 1
        
        # Guardar archivo
        os.makedirs(output_course_dir, exist_ok=True)
        output_file = os.path.join(output_course_dir, f"Planilla_Final_{course}.{self.output_format}")
        wb.save(output_file)
        
        print(f"✅ Planilla final generada: {output_file}")
        print(f"   Total de alumnos: {len(all_ids)}")
        print(f"   Columnas de TPs: {'Incluidas' if has_tps else 'Vacías'}")
        print(f"   Columnas de Parciales: {'Incluidas' if has_exams else 'Vacías'}")
    
    def _read_csv_as_dict(self, file_path: str) -> Dict[str, Dict]:
        """
        Lee un archivo CSV y retorna un diccionario indexado por ID de alumno.
        
        Args:
            file_path: Ruta al archivo CSV
            
        Returns:
            Diccionario con ID de alumno como clave y datos como valor
        """
        data = {}
        with open(file_path, newline='', encoding=self.encoding) as f:
            reader = csv.DictReader(f)
            for row in reader:
                student_id = row["Número de ID"]
                data[student_id] = row
        return data
