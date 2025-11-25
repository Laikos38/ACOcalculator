"""
Módulo para consolidar múltiples archivos de un mismo TP o Parcial.
"""
import glob
import os
import csv
from typing import Dict, List
from .csv_helpers import get_col_name, save_csv, read_csv_with_best_grades, detect_grade_scale, normalize_grade_to_scale_10, is_average_row


def find_files_case_insensitive(directory: str, base_pattern: str) -> List[str]:
    """
    Busca archivos en un directorio usando un patrón case-insensitive.
    
    Por ejemplo, si base_pattern es "TP1_1K15", encontrará:
    - TP1_1K15.csv
    - tp1_1k15.csv
    - Tp1_1K15_1.csv
    - etc.
    
    Args:
        directory: Directorio donde buscar
        base_pattern: Patrón base (ej: "TP1_1K15", "Parcial2_1K2")
        
    Returns:
        Lista de rutas completas a archivos que coinciden
    """
    if not os.path.exists(directory):
        return []
    
    # Obtener todos los archivos CSV del directorio
    all_files = [f for f in os.listdir(directory) if f.lower().endswith('.csv')]
    
    # Normalizar el patrón base a minúsculas para comparación
    base_pattern_lower = base_pattern.lower()
    
    matched_files = []
    
    for filename in all_files:
        filename_lower = filename[:-4].lower()  # Remover .csv y convertir a minúsculas
        
        # Verificar si el nombre del archivo coincide con el patrón base
        # Puede ser exacto o con sufijo numérico (_1, _2, etc.)
        if filename_lower == base_pattern_lower:
            # Coincidencia exacta (ej: TP1_1K15.csv)
            matched_files.append(os.path.join(directory, filename))
        elif filename_lower.startswith(base_pattern_lower + "_"):
            # Coincidencia con sufijo (ej: TP1_1K15_1.csv, TP1_1K15_2.csv)
            # Verificar que lo que sigue sea un número
            suffix = filename_lower[len(base_pattern_lower) + 1:]
            if suffix.isdigit():
                matched_files.append(os.path.join(directory, filename))
    
    return matched_files


class FileConsolidator:
    """Clase para consolidar múltiples archivos CSV de un mismo TP o Parcial."""
    
    def __init__(self, source_dir: str, output_dir: str, header_map: Dict, encoding: str = 'utf-8-sig', calculate_avg_grades: bool = False):
        """
        Inicializa el consolidador de archivos.
        
        Args:
            source_dir: Directorio de archivos de entrada
            output_dir: Directorio de archivos de salida
            header_map: Mapeo de nombres de columnas
            encoding: Encoding de archivos CSV
            calculate_avg_grades: Si False, filtra la fila "Promedio general" de Moodle
        """
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.header_map = header_map
        self.encoding = encoding
        self.calculate_avg_grades = calculate_avg_grades
    
    def consolidate_multiple_files(self, base_name: str, course: str) -> bool:
        """
        Busca y consolida múltiples archivos de un mismo TP o Parcial.
        Soporta búsqueda case-insensitive tanto para prefijos (TP, Parcial, etc.) como para el curso.
        
        Por ejemplo, encontrará:
        - Parcial1_1K2.csv, parcial1_1k2.csv, PARCIAL1_1K2.csv
        - TP1_1K15.csv, tp1_1k15.csv, Tp1_1K15.csv
        
        Args:
            base_name: Nombre base sin extensión (ej: "Parcial1_1K2", "TP1_1K4")
            course: Código del curso (ej: "1K2", "1K4")
            
        Returns:
            bool: True si se encontraron y consolidaron archivos, False si no
        """
        # Buscar archivos usando búsqueda case-insensitive
        found_files = find_files_case_insensitive(self.source_dir, base_name)
        
        if not found_files:
            return False
        
        # Extraer el curso del base_name y crear el directorio de salida (case-insensitive)
        parts = base_name.split("_")
        if len(parts) >= 2:
            course_dir = parts[-1].upper()  # Último elemento es el curso, normalizar a mayúsculas
            output_course_dir = os.path.join(self.output_dir, course_dir)
        else:
            output_course_dir = self.output_dir
        
        # Crear el directorio de salida al inicio
        os.makedirs(output_course_dir, exist_ok=True)
        output_file = os.path.join(output_course_dir, base_name + "_filtrado.csv")
        
        # Si solo hay un archivo, procesarlo normalmente
        if len(found_files) == 1:
            file = found_files[0]
            self._filter_best_grade(file, output_file)
            print(f"✅ Procesado: {os.path.basename(file)}")
            return True
        
        # Si hay múltiples archivos, consolidarlos
        print(f"📦 Encontrados {len(found_files)} archivos para {base_name}")
        for file in found_files:
            print(f"   - {os.path.basename(file)}")
        
        # Consolidar todos los archivos en un diccionario con la mejor nota por alumno
        best_attempts = {}
        fieldnames = None
        
        for file in found_files:
            with open(file, newline='', encoding=self.encoding) as f:
                reader = csv.DictReader(f)
                if fieldnames is None:
                    fieldnames = reader.fieldnames
                
                id_col = get_col_name(reader.fieldnames, self.header_map["id"])
                grade_col = get_col_name(reader.fieldnames, self.header_map["nota"])
                
                # Detectar escala de calificación
                scale_max = detect_grade_scale(grade_col)
                
                for row in reader:
                    # Filtrar fila de "Promedio general" si está configurado
                    if not self.calculate_avg_grades and is_average_row(row, self.header_map):
                        continue
                    
                    student_id = row[id_col]
                    grade = float(row[grade_col].replace(",", "."))
                    
                    # Normalizar calificación a escala 0-10
                    normalized_grade = normalize_grade_to_scale_10(grade, scale_max)
                    
                    if student_id not in best_attempts:
                        # Guardar con nota normalizada (redondeada a 2 decimales)
                        normalized_row = row.copy()
                        normalized_row[grade_col] = round(normalized_grade, 2)
                        best_attempts[student_id] = normalized_row
                    else:
                        current_grade = best_attempts[student_id][grade_col]
                        if isinstance(current_grade, str):
                            current_grade = float(current_grade.replace(",", "."))
                        
                        if normalized_grade > current_grade:
                            # Actualizar con nota normalizada (redondeada a 2 decimales)
                            normalized_row = row.copy()
                            normalized_row[grade_col] = round(normalized_grade, 2)
                            best_attempts[student_id] = normalized_row
        
        # Guardar el archivo consolidado
        save_csv(output_file, fieldnames, list(best_attempts.values()), self.encoding)
        
        print(f"✅ Consolidado en: {base_name}_filtrado.csv ({len(best_attempts)} alumnos)")
        return True
    
    def _filter_best_grade(self, input_file: str, output_file: str):
        """
        Filtra un archivo CSV manteniendo solo la mejor calificación por alumno.
        
        Args:
            input_file: Ruta al archivo CSV de entrada
            output_file: Ruta al archivo CSV de salida
            
        Raises:
            ValueError: Si el archivo está vacío o no tiene headers válidos
        """
        # Verificar que el archivo no esté vacío y tenga headers
        with open(input_file, newline='', encoding=self.encoding) as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            
            # Validar fieldnames
            if fieldnames is None:
                raise ValueError(f"El archivo '{input_file}' está vacío o no tiene headers")
            
            if not fieldnames:
                raise ValueError(f"El archivo '{input_file}' no tiene columnas")
        
        # Procesar archivo
        best_attempts = read_csv_with_best_grades(input_file, self.header_map, self.encoding, self.calculate_avg_grades)
        
        # Guardar resultado (incluso si está vacío)
        save_csv(output_file, fieldnames, list(best_attempts.values()), self.encoding)
