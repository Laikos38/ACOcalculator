# Guía de Construcción de Binarios - ACOCalculator

## 📦 Generación de Ejecutables Standalone

ACOCalculator puede compilarse en ejecutables standalone que **no requieren Python instalado**. Esto es ideal para distribuir a usuarios finales.

**Plataformas soportadas:**
- 🍎 macOS (Intel y Apple Silicon)
- 🪟 Windows (x64, x86)
- 🐧 Linux (x86_64, arm64, etc.)

> ⚠️ **Nota importante**: Los binarios deben compilarse en el SO objetivo. Un binario compilado en Windows no funcionará en macOS o Linux, y viceversa.

---

## 🍎 Construir para macOS

### Requisitos

- macOS 10.13 o superior
- UV instalado
- 500 MB de espacio libre

### Construcción Rápida

```bash
# Generar ejecutable
./scripts/build-macos.sh
```

Este script:
1. ✅ Instala PyInstaller automáticamente
2. ✅ Limpia builds anteriores
3. ✅ Construye el ejecutable
4. ✅ Crea bundle macOS (.app)
5. ✅ Verifica los binarios generados

### Salida Generada

Después del build, encontrarás en `dist/`:

```
dist/
├── ACOCalculator          # Ejecutable CLI (standalone)
└── ACOCalculator.app/     # Bundle macOS (doble clic)
```

## 🚀 Ejecutar Binarios

### Opción 1: Ejecutable CLI

```bash
# Desde terminal
./dist/ACOCalculator

# Copiar a cualquier Mac y ejecutar
cp dist/ACOCalculator ~/Desktop/
~/Desktop/ACOCalculator
```

### Opción 2: Bundle macOS (.app)

```bash
# Doble clic en Finder, o:
open dist/ACOCalculator.app
```

⚠️ **Primera ejecución**: macOS puede mostrar advertencia de seguridad.
Solución: Click derecho → Abrir → Confirmar

---

## 🪟 Construir para Windows

### Requisitos

- Windows 10 o superior
- UV instalado ([Descargar aquí](https://github.com/astral-sh/uv))
- 500 MB de espacio libre

### Construcción Rápida

**Opción 1: Usando CMD o PowerShell**

```cmd
REM Ejecutar script batch
scripts\build-windows.bat
```

**Opción 2: Usando Git Bash o WSL**

```bash
# Convertir y ejecutar (si no hay permisos)
chmod +x scripts/build-windows.bat
./scripts/build-windows.bat
```

Este script:
1. ✅ Instala PyInstaller automáticamente
2. ✅ Limpia builds anteriores
3. ✅ Construye el ejecutable
4. ✅ Verifica el binario generado

### Salida Generada

Después del build, encontrarás en `dist/`:

```
dist/
└── ACOCalculator.exe      # Ejecutable Windows (standalone)
```

### Ejecutar el Binario

```cmd
REM Opción 1: Doble clic en el archivo
REM Opción 2: Desde CMD
.\dist\ACOCalculator.exe

REM Opción 3: Desde PowerShell
.\dist\ACOCalculator.exe
```

### Distribución para Windows

```cmd
REM Opción 1: ZIP simple
cd dist
tar -a -c -f ACOCalculator-windows-v1.0.0.zip ACOCalculator.exe

REM Opción 2: Instalador profesional con InnoSetup o NSIS
```

⚠️ **Windows Defender**: Puede mostrar advertencia en primera ejecución. Esto es normal para binarios sin firma digital.

---

## 🐧 Construir para Linux

### Requisitos

- Linux (Ubuntu, Debian, Fedora, Arch, etc.)
- UV instalado
- 500 MB de espacio libre

### Construcción Rápida

```bash
# Dar permisos de ejecución (primera vez)
chmod +x scripts/build-linux.sh

# Generar ejecutable
./scripts/build-linux.sh
```

Este script:
1. ✅ Instala PyInstaller automáticamente
2. ✅ Limpia builds anteriores
3. ✅ Construye el ejecutable
4. ✅ Configura permisos de ejecución
5. ✅ Verifica el binario generado

### Salida Generada

Después del build, encontrarás en `dist/`:

```
dist/
└── ACOCalculator          # Ejecutable Linux (standalone)
```

### Ejecutar el Binario

```bash
# Desde terminal
./dist/ACOCalculator

# Copiar a cualquier ubicación
cp dist/ACOCalculator ~/bin/
~/bin/ACOCalculator
```

### Distribución para Linux

```bash
# Crear tarball con arquitectura en el nombre
tar -czf ACOCalculator-linux-$(uname -m)-v1.0.0.tar.gz -C dist ACOCalculator

# El archivo resultante será:
# - ACOCalculator-linux-x86_64-v1.0.0.tar.gz (Intel/AMD 64-bit)
# - ACOCalculator-linux-aarch64-v1.0.0.tar.gz (ARM 64-bit)
```

⚠️ **Compatibilidad**: El binario Linux funciona solo en la misma arquitectura donde se compiló. Para soportar múltiples arquitecturas, compila en cada una.

---

## 📤 Distribución Multi-Plataforma

### Crear Paquetes para GitHub Releases

```bash
# macOS
cd dist
zip -r ACOCalculator-macos-v1.0.0.zip ACOCalculator.app

# Windows (desde PowerShell)
Compress-Archive -Path dist\ACOCalculator.exe -DestinationPath ACOCalculator-windows-v1.0.0.zip

# Linux
tar -czf ACOCalculator-linux-$(uname -m)-v1.0.0.tar.gz -C dist ACOCalculator
```

### Crear DMG para macOS (Opcional)

Para distribución más profesional en macOS:

```bash
# Instalar create-dmg (una sola vez)
brew install create-dmg

# Crear DMG
create-dmg \
  --volname "ACOCalculator" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "ACOCalculator.app" 175 120 \
  --app-drop-link 425 120 \
  "ACOCalculator-v1.0.0.dmg" \
  "dist/ACOCalculator.app"
```

### Estructura de Release Completo

```
releases/
├── ACOCalculator-macos-v1.0.0.zip          # macOS (Intel + M1/M2)
├── ACOCalculator-windows-v1.0.0.zip        # Windows (x64)
└── ACOCalculator-linux-x86_64-v1.0.0.tar.gz # Linux (x86_64)
```

## ⚙️ Configuración Avanzada

### Personalizar el Build

Edita `acocalculator.spec` para:

#### Agregar Icono

```python
exe = EXE(
    ...
    icon='assets/icon.icns',  # Tu icono personalizado
)
```

#### Excluir Módulos Innecesarios

```python
a = Analysis(
    ...
    excludes=[
        'pytest', 'faker', 'tests',  # Ya excluidos
        'tkinter',  # Si no usas GUI
        'matplotlib',  # Si no usas gráficos
    ],
)
```

#### Incluir Archivos Adicionales

```python
a = Analysis(
    ...
    datas=[
        ('config.ini', '.'),
        ('README.md', '.'),
        ('assets/', 'assets/'),  # Carpeta completa
    ],
)
```

## 🔍 Debugging del Build

### Ver Qué Se Incluye

```bash
# Analizar el build
uv run pyinstaller --log-level=DEBUG acocalculator.spec
```

### Probar en Modo Debug

Edita `acocalculator.spec`:

```python
exe = EXE(
    ...
    debug=True,  # Activar modo debug
    console=True,  # Mostrar consola
)
```

### Errores Comunes

#### Error: "Module not found"

**Solución**: Agregar a `hiddenimports` en `.spec`:

```python
hiddenimports=[
    'xlwt',
    'tu_modulo_faltante',
],
```

#### Error: "config.ini not found"

**Solución**: Verificar que está en `datas`:

```python
datas=[
    ('config.ini', '.'),
],
```


## 📚 Recursos Adicionales

- **PyInstaller Docs**: https://pyinstaller.org/

---

## 🎯 TL;DR - Resumen Rápido

### macOS
```bash
./scripts/build-macos.sh
./dist/ACOCalculator
# o: open dist/ACOCalculator.app
```

### Windows
```cmd
scripts\build-windows.bat
.\dist\ACOCalculator.exe
```

### Linux
```bash
chmod +x scripts/build-linux.sh
./scripts/build-linux.sh
./dist/ACOCalculator
```
