# Guía de Uso del Binario - ACOCalculator

## 🚀 Inicio Rápido

El binario `ACOCalculator` es **completamente standalone** y funciona sin ninguna instalación previa.

> **Disponible para:** 🍎 macOS | 🪟 Windows | 🐧 Linux

### Primer Uso

**macOS / Linux:**
```bash
# 1. Copiar el binario a cualquier directorio
cp dist/ACOCalculator ~/Desktop/

# 2. Ir al directorio
cd ~/Desktop/

# 3. Ejecutar (primera vez)
./ACOCalculator
```

**Windows:**
```cmd
REM 1. Copiar ACOCalculator.exe al escritorio

REM 2. Ir al directorio
cd %USERPROFILE%\Desktop

REM 3. Ejecutar (primera vez)
ACOCalculator.exe
```

### Qué Sucede en la Primera Ejecución

```
============================================================
 BIENVENIDO AL SISTEMA DE GESTIÓN DE CALIFICACIONES
 Versión 1.0 - Modular y Profesional
============================================================

ℹ️  No se encontró config.ini, usando configuración por defecto
✅ Archivo de configuración creado: config.ini
   Puedes editarlo para personalizar el comportamiento del sistema.

📁 Directorio de trabajo: /Users/tu_usuario/Desktop

✅ Directorio de entrada creado: inputs/
✅ Directorio de salida creado: outputs/

============================================================
 SISTEMA DE GESTIÓN DE CALIFICACIONES - MOODLE
============================================================
1) Generar planilla de notas (XLS)
2) Operaciones intermedias
h) Ayuda - Abrir manual de usuario
q) Salir
============================================================
```

## 📁 Estructura de Directorios

El binario crea los directorios **en su misma ubicación** (no en el directorio actual de trabajo):

```
directorio_del_binario/
├── ACOCalculator          # El binario ejecutable
├── config.ini             # Se crea automáticamente aquí
├── inputs/                # Se crea automáticamente aquí
│   └── (tus archivos CSV de Moodle aquí)
└── outputs/               # Se crea automáticamente aquí
    ├── 1K2/               # Se crea al procesar curso 1K2
    ├── 1K4/               # Se crea al procesar curso 1K4
    └── ...
```

**Importante**: Los directorios se crean junto al binario, independientemente de desde dónde lo ejecutes.

### Directorios Automáticos

✅ **inputs/** - Se crea automáticamente al iniciar
- Coloca aquí tus archivos CSV de Moodle
- Formatos esperados: `TP1_1K2.csv`, `Parcial1_1K4.csv`, etc.
- ✨ **Case-insensitive**: También acepta `tp1_1k2.csv`, `parcial1_1k4.csv`, etc.

✅ **outputs/** - Se crea automáticamente al iniciar
- Aquí se guardan todos los resultados procesados
- Se organizan automáticamente por curso

✅ **config.ini** - Se crea automáticamente si no existe
- Configuración por defecto funcional
- Puedes editarlo para personalizar

## 🎯 Workflow Típico

### 1. Preparar Archivos

```bash
# Estructura inicial
~/mi_proyecto/
└── ACOCalculator

# Ejecutar para crear directorios
./ACOCalculator
q  # Salir

# Ahora tienes
~/mi_proyecto/
├── ACOCalculator
├── config.ini
├── inputs/        ← Poner CSVs aquí
└── outputs/       ← Resultados aquí
```

### 2. Agregar Archivos CSV

```bash
# Copiar tus CSVs de Moodle
cp ~/Downloads/TP1_1K2.csv inputs/
cp ~/Downloads/TP2_1K2.csv inputs/
cp ~/Downloads/Parcial1_1K2.csv inputs/
```

**✨ Flexibilidad en Nomenclatura:**

El sistema acepta **cualquier combinación de mayúsculas y minúsculas**:

```
✅ Todos estos archivos son VÁLIDOS y se procesan igual:

   TP1_1K15.csv          tp1_1k15.csv
   Tp1_1K15.csv          TP1_1k15.csv
   
   Parcial1_1K2.csv      parcial1_1k2.csv
   PARCIAL1_1K2.csv      Parcial1_1k2.csv
   
   Recuperatorio1_1K4.csv   recuperatorio1_1k4.csv
   RECUPERATORIO1_1K4.csv   Recuperatorio1_1K4_1.csv
```

> **Nota:** Los archivos de salida se normalizan automáticamente a mayúsculas para mantener consistencia (ej: `TP1_1K15_filtrado.csv`).

### 3. Procesar Datos

```bash
./ACOCalculator

# Opción 1: Generar planilla final (recomendado)
# Opción 2: Operaciones intermedias
#   → Sub-opción 1: Filtrar cada archivo individualmente
#   → Sub-opción 2: Unificar TPs para un curso
#   → Sub-opción 3: Unificar Parciales para un curso
```

### 4. Obtener Resultados

```bash
# Los resultados están en:
outputs/1K2/
├── TP1_1K2_filtrado.csv
├── TP2_1K2_filtrado.csv
├── TPs_1K2_unificado.csv
├── Parciales_1K2_unificado.csv
└── Planilla_Final_1K2.xls
```

## 🚚 Distribución

### Compartir con Otros Usuarios

**Opción 1: Solo el binario**

```bash
# El destinatario solo necesita:
cp ACOCalculator /destino/
cd /destino/
./ACOCalculator  # Todo se crea automáticamente
```

**Opción 2: Con configuración personalizada**

```bash
# Incluir config.ini personalizado
zip -r ACOCalculator.zip ACOCalculator config.ini

# El destinatario:
unzip ACOCalculator.zip
cd ACOCalculator/
./ACOCalculator  # Usa el config incluido
```

**Opción 3: Package completo con ejemplos**

```bash
./scripts/create-release.sh
# Genera: release/ACOCalculator-v1.0.0-macos.zip
# Incluye: binario + config + docs + directorios
```

## ⚠️ Notas Importantes

### Ubicación del Binario

El binario crea los directorios **junto a sí mismo**, no en el directorio actual de trabajo:

```bash
# ✅ CORRECTO - Funciona desde cualquier ubicación
cd ~/cualquier_lugar/
~/mi_proyecto/ACOCalculator
# Crea inputs/ y outputs/ en ~/mi_proyecto/

# ✅ TAMBIÉN CORRECTO
cd ~/mi_proyecto/
./ACOCalculator
# Crea inputs/ y outputs/ en ~/mi_proyecto/
```

**Los directorios siempre se crean junto al binario**, no importa desde dónde lo ejecutes.

## 🔍 Verificación

### Comprobar que Funciona

```bash
# Ejecutar script de prueba
./scripts/test-binary.sh

# O probar manualmente:
mkdir -p /tmp/test_aco
cp dist/ACOCalculator /tmp/test_aco/
cd /tmp/test_aco/
./ACOCalculator
q

# Verificar:
ls -la  # Debe mostrar inputs/, outputs/, config.ini
```

### Ver Ubicación del Binario

El binario muestra al iniciar:

```
📁 Ubicación del ejecutable: /Users/tu_usuario/tu_directorio
```

Este es el directorio donde se crearán `inputs/` y `outputs/`, independientemente de desde dónde ejecutes el binario.

## 📊 Troubleshooting

### "No existe el directorio 'inputs'"

**Problema**: Ejecutaste el binario pero saliste antes de que creara los directorios.

**Solución**: Ejecuta de nuevo, los directorios se crean al inicio.

### "No hay archivos CSV en la carpeta"

**Problema**: El directorio `inputs/` está vacío.

**Solución**: Copia tus CSVs de Moodle a `inputs/`

### "No se encontró el archivo filtrado"

**Problema**: Intentas unificar sin filtrar primero.

**Solución**: El programa filtra automáticamente si faltan archivos.

### Permisos Denegados

```bash
# Si dice "Permission denied"
chmod +x ACOCalculator
```

## 📖 Documentación Completa

- **BUILD.md** - Cómo construir binarios (macOS, Windows, Linux)
- **CONFIGURATION.md** - Guía de configuración
- **README.md** - Documentación general

---

## 🎯 TL;DR - Resumen

1. **Copia** el binario a cualquier directorio
2. **Ejecuta** `./ACOCalculator`
3. **Todo se crea automáticamente**: config.ini, inputs/, outputs/
4. **Agrega** tus CSVs a `inputs/`
5. **Procesa** usando el menú
6. **Obtén** resultados en `outputs/`

¡Así de simple! 🎉

