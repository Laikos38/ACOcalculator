# Guía de Testing - ACOCalculator

## 📋 Descripción

El proyecto ACOCalculator cuenta con una suite completa de tests que utiliza:

- **pytest** - Framework de testing moderno
- **faker** - Generación de datos de prueba realistas
- **factory-boy** - Patrón Factory para crear objetos de prueba
- **pytest-cov** - Análisis de cobertura de código
- **pytest-mock** - Mocking y patching

## 🏗️ Estructura de Tests

```
tests/
├── __init__.py
├── conftest.py                 # Configuración global y fixtures
│
├── factories/                  # Factories para generar datos
│   ├── __init__.py
│   ├── student_factory.py     # Factories de estudiantes
│   └── csv_factory.py         # Factories de archivos CSV
│
├── unit/                       # Tests unitarios
│   ├── test_csv_helpers.py
│   ├── test_config_loader.py
│   └── test_tp_manager.py
│
└── integration/                # Tests de integración
    └── test_full_workflow.py
```

## 🚀 Ejecutar Tests

### Todos los Tests

```bash
# Opción 1: Con script
./scripts/test.sh

# Opción 2: Con uv directamente
uv run pytest

# Opción 3: Verbose
uv run pytest -v
```

### Tests Unitarios Solamente

```bash
./scripts/test-unit.sh
# o
uv run pytest -m unit
```

### Tests de Integración Solamente

```bash
./scripts/test-integration.sh
# o
uv run pytest -m integration
```

### Con Análisis de Cobertura

```bash
./scripts/test-coverage.sh
# o
uv run pytest --cov=src --cov-report=html
```

Esto genera:
- Reporte en terminal
- Reporte HTML en `htmlcov/index.html`

## 📊 Análisis de Cobertura

### Ver Cobertura en Terminal

```bash
uv run pytest --cov=src --cov-report=term-missing
```

### Ver Cobertura en HTML

```bash
uv run pytest --cov=src --cov-report=html
open htmlcov/index.html  # macOS
# o
xdg-open htmlcov/index.html  # Linux
```

### Objetivo de Cobertura

- **Meta mínima**: 70% de cobertura
- **Meta ideal**: 85%+ de cobertura
- **Código crítico**: 95%+ (csv_helpers, conversión de notas)

## 🏷️ Markers (Etiquetas)

Los tests están organizados con markers:

```python
@pytest.mark.unit          # Tests unitarios
@pytest.mark.integration   # Tests de integración
@pytest.mark.slow          # Tests que tardan más tiempo
```

### Usar Markers

```bash
# Solo tests unitarios
pytest -m unit

# Solo tests de integración
pytest -m integration

# Excluir tests lentos
pytest -m "not slow"

# Combinar markers
pytest -m "unit and not slow"
```

## 🏭 Factories - Generación de Datos

### StudentFactory

Genera datos de estudiantes:

```python
from tests.factories import StudentFactory

# Crear un estudiante
student = StudentFactory()
# {'first_name': 'Juan', 'last_name': 'García', 'student_id': '10001'}

# Crear múltiples
students = StudentFactory.build_batch(10)
```

### MoodleStudentRecordFactory

Genera registros completos de Moodle:

```python
from tests.factories.student_factory import MoodleStudentRecordFactory

# Un registro
record = MoodleStudentRecordFactory.create_record()
# {
#     'Apellido(s)': 'García López',
#     'Nombre': 'Juan',
#     'Número de ID': '12345',
#     'Calificación/10,00': '8,5'
# }

# Múltiples intentos del mismo estudiante
records = MoodleStudentRecordFactory.create_multiple_attempts(
    student_id='10001',
    num_attempts=3
)
```

### CSVFileFactory

Genera archivos CSV de prueba:

```python
from tests.factories import CSVFileFactory

# Crear archivo CSV de Moodle
CSVFileFactory.create_moodle_csv(
    'test.csv',
    num_students=10
)

# Crear CSV con múltiples intentos
CSVFileFactory.create_moodle_csv_with_attempts(
    'test.csv',
    {'10001': 3, '10002': 2}  # ID: num_attempts
)
```

## 🧪 Escribir Nuevos Tests

### Test Unitario Básico

```python
import pytest
from src.utils.csv_helpers import convert_grade_to_integer

@pytest.mark.unit
class TestMyFeature:
    """Tests para mi nueva característica."""
    
    def test_something(self):
        """Debe hacer algo específico."""
        result = convert_grade_to_integer("8.5")
        assert result == 8
```

### Test con Fixtures

```python
@pytest.mark.unit
def test_with_fixture(temp_dir, sample_csv_data):
    """Usa fixtures definidos en conftest.py."""
    # temp_dir es un directorio temporal
    # sample_csv_data son datos de muestra
    assert os.path.exists(temp_dir)
    assert len(sample_csv_data) > 0
```

### Test con Factory

```python
from tests.factories import CSVFileFactory

@pytest.mark.unit
def test_with_factory(temp_dir):
    """Usa factory para generar datos."""
    csv_file = os.path.join(temp_dir, "test.csv")
    CSVFileFactory.create_moodle_csv(csv_file, num_students=5)
    
    assert os.path.exists(csv_file)
```

### Test de Integración

```python
@pytest.mark.integration
def test_full_workflow(test_config_path, test_dirs):
    """Test del flujo completo."""
    from src.managers.tp_manager import TPManager
    
    # Setup
    config = ConfigLoader(test_config_path)
    manager = TPManager(config)
    
    # Acción
    manager.merge_tps("1K2")
    
    # Verificación
    output_file = os.path.join(test_dirs['output'], "1K2", "TPs_1K2_mergeado.csv")
    assert os.path.exists(output_file)
```

## 🔧 Fixtures Disponibles

### Fixtures de Archivos

- `temp_dir` - Directorio temporal que se limpia automáticamente
- `test_config_path` - Archivo config.ini de prueba
- `test_dirs` - Directorios de entrada/salida para tests

### Fixtures de Datos

- `sample_header_map` - Mapeo de headers de prueba
- `sample_csv_data` - Datos CSV de muestra

### Ejemplo de Uso

```python
def test_example(temp_dir, test_config_path, sample_csv_data):
    """Todos los fixtures disponibles."""
    # temp_dir: /tmp/pytest-xxx/
    # test_config_path: /tmp/pytest-xxx/config_test.ini
    # sample_csv_data: [{'Apellido(s)': 'García', ...}, ...]
    pass
```

## 📈 Best Practices

### 1. Nomenclatura Clara

```python
# ✅ Bueno
def test_convert_grade_returns_integer():
    ...

# ❌ Malo
def test_1():
    ...
```

### 2. Un Assert por Test (cuando sea posible)

```python
# ✅ Bueno
def test_grade_conversion():
    assert convert_grade_to_integer("8.5") == 8

# ⚠️ Aceptable pero menos específico
def test_multiple_conversions():
    assert convert_grade_to_integer("8.5") == 8
    assert convert_grade_to_integer("7.5") == 7
```

### 3. Usar Parametrize para Múltiples Casos

```python
@pytest.mark.parametrize("grade,expected", [
    ("8.5", 8),
    ("7.5", 7),
    ("9.5", 9),
])
def test_conversions(grade, expected):
    assert convert_grade_to_integer(grade) == expected
```

### 4. Tests Independientes

```python
# ✅ Cada test es independiente
def test_a():
    data = setup_data()
    assert process(data) == expected

def test_b():
    data = setup_data()  # No depende de test_a
    assert validate(data) == True
```

### 5. Cleanup Automático

```python
# ✅ Usa fixtures con yield para cleanup
@pytest.fixture
def my_resource():
    resource = create_resource()
    yield resource
    cleanup_resource(resource)  # Se ejecuta automáticamente
```

## 🐛 Debugging Tests

### Ver Output Detallado

```bash
pytest -v -s  # -s muestra prints
```

### Ejecutar un Test Específico

```bash
# Por archivo
pytest tests/unit/test_csv_helpers.py

# Por clase
pytest tests/unit/test_csv_helpers.py::TestGetColName

# Por método
pytest tests/unit/test_csv_helpers.py::TestGetColName::test_encuentra_columna
```

### Detener en Primer Fallo

```bash
pytest -x  # stop on first failure
```

### Ver Locals en Fallos

```bash
pytest -l  # show local variables
```

### Modo Debug Interactivo

```bash
pytest --pdb  # entra en debugger en fallos
```

## 📊 CI/CD Integration

### GitHub Actions (Ejemplo)

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Install dependencies
        run: uv sync --dev
      - name: Run tests
        run: uv run pytest --cov=src
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 🎯 Comandos Rápidos

```bash
# Desarrollo diario
./scripts/test.sh                 # Todos los tests
./scripts/test-unit.sh            # Solo unitarios
./scripts/test-coverage.sh        # Con cobertura

# Tests específicos
uv run pytest tests/unit/test_csv_helpers.py -v
uv run pytest -m unit -v
uv run pytest -k "test_conversion" -v

# Debugging
uv run pytest -x -v -s            # Stop on fail, verbose, show prints
uv run pytest --pdb               # Debug interactivo
uv run pytest -l                  # Show locals

# Cobertura
uv run pytest --cov=src --cov-report=term-missing
open htmlcov/index.html
```

## 📚 Recursos Adicionales

- **Pytest Docs**: https://docs.pytest.org/
- **Faker Docs**: https://faker.readthedocs.io/
- **Factory Boy Docs**: https://factoryboy.readthedocs.io/

---

**¡Los tests son documentación ejecutable! Mantenlos actualizados.**

