#!/bin/bash
# Script para generar ejecutable standalone para Linux

set -e  # Salir si hay error

cd "$(dirname "$0")/.."

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║          CONSTRUCCIÓN DE BINARIO PARA LINUX                 ║"
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
    echo "✅ Ejecutable Linux generado:"
    ls -lh dist/ACOCalculator
    echo ""
    
    # Hacer ejecutable
    chmod +x dist/ACOCalculator
    echo "✅ Permisos de ejecución configurados"
    echo ""
fi

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║              ✅ CONSTRUCCIÓN COMPLETADA                     ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📁 Binario generado en: dist/"
echo ""
echo "🚀 FORMAS DE EJECUTAR:"
echo ""
echo "1. Desde terminal:"
echo "   ./dist/ACOCalculator"
echo ""
echo "2. Copiar a cualquier Linux (misma arquitectura):"
echo "   cp dist/ACOCalculator ~/Desktop/"
echo "   ~/Desktop/ACOCalculator"
echo ""
echo "3. Distribuir:"
echo "   tar -czf ACOCalculator-linux-$(uname -m).tar.gz -C dist ACOCalculator"
echo "   # Crea archivo comprimido con arquitectura en el nombre"
echo ""
echo "📝 NOTA: Los binarios incluyen Python y todas las dependencias."
echo "   No requieren instalación adicional."
echo ""
echo "⚠️  IMPORTANTE: El binario Linux solo funciona en la misma"
echo "   arquitectura donde se compiló (x86_64, arm64, etc.)"
echo ""

