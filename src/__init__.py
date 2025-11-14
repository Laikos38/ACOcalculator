"""
Sistema de Gestión de Calificaciones de Moodle.
Procesamiento automatizado de trabajos prácticos, parciales y recuperatorios.
"""
from .utils import ConfigLoader
from .managers import TPManager, ParcialManager
from .generators import ReportGenerator

__all__ = ['ConfigLoader', 'TPManager', 'ParcialManager', 'ReportGenerator']
__version__ = '1.0.0'

