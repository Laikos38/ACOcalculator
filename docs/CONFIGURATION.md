# Guía de Configuración - ACOCalculator

## 📋 Descripción

ACOCalculator utiliza un sistema de configuración flexible con **configuración por defecto embebida** y soporte para personalización mediante archivo externo.

## 🎯 Prioridad de Configuración

El sistema sigue esta prioridad:

1. **Archivo `config.ini` externo** (si existe) - **MÁXIMA PRIORIDAD**
2. **Configuración por defecto embebida** (fallback)

```
┌─────────────────────────────────────┐
│  ¿Existe config.ini?                │
│                                     │
│  SI  → Usar config.ini ✅           │
│  NO  → Usar default + crear config  │
└─────────────────────────────────────┘
```

## 🚀 Uso Básico

### Sin Configuración Externa

El programa funciona **inmediatamente sin ninguna configuración**:

```bash
# Simplemente ejecutar
./dist/ACOCalculator

# Output:
# ℹ️  No se encontró config.ini, usando configuración por defecto
# ✅ Archivo de configuración creado: config.ini
#    Puedes editarlo para personalizar el comportamiento del sistema.
```

### Con Configuración Personalizada

1. El programa crea automáticamente `config.ini` en la primera ejecución
2. Edita `config.ini` según tus necesidades
3. En la próxima ejecución, usará tu configuración:

```bash
./dist/ACOCalculator

# Output:
# ✅ Usando configuración personalizada: config.ini
```

## ⚙️ Configuración Por Defecto

Esta es la configuración embebida (no requiere archivo):

```ini
[Directorios]
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
```

## 🎨 Personalización

### Cambiar Directorios

```ini
[Directorios]
source_dir = mis_archivos_csv
output_dir = resultados
```

### Cambiar Cantidad de TPs

```ini
[TrabajoPractico]
cantidad_tps = 6
tp_prefix = TRABAJO
```

### Cambiar Headers de Moodle

Si tu Moodle tiene headers diferentes:

```ini
[Headers]
calification_header = Nota/10
header_apellido = Apellido
header_nombre = Nombre
header_id = ID
```

### Configuración Parcial

**Puedes definir solo lo que quieres cambiar**. Los valores no definidos usarán los defaults:

```ini
# Solo cambiar directorios, resto usa defaults
[Directorios]
source_dir = datos_2024
output_dir = reportes_2024
```

## 📖 Ejemplos de Uso

### Ejemplo 1: Primera Ejecución

```bash
$ ./dist/ACOCalculator

ℹ️  No se encontró config.ini, usando configuración por defecto
✅ Archivo de configuración creado: config.ini
   Puedes editarlo para personalizar el comportamiento del sistema.

=== MENÚ ===
1) Filtrar mejor calificación por alumno
2) Mergear TPs
3) Mergear Parciales
4) Generar Planilla Final (XLS)
q) Salir
```

El programa:
- ✅ Funciona inmediatamente con defaults
- ✅ Crea `config.ini` automáticamente
- ✅ Puedes editar `config.ini` después

### Ejemplo 2: Con Configuración Personalizada

```bash
$ cat config.ini
[Directorios]
source_dir = datos_materias
output_dir = planillas_finales

[TrabajoPractico]
cantidad_tps = 5

$ ./dist/ACOCalculator

✅ Usando configuración personalizada: config.ini

=== MENÚ ===
...
```

### Ejemplo 3: Distribución del Binario

```bash
# El binario funciona SIN config.ini
$ cp dist/ACOCalculator ~/Desktop/
$ cd ~/Desktop
$ ./ACOCalculator

# Funciona inmediatamente y crea config.ini automáticamente
ℹ️  No se encontró config.ini, usando configuración por defecto
✅ Archivo de configuración creado: config.ini
```

## 🔧 API de Configuración

### Uso Programático

```python
from src.utils.config_loader import ConfigLoader

# Cargar configuración (con fallback automático a default)
config = ConfigLoader()

# Verificar si está usando default
if config.is_using_default():
    print("Usando configuración por defecto")
else:
    print("Usando configuración personalizada")

# Obtener valores
source_dir = config.get_source_dir()
cantidad_tps = config.get_cantidad_tps()
```

### Crear Configuración Programáticamente

```python
from src.utils.config_loader import ConfigLoader

# Cargar default
config = ConfigLoader("mi_config.ini")

# El archivo mi_config.ini se crea automáticamente
# con valores por defecto si no existe
```

## 📝 Referencia Completa de Opciones

### [Directorios]

| Opción | Default | Descripción |
|--------|---------|-------------|
| `source_dir` | `inputs` | Directorio de archivos CSV de entrada |
| `output_dir` | `outputs` | Directorio para archivos generados |

### [Headers]

| Opción | Default | Descripción |
|--------|---------|-------------|
| `calification_header` | `Calificación/10,00` | Header de notas en CSV |
| `header_apellido` | `Apellido(s), Apellidos, Last Name` | Headers posibles para apellido |
| `header_nombre` | `Nombre, First Name` | Headers posibles para nombre |
| `header_id` | `Número de ID, ID` | Headers posibles para ID |

### [TrabajoPractico]

| Opción | Default | Descripción |
|--------|---------|-------------|
| `cantidad_tps` | `4` | Cantidad de TPs a procesar |
| `tp_prefix` | `TP` | Prefijo para archivos de TPs |

### [Parciales]

| Opción | Default | Descripción |
|--------|---------|-------------|
| `cantidad_parciales` | `2` | Cantidad de parciales |
| `cantidad_recuperatorios` | `2` | Cantidad de recuperatorios |
| `parcial_prefix` | `Parcial` | Prefijo para parciales |
| `recuperatorio_prefix` | `Recuperatorio` | Prefijo para recuperatorios |

### [Formatos]

| Opción | Default | Descripción |
|--------|---------|-------------|
| `csv_encoding` | `utf-8-sig` | Encoding para leer/escribir CSVs |
| `output_format` | `xls` | Formato de salida (xls) |


## 🔍 Debugging de Configuración

### Ver Qué Configuración Se Está Usando

```bash
# El programa imprime al iniciar:
✅ Usando configuración personalizada: config.ini
# o
ℹ️  No se encontró config.ini, usando configuración por defecto
```

### Verificar Valores Cargados

```python
from src.utils.config_loader import ConfigLoader

config = ConfigLoader()

# Mostrar todos los valores
print(f"Source dir: {config.get_source_dir()}")
print(f"Output dir: {config.get_output_dir()}")
print(f"Cantidad TPs: {config.get_cantidad_tps()}")
print(f"TP prefix: {config.get_tp_prefix()}")
```

### Regenerar config.ini

```bash
# Eliminar config existente
rm config.ini

# Ejecutar el programa
./ACOCalculator

# Se crea nuevo config.ini con defaults
```

## ⚠️ Notas Importantes

### En Binarios

- ✅ El binario **NO requiere** `config.ini` externo
- ✅ Funciona **out-of-the-box**
- ✅ Crea `config.ini` automáticamente en primera ejecución
- ✅ Respeta `config.ini` externo si existe

### Ubicación del config.ini

El programa busca `config.ini` en:
1. Directorio actual de ejecución
2. Si no existe, crea uno nuevo ahí
3. Si no puede escribir, continúa con defaults en memoria

## 📚 Recursos Adicionales

- **README.md**: Documentación general del proyecto
- **BUILD.md**: Cómo construir binarios
- **src/utils/config_loader.py**: Implementación de la configuración

---

## 💡 TL;DR - Resumen

1. **El programa funciona SIN configuración** - usa defaults embebidos
2. **config.ini es opcional** - se crea automáticamente si no existe
3. **config.ini tiene prioridad** - sobrescribe defaults
4. **Configuración parcial funciona** - solo define lo que cambias
5. **Binario standalone** - no requiere config.ini externo
