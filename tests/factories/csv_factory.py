"""
Factories para generar archivos CSV de prueba.
"""
import csv
import os
from pathlib import Path
from faker import Faker
from .student_factory import MoodleStudentRecordFactory

fake = Faker('es_ES')


class CSVFileFactory:
    """Factory para crear archivos CSV de prueba."""
    
    @staticmethod
    def create_moodle_csv(file_path, num_students=10, encoding='utf-8-sig'):
        """
        Crea un archivo CSV con formato Moodle.
        
        Args:
            file_path: Ruta donde crear el archivo
            num_students: Número de estudiantes a generar
            encoding: Encoding del archivo
        """
        # Asegurar que el directorio existe
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        fieldnames = ["Apellido(s)", "Nombre", "Número de ID", "Calificación/10,00"]
        
        with open(file_path, 'w', newline='', encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for i in range(num_students):
                record = MoodleStudentRecordFactory.create_record(
                    student_id=str(10000 + i)
                )
                writer.writerow(record)
        
        return file_path
    
    @staticmethod
    def create_moodle_csv_with_attempts(file_path, students_with_attempts, encoding='utf-8-sig'):
        """
        Crea un archivo CSV con múltiples intentos por estudiante.
        
        Args:
            file_path: Ruta donde crear el archivo
            students_with_attempts: Dict {student_id: num_attempts}
            encoding: Encoding del archivo
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        fieldnames = ["Apellido(s)", "Nombre", "Número de ID", "Calificación/10,00"]
        
        with open(file_path, 'w', newline='', encoding=encoding) as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for student_id, num_attempts in students_with_attempts.items():
                records = MoodleStudentRecordFactory.create_multiple_attempts(
                    student_id=student_id,
                    num_attempts=num_attempts
                )
                for record in records:
                    writer.writerow(record)
        
        return file_path
    
    @staticmethod
    def create_tp_file(file_path, course, tp_num, num_students=10):
        """Crea un archivo de TP con el formato esperado."""
        return CSVFileFactory.create_moodle_csv(file_path, num_students)
    
    @staticmethod
    def create_parcial_file(file_path, course, parcial_num, num_students=10):
        """Crea un archivo de Parcial con el formato esperado."""
        return CSVFileFactory.create_moodle_csv(file_path, num_students)


class MoodleGradeFactory:
    """Factory para generar calificaciones en formato Moodle."""
    
    @staticmethod
    def generate_grade(min_grade=0.0, max_grade=10.0):
        """Genera una calificación aleatoria."""
        grade = round(fake.random.uniform(min_grade, max_grade), 2)
        return str(grade).replace('.', ',')
    
    @staticmethod
    def generate_passing_grade():
        """Genera una calificación aprobada (>= 6.0)."""
        return MoodleGradeFactory.generate_grade(6.0, 10.0)
    
    @staticmethod
    def generate_failing_grade():
        """Genera una calificación desaprobada (< 6.0)."""
        return MoodleGradeFactory.generate_grade(0.0, 5.99)
    
    @staticmethod
    def generate_excellent_grade():
        """Genera una calificación excelente (>= 9.0)."""
        return MoodleGradeFactory.generate_grade(9.0, 10.0)

