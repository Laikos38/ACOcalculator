#!/usr/bin/env python3
"""
Sistema de Gestión de Calificaciones de Moodle - Versión 1.0
=============================================================

Sistema automatizado para gestionar y procesar las calificaciones de trabajos 
prácticos (TPs), parciales y recuperatorios de estudiantes, diseñado para 
trabajar con exportaciones CSV de Moodle.

Características principales:
- Filtrado de mejores calificaciones por alumno
- Consolidación de múltiples intentos
- Seguimiento de cantidad de intentos por TP
- Fusión de TPs por curso
- Fusión de Parciales y Recuperatorios por curso
- Generación de planillas finales consolidadas en formato XLS

Autor: Sistema ACOCalculator
Versión: 1.0
"""

import os
import sys
import webbrowser
from src import ConfigLoader, TPManager, ParcialManager, ReportGenerator


def get_binary_directory():
    """
    Obtiene el directorio donde se encuentra el ejecutable.
    
    Returns:
        str: Ruta absoluta al directorio del ejecutable
    """
    if getattr(sys, 'frozen', False):
        # Si está ejecutando como binario empaquetado (PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # Si está ejecutando como script Python normal
        return os.path.dirname(os.path.abspath(__file__))


def ensure_directories(config):
    """
    Asegura que existan los directorios necesarios en el mismo directorio del binario.
    
    Args:
        config: Instancia de ConfigLoader con la configuración
    """
    # Obtener directorio del binario
    binary_dir = get_binary_directory()
    
    # Cambiar al directorio del binario
    os.chdir(binary_dir)
    
    input_dir = config.get_source_dir()
    output_dir = config.get_output_dir()
    
    # Construir rutas completas relativas al binario
    input_path = os.path.join(binary_dir, input_dir)
    output_path = os.path.join(binary_dir, output_dir)
    
    # Mostrar ubicación del binario
    print(f"📁 Ubicación del ejecutable: {binary_dir}")
    print("")
    
    # Crear directorios si no existen
    created = False
    if not os.path.exists(input_path):
        os.makedirs(input_path, exist_ok=True)
        print(f"✅ Directorio de entrada creado: {input_dir}/")
        created = True
    
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
        print(f"✅ Directorio de salida creado: {output_dir}/")
        created = True
    
    if not created:
        print(f"✅ Usando directorios existentes:")
        print(f"   • Entrada: {input_dir}/")
        print(f"   • Salida: {output_dir}/")


def menu():
    """
    Muestra el menú principal y maneja la interacción con el usuario.
    """
    # Cargar configuración (con fallback a configuración por defecto)
    config = ConfigLoader("config.ini")
    
    # Asegurar que existen los directorios necesarios
    ensure_directories(config)
    print("")
    
    # Inicializar managers
    tp_manager = TPManager(config)
    exam_manager = ParcialManager(config)
    report_generator = ReportGenerator(config)
    
    # Obtener directorios de configuración
    source_dir = config.get_source_dir()
    
    while True:
        print("\n" + "="*60)
        print(" SISTEMA DE GESTIÓN DE CALIFICACIONES - MOODLE")
        print("="*60)
        print("1) Filtrar mejor calificación por alumno")
        print("2) Mergear TPs (incluye seguimiento de intentos)")
        print("3) Mergear Parciales y Recuperatorios")
        print("4) Generar Planilla Final (XLS)")
        print("h) Ayuda - Abrir manual de usuario")
        print("q) Salir")
        print("="*60)
        option = input("Selecciona una opción: ").strip()
        
        if option == "1":
            try:
                files = [f for f in os.listdir(source_dir) if f.endswith(".csv")]
            except FileNotFoundError:
                print(f"❌ No existe el directorio '{source_dir}'")
                continue
            
            if not files:
                print(f"⚠️ No hay archivos CSV en la carpeta '{source_dir}'")
                continue
            
            print("\n" + "-"*60)
            print("Archivos disponibles:")
            print("-"*60)
            for i, file in enumerate(files, start=1):
                print(f"{i}) {file}")
            print("-"*60)
            
            selection = input("Selecciona el número del archivo: ").strip()
            if not selection.isdigit() or int(selection) not in range(1, len(files)+1):
                print("❌ Selección inválida")
                continue
            
            selected_file = files[int(selection)-1]
            
            # Detectar el tipo de archivo (TP o Parcial/Recuperatorio)
            if selected_file.upper().startswith("TP"):
                tp_manager.filter_best_grade(selected_file)
            else:
                exam_manager.filter_best_grade(selected_file)
        
        elif option == "2":
            print("\n" + "-"*60)
            course = input("Ingrese el curso (ej: 1K4, 1K2): ").strip()
            print("-"*60)
            if course:
                print(f"\n🔄 Procesando TPs para el curso {course.upper()}...")
                tp_manager.merge_tps(course)
            else:
                print("❌ Curso inválido")
        
        elif option == "3":
            print("\n" + "-"*60)
            course = input("Ingrese el curso (ej: 1K4, 1K2): ").strip()
            print("-"*60)
            if course:
                print(f"\n🔄 Procesando Parciales para el curso {course.upper()}...")
                exam_manager.merge_exams(course)
            else:
                print("❌ Curso inválido")
        
        elif option == "4":
            print("\n" + "-"*60)
            course = input("Ingrese el curso (ej: 1K4, 1K2): ").strip()
            print("-"*60)
            if course:
                print(f"\n📊 Generando planilla final para el curso {course.upper()}...")
                report_generator.generate_final_report(course, tp_manager, exam_manager)
            else:
                print("❌ Curso inválido")
        
        elif option.lower() == "h":
            print("\n" + "="*60)
            print("📖 Abriendo manual de usuario en el navegador...")
            print("="*60)
            try:
                webbrowser.open("https://github.com/Laikos38/ACOcalculator#readme")
                print("✅ Manual abierto en el navegador")
            except Exception as e:
                print(f"❌ Error al abrir el navegador: {e}")
                print("📝 Puedes acceder manualmente a:")
                print("   https://github.com/Laikos38/ACOcalculator#readme")
        
        elif option.lower() == "q":
            print("\n" + "="*60)
            print("👋 Gracias por usar el Sistema de Gestión de Calificaciones")
            print("="*60)
            break
        else:
            print("❌ Opción no válida. Por favor, selecciona una opción del menú.")


def main():
    """
    Función principal del programa.
    """
    print("\n" + "="*60)
    print(" BIENVENIDO AL SISTEMA DE GESTIÓN DE CALIFICACIONES")
    print(" Versión 1.0 - Modular y Profesional")
    print("="*60)
    print("")
    
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\n⚠️ Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
