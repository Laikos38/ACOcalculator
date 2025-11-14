#!/bin/bash
# Script para ejecutar solo tests de integración

cd "$(dirname "$0")/.."

echo "🧪 Ejecutando tests de integración..."
echo ""

uv run pytest -m integration "$@"

