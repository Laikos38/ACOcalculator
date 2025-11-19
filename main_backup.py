import os
import csv

SOURCE_DIR = "inputs"
OUTPUT_DIR = "outputs"
CALIFICATION_HEADER = "Calificación/10,00"

HEADER_MAP = {
    "apellido": ["Apellido(s)", "Apellidos", "Last Name"],
    "nombre": ["Nombre", "First Name"],
    "id": ["Número de ID", "ID"],
    "nota": [CALIFICATION_HEADER],
}

def get_col_name(fieldnames, posibles):
    """Devuelve el nombre real de la columna si existe en fieldnames"""
    for p in posibles:
        if p in fieldnames:
            return p
    raise KeyError(f"No se encontró ninguna de las columnas {posibles} en {fieldnames}")

def consolidar_archivos_multiples(base_name, curso):
    """
    Busca y consolida múltiples archivos de un mismo TP o Parcial.
    
    Por ejemplo, si hay Parcial1_1K2_1.csv y Parcial1_1K2_2.csv,
    los consolida en un solo archivo Parcial1_1K2_filtrado.csv tomando
    la mejor calificación de cada alumno entre todos los archivos.
    
    Args:
        base_name: Nombre base sin extensión (ej: "Parcial1_1K2", "TP1_1K4")
        curso: Código del curso (ej: "1K2", "1K4")
    
    Returns:
        bool: True si se encontraron y consolidaron archivos, False si no
    """
    import glob
    
    # Buscar todos los archivos que coincidan con el patrón
    pattern = os.path.join(SOURCE_DIR, f"{base_name}_*.csv")
    archivos_encontrados = glob.glob(pattern)
    
    # También buscar el archivo sin sufijo numérico
    archivo_base = os.path.join(SOURCE_DIR, f"{base_name}.csv")
    if os.path.exists(archivo_base):
        archivos_encontrados.append(archivo_base)
    
    if not archivos_encontrados:
        return False
    
    # Extraer el curso del base_name y crear el directorio de salida
    partes = base_name.split("_")
    if len(partes) >= 2:
        curso_dir = partes[-1]  # Último elemento es el curso
        output_curso_dir = os.path.join(OUTPUT_DIR, curso_dir)
    else:
        output_curso_dir = OUTPUT_DIR
    
    # Crear el directorio de salida al inicio
    os.makedirs(output_curso_dir, exist_ok=True)
    output_file = os.path.join(output_curso_dir, base_name + "_filtrado.csv")
    
    # Si solo hay un archivo, procesarlo normalmente
    if len(archivos_encontrados) == 1:
        archivo = archivos_encontrados[0]
        filtrar_mejor_calificacion(archivo, output_file)
        print(f"✅ Procesado: {os.path.basename(archivo)}")
        return True
    
    # Si hay múltiples archivos, consolidarlos
    print(f"📦 Encontrados {len(archivos_encontrados)} archivos para {base_name}")
    for archivo in archivos_encontrados:
        print(f"   - {os.path.basename(archivo)}")
    
    # Consolidar todos los archivos en un diccionario con la mejor nota por alumno
    best_attempts = {}
    fieldnames = None
    
    for archivo in archivos_encontrados:
        with open(archivo, newline='', encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if fieldnames is None:
                fieldnames = reader.fieldnames
            
            id_col = get_col_name(reader.fieldnames, HEADER_MAP["id"])
            nota_col = get_col_name(reader.fieldnames, HEADER_MAP["nota"])
            
            for row in reader:
                alumno_id = row[id_col]
                nota = float(row[nota_col].replace(",", "."))
                
                if alumno_id not in best_attempts:
                    best_attempts[alumno_id] = row
                else:
                    nota_actual = float(best_attempts[alumno_id][nota_col].replace(",", "."))
                    if nota > nota_actual:
                        best_attempts[alumno_id] = row
    
    # Guardar el archivo consolidado (el directorio ya fue creado al inicio)
    with open(output_file, "w", newline='', encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(best_attempts.values())
    
    print(f"✅ Consolidado en: {base_name}_filtrado.csv ({len(best_attempts)} alumnos)")
    return True

def convertir_nota_a_entero(nota_str):
    """
    Convierte una nota decimal a su equivalente entero según la escala de calificación.
    
    Las notas de Moodle vienen en escala 0-10, se multiplican por 10 para llevarlas
    a escala 0-100 y luego se aplica la conversión a escala entera (2-10).
    
    Escala de conversión (base 100):
    - 0 a 54.44 -> 2
    - 54.45 a 57.44 -> 4
    - 57.45 a 59.44 -> 5
    - 59.45 a 68.44 -> 6
    - 68.45 a 77.44 -> 7
    - 77.45 a 86.44 -> 8
    - 86.45 a 95.44 -> 9
    - 95.45 a 100 -> 10
    - Si está vacío o fuera de rango -> "FALTA"
    """
    if not nota_str or nota_str.strip() == "":
        return "FALTA"
    
    try:
        nota = float(nota_str)
    except ValueError:
        return "FALTA"
    
    # Convertir de escala 0-10 a escala 0-100
    nota_100 = nota * 10
    
    if 0 <= nota_100 <= 54.44:
        return 2
    elif 54.45 <= nota_100 <= 57.44:
        return 4
    elif 57.45 <= nota_100 <= 59.44:
        return 5
    elif 59.45 <= nota_100 <= 68.44:
        return 6
    elif 68.45 <= nota_100 <= 77.44:
        return 7
    elif 77.45 <= nota_100 <= 86.44:
        return 8
    elif 86.45 <= nota_100 <= 95.44:
        return 9
    elif 95.45 <= nota_100 <= 100:
        return 10
    else:
        return "FALTA"

def filtrar_mejor_calificacion(input_file, output_file):
    best_attempts = {}
    with open(input_file, newline='', encoding="utf-8-sig") as f:   # 👈 utf-8-sig
        reader = csv.DictReader(f)
        id_col = get_col_name(reader.fieldnames, HEADER_MAP["id"])
        nota_col = get_col_name(reader.fieldnames, HEADER_MAP["nota"])

        for row in reader:
            alumno_id = row[id_col]
            nota = float(row[nota_col].replace(",", "."))

            if alumno_id not in best_attempts:
                best_attempts[alumno_id] = row
            else:
                nota_actual = float(best_attempts[alumno_id][nota_col].replace(",", "."))
                if nota > nota_actual:
                    best_attempts[alumno_id] = row

    # Asegurar que el directorio de salida exista
    output_dir = os.path.dirname(output_file)
    if output_dir:  # Solo crear si hay un directorio en la ruta
        os.makedirs(output_dir, exist_ok=True)
    
    with open(output_file, "w", newline='', encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(best_attempts.values())

def mergear_tps(curso):
    archivos = {
        "TP1": f"TP1_{curso.upper()}",
        "TP2": f"TP2_{curso.upper()}",
        "TP3": f"TP3_{curso.upper()}",
        "TP4": f"TP4_{curso.upper()}",
    }

    datos = {}
    
    # Directorio de salida específico del curso
    output_curso_dir = os.path.join(OUTPUT_DIR, curso.upper())

    for tp, base_name in archivos.items():
        filtered_file = os.path.join(output_curso_dir, base_name + "_filtrado.csv")

        # Si no existe el filtrado, generarlo desde el/los source(s)
        if not os.path.exists(filtered_file):
            print(f"⚠️ No se encontró el archivo filtrado para {base_name}. Buscando archivos source...")
            if not consolidar_archivos_multiples(base_name, curso):
                print(f"⚠️ No se encontraron archivos source para {base_name}. Se ignorará este TP.")
                continue  # ignoramos este TP y continuamos con los demás

        # Leer el archivo filtrado (ya existente o recién generado)
        with open(filtered_file, newline='', encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            apellido_col = get_col_name(reader.fieldnames, HEADER_MAP["apellido"])
            nombre_col = get_col_name(reader.fieldnames, HEADER_MAP["nombre"])
            id_col = get_col_name(reader.fieldnames, HEADER_MAP["id"])
            nota_col = get_col_name(reader.fieldnames, HEADER_MAP["nota"])

            for row in reader:
                alumno_id = row[id_col]
                if alumno_id not in datos:
                    datos[alumno_id] = {
                        "Apellido(s)": row[apellido_col],
                        "Nombre": row[nombre_col],
                        "Número de ID": alumno_id,
                        "TP1": "",
                        "TP1_Nota": "",
                        "TP2": "",
                        "TP2_Nota": "",
                        "TP3": "",
                        "TP3_Nota": "",
                        "TP4": "",
                        "TP4_Nota": ""
                    }
                # Guardar la nota decimal
                nota_decimal = row[nota_col].replace(",", ".")
                datos[alumno_id][tp] = nota_decimal
                # Guardar la nota convertida a entero
                datos[alumno_id][f"{tp}_Nota"] = convertir_nota_a_entero(nota_decimal)

    if not datos:
        print("⚠️ No se pudo unificar los TPs porque no hay datos disponibles.")
        return

    os.makedirs(output_curso_dir, exist_ok=True)
    merge_file = os.path.join(output_curso_dir, f"TPs_{curso.upper()}_unificado.csv")
    with open(merge_file, "w", newline='', encoding="utf-8-sig") as f:
        fieldnames = [
            "Apellido(s)", "Nombre", "Número de ID", 
            "TP1", "TP1_Nota", 
            "TP2", "TP2_Nota", 
            "TP3", "TP3_Nota", 
            "TP4", "TP4_Nota"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(datos.values())

    print(f"✅ Unificación de TPs completada: {merge_file}")

def mergear_parciales(curso):
    archivos = {
        "Parcial1": f"Parcial1_{curso.upper()}",
        "Parcial2": f"Parcial2_{curso.upper()}",
        "Recuperatorio1": f"Recuperatorio1_{curso.upper()}",
        "Recuperatorio2": f"Recuperatorio2_{curso.upper()}",
    }

    datos = {}
    
    # Directorio de salida específico del curso
    output_curso_dir = os.path.join(OUTPUT_DIR, curso.upper())

    for parcial, base_name in archivos.items():
        filtered_file = os.path.join(output_curso_dir, base_name + "_filtrado.csv")

        # Si no existe el filtrado, generarlo desde el/los source(s)
        if not os.path.exists(filtered_file):
            print(f"⚠️ No se encontró el archivo filtrado para {base_name}. Buscando archivos source...")
            if not consolidar_archivos_multiples(base_name, curso):
                print(f"⚠️ No se encontraron archivos source para {base_name}. Se ignorará.")
                continue  # ignoramos este Parcial/Recuperatorio y continuamos con los demás

        # Leer el archivo filtrado (ya existente o recién generado)
        with open(filtered_file, newline='', encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            apellido_col = get_col_name(reader.fieldnames, HEADER_MAP["apellido"])
            nombre_col = get_col_name(reader.fieldnames, HEADER_MAP["nombre"])
            id_col = get_col_name(reader.fieldnames, HEADER_MAP["id"])
            nota_col = get_col_name(reader.fieldnames, HEADER_MAP["nota"])

            for row in reader:
                alumno_id = row[id_col]
                if alumno_id not in datos:
                    datos[alumno_id] = {
                        "Apellido(s)": row[apellido_col],
                        "Nombre": row[nombre_col],
                        "Número de ID": alumno_id,
                        "Parcial1": "",
                        "Parcial1_Nota": "",
                        "Parcial2": "",
                        "Parcial2_Nota": "",
                        "Recuperatorio1": "",
                        "Recuperatorio1_Nota": "",
                        "Recuperatorio2": "",
                        "Recuperatorio2_Nota": ""
                    }
                # Guardar la nota decimal
                nota_decimal = row[nota_col].replace(",", ".")
                datos[alumno_id][parcial] = nota_decimal
                # Guardar la nota convertida a entero
                datos[alumno_id][f"{parcial}_Nota"] = convertir_nota_a_entero(nota_decimal)

    if not datos:
        print("⚠️ No se pudo unificar los Parciales porque no hay datos disponibles.")
        return

    os.makedirs(output_curso_dir, exist_ok=True)
    merge_file = os.path.join(output_curso_dir, f"Parciales_{curso.upper()}_unificado.csv")
    with open(merge_file, "w", newline='', encoding="utf-8-sig") as f:
        fieldnames = [
            "Apellido(s)", "Nombre", "Número de ID", 
            "Parcial1", "Parcial1_Nota", 
            "Parcial2", "Parcial2_Nota",
            "Recuperatorio1", "Recuperatorio1_Nota",
            "Recuperatorio2", "Recuperatorio2_Nota"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(datos.values())

    print(f"✅ Unificación de Parciales completada: {merge_file}")

def generar_planilla_final(curso):
    """
    Genera una planilla final consolidada combinando TPs y Parciales en formato XLS.
    Incluye tanto las notas decimales de Moodle como las notas convertidas a enteros.
    """
    try:
        import xlwt
    except ImportError:
        print("❌ Error: Se requiere la librería 'xlwt' para generar archivos XLS.")
        print("   Instálala con: pip install xlwt")
        return
    
    # Directorio de salida específico del curso
    output_curso_dir = os.path.join(OUTPUT_DIR, curso.upper())
    
    # Archivos mergeados de TPs y Parciales
    tps_file = os.path.join(output_curso_dir, f"TPs_{curso.upper()}_unificado.csv")
    parciales_file = os.path.join(output_curso_dir, f"Parciales_{curso.upper()}_unificado.csv")
    
    # Verificar que existan los archivos mergeados
    if not os.path.exists(tps_file):
        print(f"⚠️ No se encontró el archivo de TPs unificado: {tps_file}")
        print(f"   Ejecuta primero la opción 2 (Unificar TPs) para el curso {curso.upper()}")
        generar = input("¿Quieres unificar los TPs ahora? (S/n) [S]: ").strip().lower()
        # Por defecto es 's' si no se ingresa nada
        if generar == '' or generar == 's':
            mergear_tps(curso)
            if not os.path.exists(tps_file):
                print("❌ No se pudo unificar los TPs. Abortando.")
                return
        else:
            return
    
    if not os.path.exists(parciales_file):
        print(f"⚠️ No se encontró el archivo de Parciales unificado: {parciales_file}")
        print(f"   Ejecuta primero la opción 3 (Unificar Parciales) para el curso {curso.upper()}")
        generar = input("¿Quieres unificar los Parciales ahora? (S/n) [S]: ").strip().lower()
        # Por defecto es 's' si no se ingresa nada
        if generar == '' or generar == 's':
            mergear_parciales(curso)
            if not os.path.exists(parciales_file):
                print("❌ No se pudo unificar los Parciales. Abortando.")
                return
        else:
            return
    
    # Leer datos de TPs
    datos_tps = {}
    with open(tps_file, newline='', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            alumno_id = row["Número de ID"]
            datos_tps[alumno_id] = row
    
    # Leer datos de Parciales
    datos_parciales = {}
    with open(parciales_file, newline='', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            alumno_id = row["Número de ID"]
            datos_parciales[alumno_id] = row
    
    # Combinar todos los IDs únicos
    todos_ids = set(datos_tps.keys()) | set(datos_parciales.keys())
    
    if not todos_ids:
        print("⚠️ No hay datos para generar la planilla final.")
        return
    
    # Crear libro de Excel
    wb = xlwt.Workbook()
    ws = wb.add_sheet(f'Notas {curso.upper()}')
    
    # Estilo para el encabezado
    header_style = xlwt.easyxf('font: bold on; align: horiz center')
    
    # Definir columnas
    columnas = [
        "Apellido(s)", "Nombre", "Número de ID",
        "TP1", "TP1_Nota", "TP2", "TP2_Nota", "TP3", "TP3_Nota", "TP4", "TP4_Nota",
        "Parcial1", "Parcial1_Nota", "Parcial2", "Parcial2_Nota",
        "Recuperatorio1", "Recuperatorio1_Nota", "Recuperatorio2", "Recuperatorio2_Nota"
    ]
    
    # Escribir encabezados
    for col, columna in enumerate(columnas):
        ws.write(0, col, columna, header_style)
    
    # Escribir datos
    fila = 1
    for alumno_id in sorted(todos_ids):
        # Obtener datos de TPs (si existen)
        tp_data = datos_tps.get(alumno_id, {})
        # Obtener datos de Parciales (si existen)
        parcial_data = datos_parciales.get(alumno_id, {})
        
        # Obtener información básica (priorizar TPs, luego Parciales)
        apellido = tp_data.get("Apellido(s)", parcial_data.get("Apellido(s)", ""))
        nombre = tp_data.get("Nombre", parcial_data.get("Nombre", ""))
        
        # Escribir fila
        ws.write(fila, 0, apellido)
        ws.write(fila, 1, nombre)
        ws.write(fila, 2, alumno_id)
        
        # TPs
        ws.write(fila, 3, tp_data.get("TP1", ""))
        ws.write(fila, 4, tp_data.get("TP1_Nota", ""))
        ws.write(fila, 5, tp_data.get("TP2", ""))
        ws.write(fila, 6, tp_data.get("TP2_Nota", ""))
        ws.write(fila, 7, tp_data.get("TP3", ""))
        ws.write(fila, 8, tp_data.get("TP3_Nota", ""))
        ws.write(fila, 9, tp_data.get("TP4", ""))
        ws.write(fila, 10, tp_data.get("TP4_Nota", ""))
        
        # Parciales y Recuperatorios
        ws.write(fila, 11, parcial_data.get("Parcial1", ""))
        ws.write(fila, 12, parcial_data.get("Parcial1_Nota", ""))
        ws.write(fila, 13, parcial_data.get("Parcial2", ""))
        ws.write(fila, 14, parcial_data.get("Parcial2_Nota", ""))
        ws.write(fila, 15, parcial_data.get("Recuperatorio1", ""))
        ws.write(fila, 16, parcial_data.get("Recuperatorio1_Nota", ""))
        ws.write(fila, 17, parcial_data.get("Recuperatorio2", ""))
        ws.write(fila, 18, parcial_data.get("Recuperatorio2_Nota", ""))
        
        fila += 1
    
    # Guardar archivo
    os.makedirs(output_curso_dir, exist_ok=True)
    output_file = os.path.join(output_curso_dir, f"Planilla_Final_{curso.upper()}.xls")
    wb.save(output_file)
    
    print(f"✅ Planilla final generada: {output_file}")
    print(f"   Total de alumnos: {len(todos_ids)}")


def menu():
    while True:
        print("\n=== MENÚ ===")
        print("1) Filtrar mejor calificación por alumno")
        print("2) Unificar TPs")
        print("3) Unificar Parciales")
        print("4) Generar Planilla Final (XLS)")
        print("q) Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            try:
                archivos = [f for f in os.listdir(SOURCE_DIR) if f.endswith(".csv")]
            except FileNotFoundError:
                print(f"❌ No existe el directorio '{SOURCE_DIR}'")
                continue

            if not archivos:
                print("⚠️ No hay archivos CSV en la carpeta 'source'")
                continue

            print("\nArchivos disponibles:")
            for i, archivo in enumerate(archivos, start=1):
                print(f"{i}) {archivo}")

            seleccion = input("Selecciona el número del archivo: ").strip()
            if not seleccion.isdigit() or int(seleccion) not in range(1, len(archivos)+1):
                print("❌ Selección inválida")
                continue

            archivo_elegido = archivos[int(seleccion)-1]
            input_path = os.path.join(SOURCE_DIR, archivo_elegido)
            
            # Intentar detectar el curso del nombre del archivo (ej: TP1_1K2.csv -> 1K2)
            nombre_sin_ext = archivo_elegido.replace(".csv", "")
            partes = nombre_sin_ext.split("_")
            if len(partes) >= 2:
                curso_detectado = partes[-1]  # Último elemento debería ser el curso
                # Remover sufijos numéricos si los hay (ej: 1K2_1 -> 1K2)
                if curso_detectado[-1].isdigit() and len(curso_detectado) > 1:
                    curso_detectado = "_".join(partes[:-1])
                    if "_" in curso_detectado:
                        curso_detectado = curso_detectado.split("_")[-1]
                output_curso_dir = os.path.join(OUTPUT_DIR, curso_detectado.upper())
            else:
                output_curso_dir = OUTPUT_DIR
            
            os.makedirs(output_curso_dir, exist_ok=True)
            output_path = os.path.join(output_curso_dir, archivo_elegido.replace(".csv", "_filtrado.csv"))

            filtrar_mejor_calificacion(input_path, output_path)
            print(f"✅ Archivo procesado y guardado en '{output_path}'")

        elif opcion == "2":
            curso = input("Ingrese el curso (ej: 1K4, 1K2): ").strip()
            if curso:
                mergear_tps(curso)
            else:
                print("❌ Curso inválido")

        elif opcion == "3":
            curso = input("Ingrese el curso (ej: 1K4, 1K2): ").strip()
            if curso:
                mergear_parciales(curso)
            else:
                print("❌ Curso inválido")

        elif opcion == "4":
            curso = input("Ingrese el curso (ej: 1K4, 1K2): ").strip()
            if curso:
                generar_planilla_final(curso)
            else:
                print("❌ Curso inválido")

        elif opcion.lower() == "q":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    menu()

