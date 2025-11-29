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
