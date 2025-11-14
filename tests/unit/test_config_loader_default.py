"""
Tests para la configuración por defecto de ConfigLoader.
"""
import pytest
import os
from src.utils.config_loader import ConfigLoader


@pytest.mark.unit
class TestConfigLoaderDefault:
    """Tests para la configuración por defecto."""
    
    def test_carga_config_por_defecto_si_no_existe_archivo(self, temp_dir):
        """Debe usar configuración por defecto si no existe el archivo."""
        os.chdir(temp_dir)
        config_path = os.path.join(temp_dir, "no_existe.ini")
        
        # No debe lanzar excepción
        config = ConfigLoader(config_path)
        
        assert config.is_using_default() == True
        assert config.get_source_dir() == "inputs"
        assert config.get_output_dir() == "outputs"
    
    def test_crea_archivo_config_por_defecto(self, temp_dir):
        """Debe crear un archivo config.ini por defecto."""
        os.chdir(temp_dir)
        config_path = os.path.join(temp_dir, "auto_generated.ini")
        
        config = ConfigLoader(config_path)
        
        # Verificar que se creó el archivo
        assert os.path.exists(config_path)
        
        # Verificar que tiene contenido válido
        with open(config_path, 'r') as f:
            content = f.read()
        
        assert "[Directorios]" in content
        assert "source_dir" in content
        assert "[TrabajoPractico]" in content
    
    def test_prioridad_config_externo_sobre_default(self, temp_dir):
        """Debe dar prioridad al config externo sobre el default."""
        os.chdir(temp_dir)
        config_path = os.path.join(temp_dir, "custom.ini")
        
        # Crear config personalizado
        custom_config = """[Directorios]
source_dir = mis_inputs
output_dir = mis_outputs

[TrabajoPractico]
cantidad_tps = 6
tp_prefix = TRABAJO
"""
        with open(config_path, 'w') as f:
            f.write(custom_config)
        
        config = ConfigLoader(config_path)
        
        # Debe usar valores personalizados
        assert config.is_using_default() == False
        assert config.get_source_dir() == "mis_inputs"
        assert config.get_output_dir() == "mis_outputs"
        assert config.get_cantidad_tps() == 6
        assert config.get_tp_prefix() == "TRABAJO"
    
    def test_config_parcial_usa_defaults_para_faltantes(self, temp_dir):
        """Debe usar defaults para valores no definidos en config parcial."""
        os.chdir(temp_dir)
        config_path = os.path.join(temp_dir, "partial.ini")
        
        # Config que solo define algunos valores
        partial_config = """[Directorios]
source_dir = custom_inputs
"""
        with open(config_path, 'w') as f:
            f.write(partial_config)
        
        config = ConfigLoader(config_path)
        
        # Valor personalizado
        assert config.get_source_dir() == "custom_inputs"
        
        # Valores por defecto
        assert config.get_output_dir() == "outputs"
        assert config.get_cantidad_tps() == 4
        assert config.get_tp_prefix() == "TP"
    
    def test_default_config_tiene_todas_las_secciones(self):
        """Debe verificar que DEFAULT_CONFIG tiene todas las secciones necesarias."""
        config_content = ConfigLoader.DEFAULT_CONFIG
        
        # Verificar secciones
        assert "[Directorios]" in config_content
        assert "[Headers]" in config_content
        assert "[TrabajoPractico]" in config_content
        assert "[Parciales]" in config_content
        assert "[Formatos]" in config_content
        
        # Verificar valores clave
        assert "source_dir" in config_content
        assert "cantidad_tps" in config_content
        assert "cantidad_parciales" in config_content

