# Guía de Construcción de Binarios - ACOCalculator

## 📦 Generación de Ejecutables Standalone

ACOCalculator puede compilarse en ejecutables standalone que **no requieren Python instalado**. Esto es ideal para distribuir a usuarios finales.

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

## 📤 Distribución

### Crear ZIP para Distribución

```bash
# Comprimir el bundle
cd dist
zip -r ACOCalculator-macos-v1.0.0.zip ACOCalculator.app

# El ZIP resultante se puede compartir
```

### Crear DMG Profesional (Opcional)

Para distribución más profesional, crea un DMG:

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

### Reducir Tamaño del Ejecutable

```bash
# Habilitar compresión UPX (ya activada por defecto)
upx=True

# Excluir módulos de testing
excludes=['pytest', 'faker', 'factory', '_pytest', 'tests']
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

#### Bundle No Abre en macOS

**Solución**: Firmar el bundle:

```bash
codesign --force --deep --sign - dist/ACOCalculator.app
```

## 📊 Información del Binario

### Tamaños Típicos

- **Ejecutable CLI**: ~15-20 MB
- **Bundle .app**: ~25-30 MB
- **DMG comprimido**: ~10-15 MB

Los binarios incluyen:
- ✅ Intérprete Python
- ✅ Todas las dependencias (xlwt, etc.)
- ✅ Código fuente del proyecto
- ✅ Archivo de configuración

### Verificar Binario

```bash
# Ver tamaño
du -sh dist/ACOCalculator

# Ver arquitectura
file dist/ACOCalculator

# Probar ejecución
./dist/ACOCalculator --help
```

## 🏗️ Build Automatizado (CI/CD)

### GitHub Actions (Ejemplo)

```yaml
name: Build macOS

on:
  release:
    types: [created]

jobs:
  build:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      
      - name: Build binary
        run: ./scripts/build-macos.sh
      
      - name: Create ZIP
        run: |
          cd dist
          zip -r ACOCalculator-macos.zip ACOCalculator.app
      
      - name: Upload Release Asset
        uses: actions/upload-release-asset@v1
        with:
          asset_path: dist/ACOCalculator-macos.zip
          asset_name: ACOCalculator-macos-${{ github.ref_name }}.zip
```

## 🔐 Firma y Notarización (macOS)

Para distribución fuera de la Mac App Store:

### 1. Obtener Certificado de Desarrollador

```bash
# Verificar certificados instalados
security find-identity -v -p codesigning
```

### 2. Firmar el Bundle

```bash
codesign --deep --force \
  --sign "Developer ID Application: Tu Nombre" \
  dist/ACOCalculator.app
```

### 3. Notarizar (Opcional)

```bash
# Comprimir
ditto -c -k --keepParent dist/ACOCalculator.app ACOCalculator.zip

# Subir para notarización
xcrun notarytool submit ACOCalculator.zip \
  --apple-id tu@email.com \
  --team-id TEAMID \
  --password app-specific-password
```

## 📝 Checklist de Distribución

Antes de distribuir, verificar:

- [ ] El ejecutable se ejecuta sin errores
- [ ] `config.ini` está incluido
- [ ] Los directorios `inputs/` y `outputs/` se crean automáticamente
- [ ] El menú funciona correctamente
- [ ] Todas las funcionalidades (filtrar, mergear, generar) funcionan
- [ ] El tamaño del binario es razonable (< 50 MB)
- [ ] Probado en un Mac limpio (sin Python instalado)
- [ ] Incluye README o documentación básica
- [ ] Versión correcta en el nombre del archivo

## 🆘 Soporte

### Reportar Problemas con Binarios

Si el binario no funciona:

1. Ejecutar desde terminal para ver errores:
   ```bash
   ./dist/ACOCalculator
   ```

2. Verificar logs en:
   ```bash
   # macOS
   ~/Library/Logs/ACOCalculator/
   ```

3. Probar versión debug:
   ```bash
   # Editar acocalculator.spec
   debug=True
   # Reconstruir
   ./scripts/build-macos.sh
   ```

## 📚 Recursos Adicionales

- **PyInstaller Docs**: https://pyinstaller.org/
- **macOS Code Signing**: https://developer.apple.com/support/code-signing/
- **create-dmg**: https://github.com/create-dmg/create-dmg

---

## 🎯 TL;DR - Resumen Rápido

```bash
# Construir
./scripts/build-macos.sh

# Ejecutar
./dist/ACOCalculator
# o
open dist/ACOCalculator.app

# Distribuir
cd dist && zip -r ACOCalculator-macos.zip ACOCalculator.app
```

**El ejecutable funciona en cualquier Mac sin Python instalado.** 🎉

