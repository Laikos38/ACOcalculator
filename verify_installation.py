#!/usr/bin/env python3
"""
Script de verificación de instalación para ACOCalculator v1.0
Verifica que todos los módulos y dependencias estén correctamente instalados.
"""

import sys
import os


def print_header(text):
    """Imprime un encabezado formateado."""
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)


def print_status(check, status, message=""):
    """Imprime el estado de una verificación."""
    icon = "✅" if status else "❌"
    print(f"{icon} {check:<40} {message}")
    return status


def verify_python_version():
    """Verifica la versión de Python."""
    version = sys.version_info
    required = (3, 6)
    
    if version >= required:
        print_status("Versión de Python", True, f"v{version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_status("Versión de Python", False, 
                    f"Requiere Python 3.6+, tienes {version.major}.{version.minor}")
        return False


def verify_config_file():
    """Verifica que existe el archivo de configuración."""
    exists = os.path.exists("config.ini")
    print_status("Archivo config.ini", exists)
    return exists


def verify_directories():
    """Verifica que existen los directorios necesarios."""
    results = []
    
    # Directorio src
    results.append(print_status("Directorio src/", os.path.exists("src")))
    results.append(print_status("Directorio src/utils/", os.path.exists("src/utils")))
    results.append(print_status("Directorio src/managers/", os.path.exists("src/managers")))
    results.append(print_status("Directorio src/generators/", os.path.exists("src/generators")))
    
    # Directorios de datos
    results.append(print_status("Directorio inputs/", os.path.exists("inputs")))
    results.append(print_status("Directorio outputs/", os.path.exists("outputs")))
    
    return all(results)


def verify_modules():
    """Verifica que todos los módulos están presentes."""
    modules = [
        "src/__init__.py",
        "src/utils/__init__.py",
        "src/utils/config_loader.py",
        "src/utils/csv_helpers.py",
        "src/utils/file_consolidator.py",
        "src/managers/__init__.py",
        "src/managers/tp_manager.py",
        "src/managers/parcial_manager.py",
        "src/generators/__init__.py",
        "src/generators/report_generator.py",
    ]
    
    results = []
    for module in modules:
        name = module.replace("src/", "").replace("__init__.py", "(package)")
        results.append(print_status(name, os.path.exists(module)))
    
    return all(results)


def verify_imports():
    """Verifica que los módulos se pueden importar correctamente."""
    results = []
    
    try:
        from src import ConfigLoader
        results.append(print_status("Import ConfigLoader", True))
    except Exception as e:
        results.append(print_status("Import ConfigLoader", False, str(e)))
    
    try:
        from src import TPManager
        results.append(print_status("Import TPManager", True))
    except Exception as e:
        results.append(print_status("Import TPManager", False, str(e)))
    
    try:
        from src import ParcialManager
        results.append(print_status("Import ParcialManager", True))
    except Exception as e:
        results.append(print_status("Import ParcialManager", False, str(e)))
    
    try:
        from src import ReportGenerator
        results.append(print_status("Import ReportGenerator", True))
    except Exception as e:
        results.append(print_status("Import ReportGenerator", False, str(e)))
    
    return all(results)


def verify_dependencies():
    """Verifica las dependencias externas."""
    results = []
    
    try:
        import xlwt
        results.append(print_status("Librería xlwt", True, f"v{xlwt.__VERSION__}"))
    except ImportError:
        results.append(print_status("Librería xlwt", False, "pip install xlwt"))
    
    return all(results)


def verify_config_validity():
    """Verifica que el archivo de configuración es válido."""
    try:
        from src import ConfigLoader
        config = ConfigLoader("config.ini")
        
        results = []
        results.append(print_status("Directorio source", True, config.get_source_dir()))
        results.append(print_status("Directorio output", True, config.get_output_dir()))
        results.append(print_status("Cantidad de TPs", True, str(config.get_cantidad_tps())))
        results.append(print_status("Cantidad de Parciales", True, str(config.get_cantidad_parciales())))
        
        return all(results)
    except Exception as e:
        print_status("Validación de config.ini", False, str(e))
        return False


def main():
    """Función principal."""
    print_header("VERIFICACIÓN DE INSTALACIÓN - ACOCalculator v1.0")
    
    all_checks = []
    
    print_header("1. Requisitos del Sistema")
    all_checks.append(verify_python_version())
    
    print_header("2. Archivos de Configuración")
    all_checks.append(verify_config_file())
    
    print_header("3. Estructura de Directorios")
    all_checks.append(verify_directories())
    
    print_header("4. Módulos del Sistema")
    all_checks.append(verify_modules())
    
    print_header("5. Importación de Módulos")
    all_checks.append(verify_imports())
    
    print_header("6. Dependencias Externas")
    all_checks.append(verify_dependencies())
    
    print_header("7. Validación de Configuración")
    all_checks.append(verify_config_validity())
    
    # Resumen final
    print_header("RESUMEN")
    
    if all(all_checks):
        print("\n✅ ¡Todas las verificaciones pasaron exitosamente!")
        print("   El sistema está correctamente instalado y listo para usar.")
        print("\n   Ejecuta: python3 main.py")
        return 0
    else:
        print("\n❌ Algunas verificaciones fallaron.")
        print("   Revisa los errores arriba y corrígelos antes de usar el sistema.")
        print("\n   Consulta QUICK_START.md para más información.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

