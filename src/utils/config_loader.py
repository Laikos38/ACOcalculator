"""
Módulo para cargar y gestionar la configuración del sistema.
"""
import configparser
import os
from io import StringIO


class ConfigLoader:
    """Clase para cargar y proporcionar acceso a la configuración del sistema."""
    
    # Configuración por defecto embebida
    DEFAULT_CONFIG = """[Directorios]
source_dir = inputs
output_dir = outputs

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
    
    def __init__(self, config_path="config.ini"):
        """
        Inicializa el cargador de configuración.
        
        Prioridad de configuración:
        1. Archivo config.ini externo (si existe)
        2. Configuración por defecto embebida
        
        Args:
            config_path: Ruta al archivo de configuración externo
        """
        self.config = configparser.ConfigParser()
        self.config_path = config_path
        self.using_default = False
        
        # Primero cargar configuración por defecto
        self.config.read_string(self.DEFAULT_CONFIG)
        
        # Intentar cargar archivo externo (tiene prioridad)
        if os.path.exists(config_path):
            print(f"✅ Usando configuración personalizada: {config_path}")
            self.config.read(config_path, encoding='utf-8')
        else:
            print(f"ℹ️  No se encontró {config_path}, usando configuración por defecto")
            self.using_default = True
            self._create_default_config_file(config_path)
    
    def get_source_dir(self):
        """Retorna el directorio de entrada."""
        return self.config.get('Directorios', 'source_dir', fallback='inputs')
    
    def get_output_dir(self):
        """Retorna el directorio de salida."""
        return self.config.get('Directorios', 'output_dir', fallback='outputs')
    
    def get_calification_header(self):
        """Retorna el encabezado de calificación."""
        return self.config.get('Headers', 'calification_header', fallback='Calificación/10,00')
    
    def get_header_map(self):
        """Retorna el mapeo de encabezados con soporte para múltiples formatos de calificación."""
        return {
            "apellido": [s.strip() for s in self.config.get('Headers', 'header_apellido').split(',')],
            "nombre": [s.strip() for s in self.config.get('Headers', 'header_nombre').split(',')],
            "id": [s.strip() for s in self.config.get('Headers', 'header_id').split(',')],
            # Soportar múltiples formatos de calificación (escala 0-10 y 0-100)
            "nota": ["Calificación/10,00", "Calificación/100,00", "Calificación/10.00", "Calificación/100.00"],
        }
    
    def get_cantidad_tps(self):
        """Retorna la cantidad de TPs a procesar."""
        return self.config.getint('TrabajoPractico', 'cantidad_tps', fallback=4)
    
    def get_tp_prefix(self):
        """Retorna el prefijo para archivos de TPs."""
        return self.config.get('TrabajoPractico', 'tp_prefix', fallback='TP')
    
    def get_cantidad_parciales(self):
        """Retorna la cantidad de parciales."""
        return self.config.getint('Parciales', 'cantidad_parciales', fallback=2)
    
    def get_cantidad_recuperatorios(self):
        """Retorna la cantidad de recuperatorios."""
        return self.config.getint('Parciales', 'cantidad_recuperatorios', fallback=2)
    
    def get_parcial_prefix(self):
        """Retorna el prefijo para archivos de parciales."""
        return self.config.get('Parciales', 'parcial_prefix', fallback='Parcial')
    
    def get_recuperatorio_prefix(self):
        """Retorna el prefijo para archivos de recuperatorios."""
        return self.config.get('Parciales', 'recuperatorio_prefix', fallback='Recuperatorio')
    
    def get_csv_encoding(self):
        """Retorna el encoding para archivos CSV."""
        return self.config.get('Formatos', 'csv_encoding', fallback='utf-8-sig')
    
    def get_output_format(self):
        """Retorna el formato de salida para planillas finales."""
        return self.config.get('Formatos', 'output_format', fallback='xls')
    
    def _create_default_config_file(self, config_path):
        """
        Crea un archivo de configuración por defecto para referencia del usuario.
        
        Args:
            config_path: Ruta donde crear el archivo
        """
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(self.DEFAULT_CONFIG)
            print(f"✅ Archivo de configuración creado: {config_path}")
            print(f"   Puedes editarlo para personalizar el comportamiento del sistema.")
        except Exception as e:
            # Si no se puede escribir, no es crítico, usamos la config por defecto
            print(f"⚠️  No se pudo crear {config_path}: {e}")
            print(f"   Continuando con configuración por defecto.")
    
    def is_using_default(self):
        """Retorna True si se está usando la configuración por defecto."""
        return self.using_default

