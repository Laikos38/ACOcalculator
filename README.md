# Sistema de Gestión de Calificaciones de Moodle

## 📖 Manual de Usuario - Versión 1.0

> **Para usuarios:** Esta es la guía simplificada para usar el sistema.  
> **Para desarrolladores:** Ver documentación técnica en [docs/](docs/)

---

## 🎯 ¿Qué hace este programa?

Este sistema te ayuda a procesar las calificaciones de Moodle de forma automática:

✅ **Filtra duplicados** - Si un alumno hizo varias veces un TP, se queda con la mejor nota  
✅ **Consolida notas** - Junta todos los TPs y Parciales en un solo archivo  
✅ **Cuenta intentos** - Te dice cuántas veces intentó cada alumno  
✅ **Genera reporte final** - Crea una planilla Excel con todo junto  

---

## 🚀 Inicio Rápido

### Opción 1: Usar el Ejecutable (Recomendado para usuarios)

**¿No tienes Python instalado? ¡No hay problema!**

1. **Descarga el ejecutable** desde [Releases](https://github.com/Laikos38/ACOcalculator/releases)
2. **Doble clic** en `ACOCalculator` (o `ACOCalculator.app` en macOS)
3. **¡Listo!** El programa crea las carpetas necesarias automáticamente

### Opción 2: Ejecutar con Python

Si tienes Python instalado:

```bash
# Descargar el proyecto
git clone https://github.com/Laikos38/ACOcalculator.git
cd ACOcalculator

# Instalar dependencias
pip install xlwt

# Ejecutar
python main.py
```

---

## 📂 Preparar tus archivos

### Paso 1: Exportar desde Moodle

1. Entra a tu curso en Moodle
2. Ve a **Calificaciones** → **Exportar**
3. Selecciona formato **CSV**
4. Exporta el archivo

### Paso 2: Organizar archivos

El programa crea dos carpetas automáticamente:

```
📁 inputs/     ← Aquí pones tus archivos CSV de Moodle
📁 outputs/    ← Aquí aparecen los resultados procesados
```

**Importante:** Los nombres de archivo deben seguir este formato:
- TPs: `TP1_1K2.csv`, `TP2_1K4.csv`, etc.
- Parciales: `Parcial1_1K2.csv`, `Parcial2_1K4.csv`
- Recuperatorios: `Recuperatorio1_1K2.csv`

> 💡 **Tip:** El código del curso (ej: `1K2`, `1K4`) debe estar al final del nombre del archivo.

---

## 🎮 Cómo Usar el Sistema

### Menú Principal

Cuando ejecutas el programa, verás este menú:

```
============================================================
 SISTEMA DE GESTIÓN DE CALIFICACIONES - MOODLE
============================================================
1) Filtrar mejor calificación por alumno
2) Mergear TPs (incluye seguimiento de intentos)
3) Mergear Parciales y Recuperatorios
4) Generar Planilla Final (XLS)
h) Ayuda - Abrir manual de usuario
q) Salir
============================================================
```

### Opción 1: Filtrar mejor calificación

**¿Qué hace?**  
Si un alumno entregó varias veces el mismo TP, esta opción se queda solo con el intento de mejor nota.

**Cuándo usar:**  
Usa esto ANTES de hacer merge, para limpiar duplicados.

**Pasos:**
1. Selecciona opción `1`
2. Elige el archivo CSV de la lista
3. El resultado se guarda en `outputs/CURSO/archivo_filtrado.csv`

### Opción 2: Mergear TPs

**¿Qué hace?**  
Junta todos los TPs de un curso en UN SOLO archivo.

**Cuándo usar:**  
Después de filtrar los archivos individuales.

**Pasos:**
1. Selecciona opción `2`
2. Escribe el código del curso (ej: `1K2`)
3. Se crea `outputs/1K2/TPs_1K2_mergeado.csv`

**📊 El archivo incluye:**
- Apellido y Nombre del alumno
- Nota de cada TP
- **Cantidad de intentos** por TP (¡nuevo!)

### Opción 3: Mergear Parciales

**¿Qué hace?**  
Igual que la opción 2, pero para Parciales y Recuperatorios.

**Pasos:**
1. Selecciona opción `3`
2. Escribe el código del curso
3. Se crea `outputs/1K2/Parciales_1K2_mergeado.csv`

### Opción 4: Generar Planilla Final

**¿Qué hace?**  
Crea un archivo Excel (`.xls`) con **TODAS** las notas juntas:
- Todos los TPs con sus intentos
- Todos los Parciales
- Todos los Recuperatorios

**Cuándo usar:**  
Al final, cuando ya procesaste todo.

**Pasos:**
1. Selecciona opción `4`
2. Escribe el código del curso
3. Se crea `outputs/1K2/Planilla_Final_1K2.xls`

**📊 Este archivo incluye:**
- Datos del alumno (Apellido, Nombre, ID)
- Nota decimal de Moodle (ej: 8.5)
- Nota entera convertida (ej: 9)
- Cantidad de intentos por TP

### Opción h: Ayuda

Abre este manual en tu navegador web.

### Opción q: Salir

Cierra el programa.

---

## 💡 Ejemplos Prácticos

### Ejemplo 1: Procesar TPs del curso 1K2

```
1. Poner en inputs/:
   - TP1_1K2.csv
   - TP2_1K2.csv
   - TP3_1K2.csv
   - TP4_1K2.csv

2. Ejecutar programa

3. Seleccionar opción 1 → Filtrar cada archivo
   (Repetir para TP1, TP2, TP3, TP4)

4. Seleccionar opción 2 → Mergear TPs
   → Escribir: 1K2

5. ¡Listo! Resultado en:
   outputs/1K2/TPs_1K2_mergeado.csv
```

### Ejemplo 2: Procesar todo (TPs + Parciales + Planilla Final)

```
1. Poner en inputs/:
   📄 TP1_1K2.csv
   📄 TP2_1K2.csv
   📄 Parcial1_1K2.csv
   📄 Parcial2_1K2.csv
   📄 Recuperatorio1_1K2.csv

2. Filtrar todos los archivos (opción 1)

3. Mergear TPs (opción 2) → Escribir: 1K2

4. Mergear Parciales (opción 3) → Escribir: 1K2

5. Generar Planilla Final (opción 4) → Escribir: 1K2

6. Abrir: outputs/1K2/Planilla_Final_1K2.xls
```

---

## ❓ Preguntas Frecuentes

### ¿Por qué mis archivos no aparecen?

**Verifica:**
- ✅ Los archivos están en la carpeta `inputs/`
- ✅ Los archivos terminan en `.csv`
- ✅ El nombre incluye el código del curso (ej: `_1K2`)

### ¿Qué significa "filtrado"?

Significa que se eliminaron los intentos repetidos, quedándose solo con la mejor nota de cada alumno.

### ¿Puedo procesar varios cursos?

¡Sí! El programa organiza automáticamente cada curso en su propia carpeta:
```
outputs/
├── 1K2/
│   ├── TPs_1K2_mergeado.csv
│   └── Planilla_Final_1K2.xls
└── 1K4/
    ├── TPs_1K4_mergeado.csv
    └── Planilla_Final_1K4.xls
```

### ¿Cómo sé cuántos intentos hizo un alumno?

En el archivo mergeado de TPs, verás columnas como:
- `TP1_Intentos` → Cantidad de veces que entregó el TP1
- `TP2_Intentos` → Cantidad de veces que entregó el TP2
- etc.

### ¿Qué pasa si un alumno no entregó un TP?

Aparecerá como "Falta" en la planilla.

### ¿El programa modifica mis archivos originales?

**NO.** Los archivos en `inputs/` nunca se tocan. Todos los resultados se guardan en `outputs/`.

### Tengo múltiples archivos del mismo parcial (ej: Parcial1_1K2_1.csv, Parcial1_1K2_2.csv)

¡No hay problema! El sistema los detecta automáticamente y los consolida, tomando la mejor nota de cada alumno.

### ¿Cómo convierten las notas?

El sistema convierte las notas de Moodle (escala 0-10 decimal) a la escala entera de calificación:

| Nota Moodle | Nota Convertida |
|-------------|-----------------|
| 9.6 - 10.0  | 10             |
| 8.6 - 9.5   | 9              |
| 7.7 - 8.5   | 8              |
| 6.8 - 7.6   | 7              |
| 5.9 - 6.7   | 6              |
| 5.7 - 5.8   | 4              |
| < 5.7       | 2              |

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

## 📞 Soporte y Ayuda

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

```bash
# Instalar PyInstaller
uv pip install pyinstaller

# Construir
./scripts/build-macos.sh

# Binario en: dist/ACOCalculator
```

Ver [docs/BUILD.md](docs/BUILD.md) para más detalles.

### Características Principales

#### 1. Seguimiento de Intentos en TPs
- Nueva columna `TP{N}_Intentos` que registra cuántos intentos hizo cada alumno
- Conteo automático desde archivos originales
- Visible en planilla final

#### 2. Sistema de Configuración Externa
- Archivo `config.ini` en texto plano
- Variables configurables: directorios, headers, cantidades, etc.
- Sin necesidad de modificar código

#### 3. Arquitectura Modular
- **Utils**: Funciones auxiliares reutilizables
- **Managers**: Lógica de negocio (TPManager, ParcialManager)
- **Generators**: Generación de reportes (ReportGenerator)
- **Main**: Solo orquestación y UI

#### 4. Validación Robusta
- Manejo de archivos vacíos
- Detección de headers faltantes
- Mensajes de error claros
- El programa no crashea ante errores

#### 5. Testing Completo
- 52 tests unitarios e integración
- 80% de cobertura de código
- Factories con faker para datos realistas

### Historial de Cambios

Ver [docs/CHANGELOG.md](docs/CHANGELOG.md)

### Licencia

MIT License - Ver [LICENSE](LICENSE)

</details>

---

## ✨ Características Destacadas

- ✅ **Interfaz amigable** - Menú simple y claro
- ✅ **Automático** - Crea carpetas y archivos necesarios
- ✅ **Organizado** - Separa resultados por curso
- ✅ **Robusto** - Maneja errores sin crashear
- ✅ **Flexible** - Configurable mediante `config.ini`
- ✅ **Seguimiento de intentos** - Cuenta cuántas veces entregó cada alumno
- ✅ **Multi-curso** - Procesa varios cursos a la vez
- ✅ **Sin Python requerido** - Disponible como ejecutable standalone

---

**Versión 1.0** - Sistema de Gestión de Calificaciones de Moodle  
📖 [Documentación Técnica](docs/) | 🐛 [Reportar Problema](https://github.com/Laikos38/ACOcalculator/issues) | ⭐ [GitHub](https://github.com/Laikos38/ACOcalculator)
