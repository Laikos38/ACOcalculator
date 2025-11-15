#!/bin/bash
# Script para crear releases distribuibles multi-plataforma

set -e

cd "$(dirname "$0")/.."

VERSION="1.0.0"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║        CREACIÓN DE RELEASES MULTI-PLATAFORMA                ║"
echo "║                   Versión: ${VERSION}                          ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Limpiar releases anteriores
echo "🧹 Limpiando releases anteriores..."
rm -rf release
mkdir -p release
echo "✅ Directorio limpio"
echo ""

# Función para crear README de distribución
create_readme() {
    local platform=$1
    local executable=$2
    
    cat > "$3" << EOFREADME
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║            ACOCALCULATOR v${VERSION} para ${platform}
║    Sistema de Gestión de Calificaciones de Moodle          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🚀 INICIO RÁPIDO
═══════════════════════════════════════════════════════════════

EOFREADME

    if [ "$platform" = "macOS" ]; then
        cat >> "$3" << 'EOFREADME'
Opción 1: Doble clic en ACOCalculator.app

Opción 2: Desde terminal:
   ./ACOCalculator

⚠️ PRIMERA EJECUCIÓN
═══════════════════════════════════════════════════════════════

macOS puede mostrar una advertencia de seguridad.

Solución:
1. Click derecho en ACOCalculator.app
2. Seleccionar "Abrir"
3. Confirmar "Abrir" en el diálogo
EOFREADME
    elif [ "$platform" = "Windows" ]; then
        cat >> "$3" << 'EOFREADME'
Opción 1: Doble clic en ACOCalculator.exe

Opción 2: Desde CMD/PowerShell:
   ACOCalculator.exe

⚠️ PRIMERA EJECUCIÓN
═══════════════════════════════════════════════════════════════

Windows Defender puede mostrar una advertencia.
Esto es normal para binarios sin firma digital.

Solución:
1. Clic en "Más información"
2. Clic en "Ejecutar de todas formas"
EOFREADME
    else # Linux
        cat >> "$3" << 'EOFREADME'
Desde terminal:
   ./ACOCalculator

⚠️ PRIMERA EJECUCIÓN
═══════════════════════════════════════════════════════════════

Si obtienes "Permission denied":
   chmod +x ACOCalculator
   ./ACOCalculator
EOFREADME
    fi

    cat >> "$3" << 'EOFREADME'

📁 ESTRUCTURA
═══════════════════════════════════════════════════════════════

inputs/     - Coloca aquí tus archivos CSV de Moodle
outputs/    - Aquí se guardarán los resultados
config.ini  - Configuración del sistema (editable)
docs/       - Documentación completa

📖 DOCUMENTACIÓN
═══════════════════════════════════════════════════════════════

- README.md           - Manual de usuario completo
- docs/QUICK_START.md - Guía de inicio rápido
- docs/BINARY_USAGE.md - Uso detallado del binario
- docs/CONFIGURATION.md - Configuración avanzada

✅ CARACTERÍSTICAS
═══════════════════════════════════════════════════════════════

✓ No requiere Python instalado
✓ Incluye todas las dependencias
✓ Procesamiento automático de calificaciones
✓ Merge de TPs y Parciales
✓ Generación de planillas finales en XLS
✓ Seguimiento de intentos por estudiante
✓ Consolidación automática de múltiples archivos
✓ Conversión de notas según escala de cátedra

🆘 SOPORTE
═══════════════════════════════════════════════════════════════

Si encuentras problemas:

1. Revisa docs/BINARY_USAGE.md para troubleshooting

2. Verifica que config.ini existe

3. Asegúrate de que los CSV están en inputs/

4. Consulta la documentación completa en README.md

═══════════════════════════════════════════════════════════════

Versión: 1.0.0
Repositorio: https://github.com/Laikos38/ACOcalculator
Copyright © 2025 ACOCalculator
EOFREADME
}

# Función para copiar archivos comunes
copy_common_files() {
    local dest_dir=$1
    
    # Copiar configuración
    cp config.ini "$dest_dir/"
    
    # Copiar README principal
    cp README.md "$dest_dir/"
    
    # Copiar documentación completa
    mkdir -p "$dest_dir/docs"
    cp docs/*.md "$dest_dir/docs/"
    
    # Crear directorios
    mkdir -p "$dest_dir/inputs"
    mkdir -p "$dest_dir/outputs"
    
    # Crear .gitkeep para que no se pierdan los directorios
    touch "$dest_dir/inputs/.gitkeep"
    touch "$dest_dir/outputs/.gitkeep"
}

# ============================================================================
# RELEASE PARA MACOS
# ============================================================================

if [ -d "dist/ACOCalculator.app" ] || [ -f "dist/ACOCalculator" ]; then
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              📦 Creando Release para macOS                  ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    RELEASE_NAME="ACOCalculator-v${VERSION}-macos"
    mkdir -p "release/${RELEASE_NAME}"
    
    echo "📋 Copiando archivos macOS..."
    
    # Copiar bundle si existe
    if [ -d "dist/ACOCalculator.app" ]; then
        cp -r dist/ACOCalculator.app "release/${RELEASE_NAME}/"
        echo "  ✓ ACOCalculator.app"
    fi
    
    # Copiar ejecutable CLI si existe
    if [ -f "dist/ACOCalculator" ]; then
        cp dist/ACOCalculator "release/${RELEASE_NAME}/"
        chmod +x "release/${RELEASE_NAME}/ACOCalculator"
        echo "  ✓ ACOCalculator (CLI)"
    fi
    
    # Copiar archivos comunes
    copy_common_files "release/${RELEASE_NAME}"
    echo "  ✓ Configuración y documentación"
    
    # Crear README de distribución
    create_readme "macOS" "ACOCalculator.app" "release/${RELEASE_NAME}/LEEME.txt"
    echo "  ✓ LEEME.txt"
    echo ""
    
    echo "🗜️  Comprimiendo release macOS..."
    cd release
    zip -r -q "${RELEASE_NAME}.zip" "${RELEASE_NAME}"
    cd ..
    
    MACOS_SIZE=$(ls -lh "release/${RELEASE_NAME}.zip" | awk '{print $5}')
    echo "✅ Release macOS creado: ${RELEASE_NAME}.zip (${MACOS_SIZE})"
    echo ""
else
    echo "⚠️  No se encontró build de macOS (dist/ACOCalculator.app)"
    echo "   Omitiendo release de macOS..."
    echo ""
fi

# ============================================================================
# RELEASE PARA WINDOWS
# ============================================================================

if [ -f "dist/ACOCalculator.exe" ]; then
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              📦 Creando Release para Windows                ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    RELEASE_NAME="ACOCalculator-v${VERSION}-windows"
    mkdir -p "release/${RELEASE_NAME}"
    
    echo "📋 Copiando archivos Windows..."
    
    # Copiar ejecutable
    cp dist/ACOCalculator.exe "release/${RELEASE_NAME}/"
    echo "  ✓ ACOCalculator.exe"
    
    # Copiar archivos comunes
    copy_common_files "release/${RELEASE_NAME}"
    echo "  ✓ Configuración y documentación"
    
    # Crear README de distribución
    create_readme "Windows" "ACOCalculator.exe" "release/${RELEASE_NAME}/LEEME.txt"
    echo "  ✓ LEEME.txt"
    echo ""
    
    echo "🗜️  Comprimiendo release Windows..."
    cd release
    zip -r -q "${RELEASE_NAME}.zip" "${RELEASE_NAME}"
    cd ..
    
    WINDOWS_SIZE=$(ls -lh "release/${RELEASE_NAME}.zip" | awk '{print $5}')
    echo "✅ Release Windows creado: ${RELEASE_NAME}.zip (${WINDOWS_SIZE})"
    echo ""
else
    echo "⚠️  No se encontró build de Windows (dist/ACOCalculator.exe)"
    echo "   Omitiendo release de Windows..."
    echo ""
fi

# ============================================================================
# RELEASE PARA LINUX
# ============================================================================

# Buscar ejecutable Linux (sin extensión, no .app, no .exe)
if [ -f "dist/ACOCalculator" ] && [ ! -d "dist/ACOCalculator.app" ]; then
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              📦 Creando Release para Linux                  ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Detectar arquitectura
    if command -v uname &> /dev/null; then
        ARCH=$(uname -m)
    else
        ARCH="x86_64"
    fi
    
    RELEASE_NAME="ACOCalculator-v${VERSION}-linux-${ARCH}"
    mkdir -p "release/${RELEASE_NAME}"
    
    echo "📋 Copiando archivos Linux (${ARCH})..."
    
    # Copiar ejecutable
    cp dist/ACOCalculator "release/${RELEASE_NAME}/"
    chmod +x "release/${RELEASE_NAME}/ACOCalculator"
    echo "  ✓ ACOCalculator"
    
    # Copiar archivos comunes
    copy_common_files "release/${RELEASE_NAME}"
    echo "  ✓ Configuración y documentación"
    
    # Crear README de distribución
    create_readme "Linux (${ARCH})" "ACOCalculator" "release/${RELEASE_NAME}/LEEME.txt"
    echo "  ✓ LEEME.txt"
    echo ""
    
    echo "🗜️  Comprimiendo release Linux..."
    cd release
    tar -czf "${RELEASE_NAME}.tar.gz" "${RELEASE_NAME}"
    cd ..
    
    LINUX_SIZE=$(ls -lh "release/${RELEASE_NAME}.tar.gz" | awk '{print $5}')
    echo "✅ Release Linux creado: ${RELEASE_NAME}.tar.gz (${LINUX_SIZE})"
    echo ""
else
    echo "⚠️  No se encontró build de Linux (dist/ACOCalculator)"
    echo "   Omitiendo release de Linux..."
    echo ""
fi

# ============================================================================
# RESUMEN FINAL
# ============================================================================

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║           ✅ RELEASES CREADOS EXITOSAMENTE                  ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

echo "📦 Releases disponibles en: release/"
echo ""
ls -lh release/*.{zip,tar.gz} 2>/dev/null | awk '{print "  " $9 " - " $5}' || echo "  (ninguno)"
echo ""

echo "📊 Contenido de cada release:"
echo "  ✓ Binario ejecutable"
echo "  ✓ config.ini (configuración)"
echo "  ✓ README.md (manual completo)"
echo "  ✓ LEEME.txt (inicio rápido)"
echo "  ✓ docs/ (documentación completa)"
echo "  ✓ inputs/ (directorio para CSVs)"
echo "  ✓ outputs/ (directorio para resultados)"
echo ""

echo "🚀 Instrucciones de distribución:"
echo ""
echo "  macOS:"
echo "    1. Enviar: release/ACOCalculator-v${VERSION}-macos.zip"
echo "    2. Usuario descomprime y doble clic en .app"
echo ""
echo "  Windows:"
echo "    1. Enviar: release/ACOCalculator-v${VERSION}-windows.zip"
echo "    2. Usuario descomprime y doble clic en .exe"
echo ""
echo "  Linux:"
echo "    1. Enviar: release/ACOCalculator-v${VERSION}-linux-*.tar.gz"
echo "    2. Usuario descomprime: tar -xzf archivo.tar.gz"
echo "    3. Ejecuta: ./ACOCalculator"
echo ""

echo "📤 Para subir a GitHub Releases:"
echo "    gh release create v${VERSION} release/*.{zip,tar.gz}"
echo ""
