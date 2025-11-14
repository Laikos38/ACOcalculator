"""
Tests unitarios para el módulo ConfigLoader.
"""
import pytest
import os
from src.utils.config_loader import ConfigLoader


@pytest.mark.unit
class TestConfigLoader:
    """Tests para la clase ConfigLoader."""
    
    def test_carga_configuracion_correctamente(self, test_config_path):
        """Debe cargar la configuración desde un archivo ini."""
        config = ConfigLoader(test_config_path)
        
        assert config.get_source_dir() == "test_inputs"
        assert config.get_output_dir() == "test_outputs"
    
    def test_usa_default_cuando_archivo_no_existe(self, temp_dir):
        """Debe usar configuración por defecto cuando el archivo no existe."""
        os.chdir(temp_dir)
        config = ConfigLoader("no_existe.ini")
        
        # No debe lanzar excepción, debe usar default
        assert config.is_using_default() == True
        assert config.get_source_dir() == "inputs"
    
    def test_get_header_map(self, test_config_path):
        """Debe retornar el mapeo de headers correctamente."""
        config = ConfigLoader(test_config_path)
        header_map = config.get_header_map()
        
        assert "apellido" in header_map
        assert "nombre" in header_map
        assert "id" in header_map
        assert "nota" in header_map
        
        assert "Apellido(s)" in header_map["apellido"]
        assert "Nombre" in header_map["nombre"]
    
    def test_get_cantidad_tps(self, test_config_path):
        """Debe retornar la cantidad de TPs correctamente."""
        config = ConfigLoader(test_config_path)
        assert config.get_cantidad_tps() == 4
    
    def test_get_tp_prefix(self, test_config_path):
        """Debe retornar el prefijo de TP correctamente."""
        config = ConfigLoader(test_config_path)
        assert config.get_tp_prefix() == "TP"
    
    def test_get_cantidad_parciales(self, test_config_path):
        """Debe retornar la cantidad de parciales correctamente."""
        config = ConfigLoader(test_config_path)
        assert config.get_cantidad_parciales() == 2
    
    def test_get_cantidad_recuperatorios(self, test_config_path):
        """Debe retornar la cantidad de recuperatorios correctamente."""
        config = ConfigLoader(test_config_path)
        assert config.get_cantidad_recuperatorios() == 2
    
    def test_valores_por_defecto(self, temp_dir):
        """Debe usar valores por defecto cuando no están en el archivo."""
        # Crear config mínimo
        minimal_config = os.path.join(temp_dir, "minimal.ini")
        with open(minimal_config, 'w') as f:
            f.write("[Directorios]\n")
        
        config = ConfigLoader(minimal_config)
        
        # Verificar valores por defecto
        assert config.get_source_dir() == "inputs"
        assert config.get_output_dir() == "outputs"
        assert config.get_tp_prefix() == "TP"
        assert config.get_cantidad_tps() == 4

