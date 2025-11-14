#!/bin/bash
# Script para ejecutar solo tests unitarios

cd "$(dirname "$0")/.."

echo "🧪 Ejecutando tests unitarios..."
echo ""

uv run pytest -m unit "$@"

