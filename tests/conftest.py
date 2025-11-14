"""
Configuración global de pytest y fixtures compartidos.
"""
import pytest
import os
import tempfile
import shutil
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Crea un directorio temporal para tests."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def test_config_path(temp_dir):
    """Crea un archivo de configuración de prueba."""
    config_content = """[Directorios]
source_dir = test_inputs
output_dir = test_outputs

[Headers]
calification_header = Calificación/10,00
header_apellido = Apellido(s), Apellidos, Last Name
header_nombre = Nombre, First Name
header_id = Número de ID, ID

[TrabajoPractico]
cantidad_tps = 4
tp_prefix = TP

[Parciales]
cantidad_parciales = 2
cantidad_recuperatorios = 2
parcial_prefix = Parcial
recuperatorio_prefix = Recuperatorio

[Formatos]
csv_encoding = utf-8-sig
output_format = xls
"""
    config_path = os.path.join(temp_dir, "config_test.ini")
    with open(config_path, 'w') as f:
        f.write(config_content)
    return config_path


@pytest.fixture
def test_dirs(temp_dir):
    """Crea directorios de entrada y salida para tests."""
    input_dir = os.path.join(temp_dir, "test_inputs")
    output_dir = os.path.join(temp_dir, "test_outputs")
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    return {
        'root': temp_dir,
        'input': input_dir,
        'output': output_dir
    }


@pytest.fixture
def sample_header_map():
    """Retorna un mapeo de headers de prueba."""
    return {
        "apellido": ["Apellido(s)", "Apellidos", "Last Name"],
        "nombre": ["Nombre", "First Name"],
        "id": ["Número de ID", "ID"],
        "nota": ["Calificación/10,00"],
    }


@pytest.fixture
def sample_csv_data():
    """Retorna datos de muestra para CSV."""
    return [
        {
            "Apellido(s)": "García",
            "Nombre": "Juan",
            "Número de ID": "12345",
            "Calificación/10,00": "8.5"
        },
        {
            "Apellido(s)": "López",
            "Nombre": "María",
            "Número de ID": "12346",
            "Calificación/10,00": "9.2"
        },
        {
            "Apellido(s)": "Martínez",
            "Nombre": "Pedro",
            "Número de ID": "12347",
            "Calificación/10,00": "7.8"
        }
    ]


@pytest.fixture(autouse=True)
def reset_env():
    """Resetea variables de entorno antes de cada test."""
    # Guardar variables originales
    original_cwd = os.getcwd()
    
    yield
    
    # Restaurar estado original
    os.chdir(original_cwd)

