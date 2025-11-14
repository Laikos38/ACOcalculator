"""
Factories para generar datos de estudiantes usando Factory Boy y Faker.
"""
import factory
from faker import Faker

fake = Faker('es_ES')  # Usar locale español


class StudentFactory(factory.Factory):
    """Factory para generar datos de estudiantes."""
    
    class Meta:
        model = dict
    
    first_name = factory.LazyFunction(lambda: fake.first_name())
    last_name = factory.LazyFunction(lambda: fake.last_name())
    student_id = factory.Sequence(lambda n: f"{10000 + n}")
    

class StudentRecordFactory(factory.Factory):
    """Factory para generar registros completos de estudiantes con calificaciones."""
    
    class Meta:
        model = dict
    
    # Headers en español (formato Moodle)
    Apellidos = factory.LazyFunction(lambda: f"{fake.last_name()} {fake.last_name()}")
    Nombre = factory.LazyFunction(lambda: fake.first_name())
    student_id = factory.Sequence(lambda n: f"{10000 + n}")
    
    # Alias para diferentes formatos de ID
    @factory.lazy_attribute
    def ID(self):
        return self.student_id
    
    @factory.lazy_attribute_sequence
    def grade(self, n):
        """Genera una calificación entre 0 y 10."""
        return round(fake.random.uniform(0, 10), 2)
    
    # Formato Moodle en español
    @factory.lazy_attribute
    def calification(self):
        """Calificación en formato string con coma."""
        return str(self.grade).replace('.', ',')


class MoodleStudentRecordFactory:
    """Factory específico para registros de Moodle."""
    
    @classmethod
    def create_record(cls, last_name=None, first_name=None, student_id=None, grade=None):
        """Crea un registro completo de Moodle."""
        return {
            "Apellido(s)": last_name or f"{fake.last_name()} {fake.last_name()}",
            "Nombre": first_name or fake.first_name(),
            "Número de ID": student_id or str(fake.random.randint(10000, 99999)),
            "Calificación/10,00": grade or str(round(fake.random.uniform(0, 10), 2)).replace('.', ','),
        }
    
    @classmethod
    def create_multiple_attempts(cls, student_id, num_attempts=3):
        """Crea múltiples intentos para un mismo estudiante."""
        last_name = f"{fake.last_name()} {fake.last_name()}"
        first_name = fake.first_name()
        
        records = []
        for _ in range(num_attempts):
            grade = round(fake.random.uniform(0, 10), 2)
            records.append(cls.create_record(
                last_name=last_name,
                first_name=first_name,
                student_id=student_id,
                grade=str(grade).replace('.', ',')
            ))
        
        return records

