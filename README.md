# Sistema de Gestión de Calificaciones de Moodle

## 📖 Manual de Usuario - Versión 1.0

> **Para usuarios:** Esta es la guía simplificada para usar el sistema.  
> **Para desarrolladores:** Ver documentación técnica en [docs/](docs/)

---

## 🎯 ¿Qué hace este programa?

Este sistema te ayuda a procesar las calificaciones de Moodle de forma automática:

✅ **Filtra duplicados** - Si un alumno hizo varias veces un TP, se queda con la mejor nota  
✅ **Consolida notas** - Junta todos los TPs y Parciales en un solo archivo  
✅ **Cuenta intentos** - Te dice cuántas veces intentó un TP cada alumno 
✅ **Genera reporte final** - Crea una planilla Excel con toda la información  

---

## 🚀 Inicio Rápido

### Usar el Ejecutable

1. Descarga el ejecutable que corresponda según tu SO desde [Releases](https://github.com/Laikos38/ACOcalculator/releases)
2. Doble click para ejecutar
3. ¡Listo! El programa crea las carpetas necesarias automáticamente

---

## 📂 Preparar tus archivos

### Paso 1: Exportar desde Moodle

1. Entra a tu curso en Moodle
2. Ve al TP, parcial o recuperatorio que desees procesar, luego click en "Intentos" 
3. Selecciona formato **CSV** y modifica el tamaño de la página para que incluya todos los intentos
4. Exporta/descarga el archivo

### Paso 2: Organizar archivos

El programa crea dos carpetas automáticamente:

```
📁 inputs/     ← Aquí dentro debes mover los archivos CSV descargados de Moodle
📁 outputs/    ← Aquí aparecen los resultados procesados
```

**Importante:** Los nombres de los archivos dentro de `inputs/` deben seguir el siguiente formato:

**Trabajos Prácticos:**
- `TP1_1K2.csv`, `TP2_1K4.csv`, etc.

**Parciales y Recuperatorios (formato simple):**
- `Parcial1_1K2.csv`, `Parcial2_1K4.csv`
- `Recuperatorio1_1K2.csv`, `Recuperatorio2_1K4.csv`

**Parciales y Recuperatorios (múltiples archivos):**

Si hubo varios turnos para un parcial o recuperatorio, se debe agregar un sufijo numérico de la siguiente forma:
- `Parcial1_1K2_1.csv`, `Parcial1_1K2_2.csv`, `Parcial1_1K2_3.csv`
- `Recuperatorio1_1K4_1.csv`, `Recuperatorio1_1K4_2.csv`

> **✨ FLEXIBILIDAD EN NOMENCLATURA:** El sistema acepta **mayúsculas y minúsculas** indistintamente. Todos estos formatos son válidos:
> - ✅ `TP1_1K15.csv` (mayúsculas)
> - ✅ `tp1_1k15.csv` (minúsculas)
> - ✅ `Tp1_1K15.csv` (capitalizado)
> - ✅ `parcial1_1k2.csv` (minúsculas)
> - ✅ `RECUPERATORIO1_1K4.csv` (mayúsculas)
>
> El sistema **automáticamente detecta y normaliza** todos estos formatos, garantizando consistencia en los archivos de salida.

> Si tienes múltiples archivos del mismo parcial (ej: `Parcial1_1K2_1.csv` y `Parcial1_1K2_2.csv`), el programa automáticamente los **consolida** tomando la mejor nota de cada alumno entre todos los archivos.

Si faltara algún archivo durante el procesamiento, el sistema mostrará un mensaje advirtiendo la situación.

---

## 🎮 Cómo Usar el Sistema

### Menú Principal

Cuando ejecutas el programa, verás este menú:

```
============================================================
 SISTEMA DE GESTIÓN DE CALIFICACIONES - MOODLE
============================================================
1) Generar planilla de notas (XLS)
2) Operaciones intermedias
h) Ayuda - Abrir manual de usuario
q) Salir
============================================================
```

### Opción 1: Generar Planilla de Notas (XLS)

**¿Qué hace?**  
Crea un archivo Excel (`.xls`) con **TODAS** las notas juntas:
- Notas de todos los TPs (mejor intento por alumno)
- Notas de todos los Parciales
- Notas de todos los Recuperatorios

**Pasos:**
1. Selecciona opción `1`
2. Escribe el código del curso (ej: `1K2 o 1k2`)
3. Se crea la planilla en `outputs/1K2/Planilla_Final_1K2.xls`

**📊 Este archivo incluye:**
- Datos del alumno (Apellido, Nombre, ID)
- Nota decimal de Moodle (ej: 8.5)
- Nota entera convertida (ej: 9)
- Cantidad de intentos por TP

### Opción 2: Operaciones Intermedias

**¿Qué hace?**  
Abre un submenú con operaciones de procesamiento individual para usuarios avanzados.

**Submenú de Operaciones Intermedias:**

```
============================================================
 OPERACIONES INTERMEDIAS
============================================================
1) Filtrar mejor calificación por alumno
2) Unificar TPs
3) Unificar Parciales y Recuperatorios
v) Volver al menú principal
============================================================
```

#### Sub-opción 1: Filtrar mejor calificación

**¿Qué hace?**  
Si un alumno entregó varias veces el mismo TP, esta opción se queda solo con el intento de mejor nota.

**Pasos:**
1. Selecciona sub-opción `1`
2. Elige el archivo CSV de la lista
3. El resultado se guarda en `outputs/CURSO/archivo_filtrado.csv`

#### Sub-opción 2: Unificar TPs

**¿Qué hace?**  
Junta todos los TPs de un curso en UN SOLO archivo.

**Pasos:**
1. Selecciona sub-opción `2`
2. Escribe el código del curso (ej: `1K2`)
3. Se crea `outputs/1K2/TPs_1K2_unificado.csv`

**📊 El archivo incluye:**
- Apellido y Nombre del alumno
- Calificación de Moodle
- Cantidad de intentos por TP
- Calificación según la escala de la cátedra

#### Sub-opción 3: Unificar Parciales

**¿Qué hace?**  
Igual que la sub-opción 2, pero para Parciales y Recuperatorios.

**Pasos:**
1. Selecciona sub-opción `3`
2. Escribe el código del curso
3. Se crea `outputs/1K2/Parciales_1K2_unificado.csv`

### Opción h: Ayuda

Abre este manual en tu navegador web.

### Opción q: Salir

Cierra el programa.

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Generar Planilla Final (Caso más común)

```
1. Ejecutar programa

2. Mover a la carpeta inputs/:
   📄 TP1_1K2.csv
   📄 TP2_1K2.csv
   📄 TP3_1K2.csv
   📄 TP4_1K2.csv
   📄 Parcial1_1K2.csv
   📄 Parcial2_1K2.csv
   📄 Recuperatorio1_1K2.csv

3. Seleccionar opción 1 → Generar planilla de notas (XLS)
   → Escribir: 1K2

4. ¡Listo! Resultado en:
   outputs/1K2/Planilla_Final_1K2.xls
```

### Ejemplo 2: Procesar TPs individualmente (Operaciones Intermedias)

```
1. Ejecutar programa

2. Poner en inputs/:
   - TP1_1K2.csv
   - TP2_1K2.csv
   - TP3_1K2.csv
   - TP4_1K2.csv

3. Seleccionar opción 2 → Operaciones intermedias
   → Seleccionar sub-opción 2 → Unificar TPs
   → Escribir: 1K2

4. ¡Listo! Resultado en:
   outputs/1K2/TPs_1K2_unificado.csv
```

---

## ❓ Preguntas Frecuentes

### ¿Por qué mis archivos no aparecen?

**Verifica:**
- ✅ Que los archivos de moodle están en la carpeta `inputs/`
- ✅ Que los archivos terminan en `.csv`
- ✅ Que el nombre incluye el código del curso (ej: `_1K2`)

### ¿Qué significa "filtrado"?

Significa que se eliminaron los intentos repetidos, quedándose solo con la mejor nota de cada alumno.

### ¿Puedo procesar varios cursos?

¡Sí! El programa organiza automáticamente cada curso en su propia carpeta:
```
outputs/
├── 1K2/
│   ├── TPs_1K2_unificado.csv
│   └── Planilla_Final_1K2.xls
└── 1K4/
    ├── TPs_1K4_unificado.csv
    └── Planilla_Final_1K4.xls
```

### ¿Cómo sé cuántos intentos hizo un alumno?

En el archivo unificado de TPs, verás columnas como:
- `TP1_Intentos` → Cantidad de veces que entregó el TP1
- `TP2_Intentos` → Cantidad de veces que entregó el TP2

### ¿Qué pasa si un alumno no entregó un TP?

Aparecerá como "Falta" en la planilla.

### ¿El programa modifica mis archivos originales?

**NO.** Los archivos en `inputs/` nunca se tocan. Todos los resultados se guardan en `outputs/`.

### Tengo múltiples archivos del mismo parcial (ej: Parcial1_1K2_1.csv, Parcial1_1K2_2.csv)

¡No hay problema! El sistema los detecta automáticamente y los consolida.

**Ejemplo:**
```
inputs/
├── Parcial1_1K2_1.csv  (Alumno García: 7.5)
├── Parcial1_1K2_2.csv  (Alumno García: 8.0)  ← Se toma esta nota
└── Parcial1_1K2_3.csv  (Alumno García: 6.5)

Resultado en outputs/1K2/Parcial1_1K2_filtrado.csv:
→ Alumno García: 8.0
```

### ¿Los nombres de archivo son case-sensitive?

**NO.** El sistema acepta mayúsculas y minúsculas indistintamente:

```
✅ Estos archivos se procesan exactamente igual:
   • TP1_1K15.csv
   • tp1_1k15.csv  
   • Tp1_1K15.csv
   • TP1_1k15.csv

✅ También para parciales:
   • Parcial1_1K2.csv
   • parcial1_1k2.csv
   • PARCIAL1_1K2.csv
```

Los archivos de salida siempre se normalizan para consistencia.

Esto funciona tanto para **Parciales** como para **Recuperatorios**.

### ¿Cómo convierten las notas?

El sistema convierte las notas de Moodle (escala 0-10 decimal) a la escala entera de calificación:

| Nota Moodle      | Nota Convertida |
|------------------|-----------------|
| 9.545 - 10.0     | 10             |
| 8.645 - 9.544    | 9              |
| 7.745 - 8.644    | 8              |
| 6.845 - 7.744    | 7              |
| 5.945 - 6.844    | 6              |
| 5.745 - 5.944    | 5              |
| 5.445 - 5.744    | 4              |
| 0 - 5.444        | 2              |

---

## 🔧 Configuración Avanzada

El archivo `config.ini` permite personalizar el comportamiento del sistema.

### ¿Dónde está?

Se crea automáticamente la primera vez que ejecutas el programa, junto a las carpetas `inputs/` y `outputs/`.

### Opciones más comunes

```ini
[Directorios]
source_dir = inputs       # Cambiar si tus CSVs están en otra carpeta
output_dir = outputs      # Cambiar dónde se guardan resultados

[TrabajoPractico]
cantidad_tps = 4          # Si tienes más o menos TPs

[Parciales]
cantidad_parciales = 2    # Si tienes más parciales
cantidad_recuperatorios = 2
```

> 📖 **Más detalles:** Ver [docs/CONFIGURATION.md](docs/CONFIGURATION.md)

---

## 🆘 Solución de Problemas

### Error: "No se encontraron archivos CSV"

**Solución:**
1. Verifica que los archivos estén en `inputs/`
2. Asegúrate que terminan en `.csv`
3. Si usas el binario, verifica que `inputs/` esté junto al ejecutable

### Error: "El archivo está vacío o no tiene headers"

**Solución:**
- El archivo CSV está corrupto o vacío
- Vuelve a exportar desde Moodle
- Abre el archivo en un editor de texto para verificar que tiene contenido

### Error: "No se encontró la columna"

**Solución:**
- El formato del CSV de Moodle es diferente al esperado
- Edita `config.ini` para ajustar los nombres de columnas
- Ver [docs/CONFIGURATION.md](docs/CONFIGURATION.md) para más detalles

### El programa se cierra inmediatamente

**Solución (si usas el binario):**
1. Abre una terminal/consola
2. Navega hasta donde está el ejecutable
3. Ejecuta: `./ACOCalculator` (macOS/Linux) o `ACOCalculator.exe` (Windows)
4. Así podrás ver los mensajes de error

---

## Soporte y Ayuda

### Documentación Completa

- **Manual Rápido:** [docs/QUICK_START.md](docs/QUICK_START.md)
- **Configuración:** [docs/CONFIGURATION.md](docs/CONFIGURATION.md)
- **Testing:** [docs/TESTING.md](docs/TESTING.md)
- **Construcción:** [docs/BUILD.md](docs/BUILD.md)
- **Índice completo:** [docs/README.md](docs/README.md)

### Reportar Problemas

¿Encontraste un error? [Abre un issue en GitHub](https://github.com/Laikos38/ACOcalculator/issues)

### Contribuir

¿Quieres mejorar el sistema? Ver [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## 📋 Información Técnica (Para Desarrolladores)

<details>
<summary>Expandir información técnica</summary>

### Arquitectura del Proyecto

```
ACOCalculator/
├── main.py                      # Script principal
├── config.ini                   # Configuración
├── pyproject.toml               # Dependencias
│
├── src/                         # Código fuente modular
│   ├── utils/                   # Utilidades
│   │   ├── config_loader.py
│   │   ├── csv_helpers.py
│   │   └── file_consolidator.py
│   ├── managers/                # Gestores
│   │   ├── tp_manager.py
│   │   └── parcial_manager.py
│   └── generators/              # Generadores
│       └── report_generator.py
│
├── tests/                       # Suite de tests
│   ├── unit/
│   ├── integration/
│   └── factories/
│
├── scripts/                     # Scripts de automatización
└── docs/                        # Documentación técnica
```

### Tecnologías

- **Python 3.8+**
- **UV** - Gestor de paquetes ultrarrápido
- **xlwt** - Generación de archivos XLS
- **pytest** - Framework de testing
- **faker & factory_boy** - Generación de datos de prueba

### Gestión de Dependencias

```bash
# Con UV (recomendado para desarrollo)
uv run main.py

# Con pip
pip install xlwt
python main.py
```

### Ejecutar Tests

```bash
# Con UV
uv run pytest

# Con pip
pip install pytest pytest-cov faker factory-boy
pytest
```

### Construir Binarios

**macOS:**
```bash
./scripts/build-macos.sh  # → dist/ACOCalculator.app
```

**Windows:**
```cmd
scripts\build-windows.bat  # → dist\ACOCalculator.exe
```

**Linux:**
```bash
./scripts/build-linux.sh  # → dist/ACOCalculator
```

Ver [docs/BUILD.md](docs/BUILD.md) para guía completa multi-plataforma.

### Licencia

MIT License - Ver [LICENSE](LICENSE)

</details>

---

**Versión 1.0** - Sistema de Gestión de Calificaciones de Moodle  
📖 [Documentación Técnica](docs/) | 🐛 [Reportar Problema](https://github.com/Laikos38/ACOcalculator/issues) | ⭐ [GitHub](https://github.com/Laikos38/ACOcalculator)
