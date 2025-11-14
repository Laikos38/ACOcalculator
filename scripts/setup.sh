#!/bin/bash
# Script de configuración inicial para ACOCalculator con uv

set -e

echo "🚀 Configurando ACOCalculator..."
echo ""

# Verificar que uv esté instalado
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv no está instalado"
    echo "   Instálalo con: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ uv encontrado: $(uv --version)"
echo ""

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    uv venv
    echo "✅ Entorno virtual creado"
else
    echo "✅ Entorno virtual ya existe"
fi
echo ""

# Instalar dependencias
echo "📥 Instalando dependencias..."
uv pip install -e .
echo "✅ Dependencias instaladas"
echo ""

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p inputs outputs
echo "✅ Directorios creados"
echo ""

echo "🎉 ¡Configuración completada!"
echo ""
echo "Para activar el entorno virtual:"
echo "  source .venv/bin/activate"
echo ""
echo "Para ejecutar el programa:"
echo "  uv run python main.py"
echo ""

