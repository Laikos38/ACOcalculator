#!/bin/bash
# Script para generar ejecutable standalone para macOS

set -e  # Salir si hay error

cd "$(dirname "$0")/.."

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║          CONSTRUCCIÓN DE BINARIO PARA MACOS                 ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Verificar que UV esté instalado
if ! command -v uv &> /dev/null; then
    echo "❌ Error: UV no está instalado"
    echo "   Instálalo con: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "📦 Paso 1: Instalando PyInstaller..."
uv sync --group build
echo "✅ PyInstaller instalado"
echo ""

echo "🧹 Paso 2: Limpiando builds anteriores..."
rm -rf build dist *.spec.bak
echo "✅ Limpieza completada"
echo ""

echo "🔨 Paso 3: Construyendo ejecutable..."
uv run pyinstaller acocalculator.spec --clean
echo "✅ Ejecutable construido"
echo ""

echo "📊 Paso 4: Verificando binarios generados..."
echo ""

if [ -f "dist/ACOCalculator" ]; then
    echo "✅ Ejecutable CLI generado:"
    ls -lh dist/ACOCalculator
    echo ""
fi

if [ -d "dist/ACOCalculator.app" ]; then
    echo "✅ Bundle macOS generado:"
    ls -lhd dist/ACOCalculator.app
    echo ""
fi

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║              ✅ CONSTRUCCIÓN COMPLETADA                     ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Binarios generados en: dist/"
echo ""
echo "🚀 FORMAS DE EJECUTAR:"
echo ""
echo "1. Ejecutable CLI:"
echo "   ./dist/ACOCalculator"
echo ""
echo "2. Bundle macOS:"
echo "   open dist/ACOCalculator.app"
echo ""
echo "3. Distribuir:"
echo "   zip -r ACOCalculator-macos.zip dist/ACOCalculator.app"
echo "   # O crear DMG para distribución profesional"
echo ""
echo "📝 NOTA: Los binarios incluyen Python y todas las dependencias."
echo "   No requieren instalación adicional."
echo ""

