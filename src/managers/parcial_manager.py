"""
Módulo para gestionar los Parciales y Recuperatorios.
"""
import os
import csv
from typing import Dict
from ..utils import (
    ConfigLoader,
    FileConsolidator,
    get_col_name,
    convert_grade_to_integer,
    save_csv
)


class ParcialManager:
    """Clase para gestionar los Parciales y Recuperatorios."""
    
    def __init__(self, config: ConfigLoader):
        """
        Inicializa el gestor de Parciales.
        
        Args:
            config: Instancia de ConfigLoader con la configuración del sistema
        """
        self.config = config
        self.source_dir = config.get_source_dir()
        self.output_dir = config.get_output_dir()
        self.header_map = config.get_header_map()
        self.encoding = config.get_csv_encoding()
        self.exam_count = config.get_cantidad_parciales()
        self.makeup_count = config.get_cantidad_recuperatorios()
        self.exam_prefix = config.get_parcial_prefix()
        self.makeup_prefix = config.get_recuperatorio_prefix()
        self.calculate_avg_grades = config.get_calculate_avg_grades()
        
        self.consolidator = FileConsolidator(
            self.source_dir,
            self.output_dir,
            self.header_map,
            "parciales",
            self.encoding,
            self.calculate_avg_grades
        )
    
    def merge_exams(self, course: str):
        """
        Fusiona todos los Parciales y Recuperatorios de un curso en un único archivo CSV.
        Soporta nombres de curso case-insensitive (ej: "1k2", "1K2").
        
        Args:
            course: Código del curso (ej: "1K2", "1K4")
        """
        # Normalizar curso a mayúsculas para consistencia
        course = course.upper()
        
        files = {}
        
        # Agregar parciales
        for i in range(1, self.exam_count + 1):
            files[f"{self.exam_prefix}{i}"] = f"{self.exam_prefix}{i}_{course}"
        
        # Agregar recuperatorios
        for i in range(1, self.makeup_count + 1):
            files[f"{self.makeup_prefix}{i}"] = f"{self.makeup_prefix}{i}_{course}"
        
        data = {}
        
        # Directorio de salida específico del curso (ya normalizado)
        output_course_dir = os.path.join(self.output_dir, course)
        output_course_dir = os.path.join(output_course_dir, "parciales")
        
        for evaluation, base_name in files.items():
            filtered_file = os.path.join(output_course_dir, base_name + "_filtrado.csv")
            
            # Si no existe el filtrado, generarlo desde el/los source(s)
            # if not os.path.exists(filtered_file):
            #     print(f"⚠️ No se encontró el archivo filtrado para {base_name}. Generando desde archivos en inputs/...")
            if not self.consolidator.consolidate_multiple_files(base_name, course):
                print(f"⚠️ No se encontraron archivos en inputs/ para {base_name}. Se ignorará.")
                continue
            
            # Leer el archivo filtrado (ya existente o recién generado)
            with open(filtered_file, newline='', encoding=self.encoding) as f:
                reader = csv.DictReader(f)
                last_name_col = get_col_name(reader.fieldnames, self.header_map["apellido"])
                first_name_col = get_col_name(reader.fieldnames, self.header_map["nombre"])
                id_col = get_col_name(reader.fieldnames, self.header_map["id"])
                grade_col = get_col_name(reader.fieldnames, self.header_map["nota"])
                
                for row in reader:
                    student_id = row[id_col]
                    if student_id not in data:
                        # Inicializar estructura de datos para el alumno
                        data[student_id] = {
                            "Apellido(s)": row[last_name_col],
                            "Nombre": row[first_name_col],
                            "Número de ID": student_id,
                        }
                        # Inicializar columnas de Parciales
                        for i in range(1, self.exam_count + 1):
                            data[student_id][f"{self.exam_prefix}{i}"] = ""
                            data[student_id][f"{self.exam_prefix}{i}_Nota"] = ""
                        # Inicializar columnas de Recuperatorios
                        for i in range(1, self.makeup_count + 1):
                            data[student_id][f"{self.makeup_prefix}{i}"] = ""
                            data[student_id][f"{self.makeup_prefix}{i}_Nota"] = ""
                    
                    # Guardar la nota decimal como float redondeado a 2 decimales
                    grade_col_value = row[grade_col]
                    if isinstance(grade_col_value, str):
                        grade_decimal = float(grade_col_value.replace(",", "."))
                    else:
                        grade_decimal = float(grade_col_value)
                    data[student_id][evaluation] = round(grade_decimal, 2)
                    # Guardar la nota convertida a entero
                    data[student_id][f"{evaluation}_Nota"] = convert_grade_to_integer(str(grade_decimal))
        
        if not data:
            print("⚠️ No se pudo unificar los Parciales porque no hay datos disponibles.")
            return
        
        os.makedirs(output_course_dir, exist_ok=True)
        merge_file = os.path.join(output_course_dir, f"{self.exam_prefix}es_{course}_unificado.csv")
        
        # Construir fieldnames dinámicamente
        fieldnames = ["Apellido(s)", "Nombre", "Número de ID"]
        for i in range(1, self.exam_count + 1):
            fieldnames.extend([
                f"{self.exam_prefix}{i}",
                f"{self.exam_prefix}{i}_Nota"
            ])
        for i in range(1, self.makeup_count + 1):
            fieldnames.extend([
                f"{self.makeup_prefix}{i}",
                f"{self.makeup_prefix}{i}_Nota"
            ])
        
        save_csv(merge_file, fieldnames, list(data.values()), self.encoding)
        
        print(f"✅ Unificación de Parciales completada: {merge_file}")
    
    def filter_best_grade(self, file_name: str, detected_course: str = None):
        """
        Filtra un archivo CSV individual manteniendo solo la mejor calificación por alumno.
        
        Args:
            file_name: Nombre del archivo a procesar
            detected_course: Curso detectado del nombre del archivo (opcional)
        """
        input_path = os.path.join(self.source_dir, file_name)
        
        # Verificar que el archivo exista
        if not os.path.exists(input_path):
            print(f"❌ Error: El archivo '{file_name}' no existe")
            return
        
        # Detectar el curso del nombre del archivo si no se proporciona
        if detected_course is None:
            name_without_ext = file_name.replace(".csv", "")
            parts = name_without_ext.split("_")
            if len(parts) >= 2:
                detected_course = parts[-1]
                # Remover sufijos numéricos si los hay (ej: 1K2_1 -> 1K2)
                if detected_course[-1].isdigit() and len(detected_course) > 1:
                    detected_course = "_".join(parts[:-1])
                    if "_" in detected_course:
                        detected_course = detected_course.split("_")[-1]
        
        if detected_course:
            output_course_dir = os.path.join(self.output_dir, detected_course.upper())
        else:
            output_course_dir = self.output_dir
        
        os.makedirs(output_course_dir, exist_ok=True)
        
        # Normalizar nombre del archivo de salida (mayúsculas para consistencia)
        output_filename = file_name.replace(".csv", "_filtrado.csv")
        # Extraer las partes del nombre y normalizar el prefijo y curso
        name_parts = output_filename.split("_")
        if len(name_parts) >= 2:
            # Normalizar cada parte (mantener el número, pero capitalizar el resto)
            normalized_parts = []
            for part in name_parts:
                if part.lower() == "filtrado.csv":
                    normalized_parts.append("filtrado.csv")
                elif part.isdigit():
                    normalized_parts.append(part)
                else:
                    # Normalizar prefijo/curso a mayúsculas
                    normalized_parts.append(part.upper())
            output_filename = "_".join(normalized_parts)
        
        output_path = os.path.join(output_course_dir, output_filename)
        
        try:
            self.consolidator._filter_best_grade(input_path, output_path)
            print(f"✅ Archivo procesado y guardado en '{output_path}'")
        except ValueError as e:
            print(f"❌ Error al procesar '{file_name}': {e}")
        except KeyError as e:
            print(f"❌ Error al procesar '{file_name}': {e}")
        except Exception as e:
            print(f"❌ Error inesperado al procesar '{file_name}': {e}")
