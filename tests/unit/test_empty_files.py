"""
Tests para manejo de archivos vacíos o con problemas.
"""
import pytest
import os
import csv
from src.utils.csv_helpers import get_col_name, read_csv_with_best_grades
from src.utils.file_consolidator import FileConsolidator
from src.managers.tp_manager import TPManager
from src.utils.config_loader import ConfigLoader


@pytest.mark.unit
class TestEmptyFilesHandling:
    """Tests para manejo de archivos vacíos."""
    
    def test_get_col_name_with_none_fieldnames(self):
        """Debe lanzar ValueError cuando fieldnames es None."""
        with pytest.raises(ValueError) as exc_info:
            get_col_name(None, ["Columna1", "Columna2"])
        
        assert "vacío o no tiene headers" in str(exc_info.value)
    
    def test_get_col_name_with_empty_fieldnames(self):
        """Debe lanzar ValueError cuando fieldnames está vacío."""
        with pytest.raises(ValueError) as exc_info:
            get_col_name([], ["Columna1", "Columna2"])
        
        assert "no tiene columnas" in str(exc_info.value)
    
    def test_empty_csv_file(self, temp_dir):
        """Debe manejar correctamente un archivo CSV completamente vacío."""
        # Crear archivo vacío
        empty_file = os.path.join(temp_dir, "empty.csv")
        with open(empty_file, 'w') as f:
            pass  # Archivo completamente vacío
        
        # Debe lanzar ValueError al intentar procesarlo
        header_map = {
            "apellido": ["Apellido(s)"],
            "nombre": ["Nombre"],
            "id": ["Número de ID"],
            "nota": ["Calificación/10,00"],
        }
        
        consolidator = FileConsolidator(
            temp_dir,
            temp_dir,
            header_map,
            'utf-8-sig'
        )
        
        output_file = os.path.join(temp_dir, "output.csv")
        
        with pytest.raises(ValueError) as exc_info:
            consolidator._filter_best_grade(empty_file, output_file)
        
        assert "vacío o no tiene headers" in str(exc_info.value)
    
    def test_csv_file_with_only_headers(self, temp_dir):
        """Debe manejar correctamente un archivo CSV con solo headers."""
        # Crear archivo con solo headers
        headers_only = os.path.join(temp_dir, "headers_only.csv")
        with open(headers_only, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=["Apellido(s)", "Nombre", "Número de ID", "Calificación/10,00"])
            writer.writeheader()
            # No escribir filas
        
        header_map = {
            "apellido": ["Apellido(s)"],
            "nombre": ["Nombre"],
            "id": ["Número de ID"],
            "nota": ["Calificación/10,00"],
        }
        
        consolidator = FileConsolidator(
            temp_dir,
            temp_dir,
            header_map,
            'utf-8-sig'
        )
        
        output_file = os.path.join(temp_dir, "output.csv")
        
        # Debe procesar sin error (archivo válido pero sin datos)
        consolidator._filter_best_grade(headers_only, output_file)
        
        # Verificar que se creó el archivo de salida
        assert os.path.exists(output_file)
        
        # Verificar que tiene headers pero no datos
        with open(output_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 0  # Sin datos
    
    def test_csv_file_with_missing_columns(self, temp_dir):
        """Debe manejar correctamente un CSV sin las columnas esperadas."""
        # Crear archivo con columnas incorrectas
        wrong_columns = os.path.join(temp_dir, "wrong_columns.csv")
        with open(wrong_columns, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=["ColumnA", "ColumnB", "ColumnC"])
            writer.writeheader()
            writer.writerow({"ColumnA": "Data1", "ColumnB": "Data2", "ColumnC": "Data3"})
        
        header_map = {
            "apellido": ["Apellido(s)"],
            "nombre": ["Nombre"],
            "id": ["Número de ID"],
            "nota": ["Calificación/10,00"],
        }
        
        # Debe lanzar KeyError al intentar encontrar columnas
        with pytest.raises(KeyError) as exc_info:
            read_csv_with_best_grades(wrong_columns, header_map, 'utf-8-sig')
        
        assert "No se encontró ninguna de las columnas" in str(exc_info.value)
    
    def test_tp_manager_handles_empty_file_gracefully(self, test_config_path, test_dirs):
        """TPManager debe manejar archivos vacíos sin crashear."""
        os.chdir(test_dirs['root'])
        config = ConfigLoader(test_config_path)
        tp_manager = TPManager(config)
        
        # Crear archivo vacío en inputs
        empty_file = os.path.join(test_dirs['input'], "TP1_1K2.csv")
        with open(empty_file, 'w') as f:
            pass  # Vacío
        
        # Debe manejar el error gracefully (no crashear)
        # La función imprime el error pero no lanza excepción
        tp_manager.filter_best_grade("TP1_1K2.csv")
        
        # Verificar que no se creó archivo de salida
        output_file = os.path.join(test_dirs['output'], "1K2", "TP1_1K2_filtrado.csv")
        assert not os.path.exists(output_file)
    
    def test_csv_with_corrupted_headers(self, temp_dir):
        """Debe lanzar KeyError cuando los headers no coinciden por corrupción."""
        # Crear archivo con headers corruptos (la coma es interpretada como separador)
        corrupted = os.path.join(temp_dir, "corrupted.csv")
        with open(corrupted, 'w', encoding='utf-8-sig') as f:
            f.write("Apellido(s),Nombre,Número de ID,Calificación/10,00\n")  # Coma se interpreta como separador
            f.write("García,Juan,12345,8,5\n")
        
        header_map = {
            "apellido": ["Apellido(s)"],
            "nombre": ["Nombre"],
            "id": ["Número de ID"],
            "nota": ["Calificación/10,00"],  # Este header no existirá, estará dividido
        }
        
        # Debe lanzar KeyError porque los headers no coinciden
        with pytest.raises(KeyError) as exc_info:
            read_csv_with_best_grades(corrupted, header_map, 'utf-8-sig')
        
        assert "No se encontró ninguna de las columnas" in str(exc_info.value)


@pytest.mark.unit
class TestEdgeCases:
    """Tests para casos extremos."""
    
    def test_csv_with_single_row(self, temp_dir):
        """Debe procesar correctamente un CSV con una sola fila."""
        single_row = os.path.join(temp_dir, "single.csv")
        with open(single_row, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=["Apellido(s)", "Nombre", "Número de ID", "Calificación/10,00"])
            writer.writeheader()
            writer.writerow({
                "Apellido(s)": "García",
                "Nombre": "Juan",
                "Número de ID": "12345",
                "Calificación/10,00": "8,5"
            })
        
        header_map = {
            "apellido": ["Apellido(s)"],
            "nombre": ["Nombre"],
            "id": ["Número de ID"],
            "nota": ["Calificación/10,00"],
        }
        
        result = read_csv_with_best_grades(single_row, header_map, 'utf-8-sig')
        
        assert len(result) == 1
        assert "12345" in result
    
    def test_csv_with_whitespace_only(self, temp_dir):
        """Debe manejar archivo con solo espacios en blanco."""
        whitespace = os.path.join(temp_dir, "whitespace.csv")
        with open(whitespace, 'w', encoding='utf-8-sig') as f:
            f.write("   \n\n  \n")  # Solo espacios y líneas vacías
        
        header_map = {
            "apellido": ["Apellido(s)"],
            "nombre": ["Nombre"],
            "id": ["Número de ID"],
            "nota": ["Calificación/10,00"],
        }
        
        consolidator = FileConsolidator(
            temp_dir,
            temp_dir,
            header_map,
            'utf-8-sig'
        )
        
        output_file = os.path.join(temp_dir, "output.csv")
        
        # Debe lanzar error (ValueError o KeyError) por headers inválidos
        with pytest.raises((ValueError, KeyError)):
            consolidator._filter_best_grade(whitespace, output_file)

