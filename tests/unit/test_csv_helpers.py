"""
Tests unitarios para el módulo csv_helpers.
"""
import pytest
from src.utils.csv_helpers import (
    get_col_name,
    convert_grade_to_integer,
    save_csv
)


@pytest.mark.unit
class TestGetColName:
    """Tests para la función get_col_name."""
    
    def test_encuentra_columna_primer_nombre(self):
        """Debe encontrar la columna usando el primer nombre posible."""
        fieldnames = ["Apellido(s)", "Nombre", "ID"]
        possible_names = ["Apellido(s)", "Apellidos"]
        
        result = get_col_name(fieldnames, possible_names)
        
        assert result == "Apellido(s)"
    
    def test_encuentra_columna_segundo_nombre(self):
        """Debe encontrar la columna usando el segundo nombre posible."""
        fieldnames = ["Last Name", "First Name", "ID"]
        possible_names = ["Apellido(s)", "Last Name"]
        
        result = get_col_name(fieldnames, possible_names)
        
        assert result == "Last Name"
    
    def test_error_cuando_no_encuentra_columna(self):
        """Debe lanzar KeyError cuando no encuentra ninguna columna."""
        fieldnames = ["Columna1", "Columna2"]
        possible_names = ["NoExiste1", "NoExiste2"]
        
        with pytest.raises(KeyError) as exc_info:
            get_col_name(fieldnames, possible_names)
        
        assert "No se encontró ninguna de las columnas" in str(exc_info.value)


@pytest.mark.unit
class TestConvertGradeToInteger:
    """Tests para la función convert_grade_to_integer."""
    
    @pytest.mark.parametrize("grade_str,expected", [
        ("10.0", 10),
        ("9.6", 10),
        ("9.5", 9),
        ("8.7", 9),
        ("8.6", 8),
        ("7.8", 8),
        ("7.7", 7),
        ("6.9", 7),
        ("6.8", 6),
        ("6.0", 6),
        ("5.9", 5),
        ("5.8", 5),
        ("5.7", 4),
        ("5.5", 4),
        ("5.4", 2),
        ("0.0", 2),
    ])
    def test_conversion_correcta_de_notas(self, grade_str, expected):
        """Debe convertir correctamente las notas según la escala."""
        result = convert_grade_to_integer(grade_str)
        assert result == expected
    
    def test_nota_vacia_retorna_falta(self):
        """Debe retornar 'FALTA' para nota vacía."""
        assert convert_grade_to_integer("") == "FALTA"
        assert convert_grade_to_integer("   ") == "FALTA"
        assert convert_grade_to_integer(None) == "FALTA"
    
    def test_nota_invalida_retorna_falta(self):
        """Debe retornar 'FALTA' para nota inválida."""
        assert convert_grade_to_integer("abc") == "FALTA"
        assert convert_grade_to_integer("no-es-numero") == "FALTA"
    
    def test_nota_fuera_de_rango_retorna_falta(self):
        """Debe retornar 'FALTA' para notas fuera del rango 0-10."""
        assert convert_grade_to_integer("15.0") == "FALTA"
        assert convert_grade_to_integer("-5.0") == "FALTA"


@pytest.mark.unit
class TestSaveCSV:
    """Tests para la función save_csv."""
    
    def test_guarda_csv_correctamente(self, temp_dir):
        """Debe guardar un CSV correctamente."""
        import os
        import csv
        
        file_path = os.path.join(temp_dir, "test.csv")
        fieldnames = ["col1", "col2", "col3"]
        data = [
            {"col1": "valor1", "col2": "valor2", "col3": "valor3"},
            {"col1": "valor4", "col2": "valor5", "col3": "valor6"},
        ]
        
        save_csv(file_path, fieldnames, data)
        
        # Verificar que el archivo existe
        assert os.path.exists(file_path)
        
        # Verificar el contenido
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            
        assert len(rows) == 2
        assert rows[0]["col1"] == "valor1"
        assert rows[1]["col2"] == "valor5"
    
    def test_crea_directorio_si_no_existe(self, temp_dir):
        """Debe crear el directorio padre si no existe."""
        import os
        
        file_path = os.path.join(temp_dir, "subdir", "subsubdir", "test.csv")
        fieldnames = ["col1"]
        data = [{"col1": "valor1"}]
        
        save_csv(file_path, fieldnames, data)
        
        assert os.path.exists(file_path)

