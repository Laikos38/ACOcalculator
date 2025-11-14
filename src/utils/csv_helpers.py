"""
Módulo con funciones auxiliares para manejo de archivos CSV.
"""
import csv
import os
from typing import Dict, List


def get_col_name(fieldnames: List[str], possible_names: List[str]) -> str:
    """
    Devuelve el nombre real de la columna si existe en fieldnames.
    
    Args:
        fieldnames: Lista de nombres de columnas disponibles
        possible_names: Lista de posibles nombres para la columna buscada
        
    Returns:
        El nombre de la columna encontrada
        
    Raises:
        ValueError: Si fieldnames es None o está vacío
        KeyError: Si no se encuentra ninguna columna coincidente
    """
    if fieldnames is None:
        raise ValueError("El archivo CSV está vacío o no tiene headers")
    
    if not fieldnames:
        raise ValueError("El archivo CSV no tiene columnas")
    
    for name in possible_names:
        if name in fieldnames:
            return name
    raise KeyError(f"No se encontró ninguna de las columnas {possible_names} en {fieldnames}")


def convert_grade_to_integer(grade_str: str) -> any:
    """
    Convierte una nota decimal a su equivalente entero según la escala de calificación.
    
    Las notas de Moodle vienen en escala 0-10, se multiplican por 10 para llevarlas
    a escala 0-100 y luego se aplica la conversión a escala entera (2-10).
    
    Escala de conversión (base 100):
    - 0 a 54.44 -> 2
    - 54.45 a 57.44 -> 4
    - 57.45 a 59.44 -> 5
    - 59.45 a 68.44 -> 6
    - 68.45 a 77.44 -> 7
    - 77.45 a 86.44 -> 8
    - 86.45 a 95.44 -> 9
    - 95.45 a 100 -> 10
    - Si está vacío o fuera de rango -> "FALTA"
    
    Args:
        grade_str: Nota en formato string
        
    Returns:
        Nota convertida a entero (2-10) o "FALTA"
    """
    if not grade_str or grade_str.strip() == "":
        return "FALTA"
    
    try:
        grade = float(grade_str)
    except ValueError:
        return "FALTA"
    
    # Convertir de escala 0-10 a escala 0-100
    grade_100 = grade * 10
    
    if 0 <= grade_100 <= 54.44:
        return 2
    elif 54.45 <= grade_100 <= 57.44:
        return 4
    elif 57.45 <= grade_100 <= 59.44:
        return 5
    elif 59.45 <= grade_100 <= 68.44:
        return 6
    elif 68.45 <= grade_100 <= 77.44:
        return 7
    elif 77.45 <= grade_100 <= 86.44:
        return 8
    elif 86.45 <= grade_100 <= 95.44:
        return 9
    elif 95.45 <= grade_100 <= 100:
        return 10
    else:
        return "FALTA"


def read_csv_with_best_grades(file_path: str, header_map: Dict, encoding: str = 'utf-8-sig') -> Dict:
    """
    Lee un archivo CSV y retorna un diccionario con las mejores notas por alumno.
    
    Args:
        file_path: Ruta al archivo CSV
        header_map: Mapeo de nombres de columnas
        encoding: Encoding del archivo
        
    Returns:
        Diccionario con ID de alumno como clave y su mejor registro como valor
    """
    best_attempts = {}
    
    with open(file_path, newline='', encoding=encoding) as f:
        reader = csv.DictReader(f)
        id_col = get_col_name(reader.fieldnames, header_map["id"])
        grade_col = get_col_name(reader.fieldnames, header_map["nota"])
        
        for row in reader:
            student_id = row[id_col]
            grade = float(row[grade_col].replace(",", "."))
            
            if student_id not in best_attempts:
                best_attempts[student_id] = row
            else:
                current_grade = float(best_attempts[student_id][grade_col].replace(",", "."))
                if grade > current_grade:
                    best_attempts[student_id] = row
    
    return best_attempts


def count_student_attempts(file_path: str, header_map: Dict, encoding: str = 'utf-8-sig') -> Dict[str, int]:
    """
    Cuenta la cantidad de intentos por alumno en un archivo CSV.
    
    Args:
        file_path: Ruta al archivo CSV
        header_map: Mapeo de nombres de columnas
        encoding: Encoding del archivo
        
    Returns:
        Diccionario con ID de alumno como clave y cantidad de intentos como valor
    """
    attempts = {}
    
    if not os.path.exists(file_path):
        return attempts
    
    with open(file_path, newline='', encoding=encoding) as f:
        reader = csv.DictReader(f)
        id_col = get_col_name(reader.fieldnames, header_map["id"])
        
        for row in reader:
            student_id = row[id_col]
            attempts[student_id] = attempts.get(student_id, 0) + 1
    
    return attempts


def save_csv(file_path: str, fieldnames: List[str], data: List[Dict], encoding: str = 'utf-8-sig'):
    """
    Guarda datos en un archivo CSV.
    
    Args:
        file_path: Ruta del archivo de salida
        fieldnames: Lista de nombres de columnas
        data: Lista de diccionarios con los datos
        encoding: Encoding del archivo
    """
    # Asegurar que el directorio de salida exista
    output_dir = os.path.dirname(file_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    with open(file_path, "w", newline='', encoding=encoding) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
