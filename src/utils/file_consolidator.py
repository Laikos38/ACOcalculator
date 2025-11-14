"""
Módulo para consolidar múltiples archivos de un mismo TP o Parcial.
"""
import glob
import os
import csv
from typing import Dict, Optional
from .csv_helpers import get_col_name, save_csv, read_csv_with_best_grades


class FileConsolidator:
    """Clase para consolidar múltiples archivos CSV de un mismo TP o Parcial."""
    
    def __init__(self, source_dir: str, output_dir: str, header_map: Dict, encoding: str = 'utf-8-sig'):
        """
        Inicializa el consolidador de archivos.
        
        Args:
            source_dir: Directorio de archivos de entrada
            output_dir: Directorio de archivos de salida
            header_map: Mapeo de nombres de columnas
            encoding: Encoding de archivos CSV
        """
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.header_map = header_map
        self.encoding = encoding
    
    def consolidate_multiple_files(self, base_name: str, course: str) -> bool:
        """
        Busca y consolida múltiples archivos de un mismo TP o Parcial.
        
        Por ejemplo, si hay Parcial1_1K2_1.csv y Parcial1_1K2_2.csv,
        los consolida en un solo archivo Parcial1_1K2_filtrado.csv tomando
        la mejor calificación de cada alumno entre todos los archivos.
        
        Args:
            base_name: Nombre base sin extensión (ej: "Parcial1_1K2", "TP1_1K4")
            course: Código del curso (ej: "1K2", "1K4")
            
        Returns:
            bool: True si se encontraron y consolidaron archivos, False si no
        """
        # Buscar todos los archivos que coincidan con el patrón
        pattern = os.path.join(self.source_dir, f"{base_name}_*.csv")
        found_files = glob.glob(pattern)
        
        # También buscar el archivo sin sufijo numérico
        base_file = os.path.join(self.source_dir, f"{base_name}.csv")
        if os.path.exists(base_file):
            found_files.append(base_file)
        
        if not found_files:
            return False
        
        # Extraer el curso del base_name y crear el directorio de salida
        parts = base_name.split("_")
        if len(parts) >= 2:
            course_dir = parts[-1]  # Último elemento es el curso
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
                
                for row in reader:
                    student_id = row[id_col]
                    grade = float(row[grade_col].replace(",", "."))
                    
                    if student_id not in best_attempts:
                        best_attempts[student_id] = row
                    else:
                        current_grade = float(best_attempts[student_id][grade_col].replace(",", "."))
                        if grade > current_grade:
                            best_attempts[student_id] = row
        
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
        best_attempts = read_csv_with_best_grades(input_file, self.header_map, self.encoding)
        
        # Guardar resultado (incluso si está vacío)
        save_csv(output_file, fieldnames, list(best_attempts.values()), self.encoding)
