#!/bin/bash
# Script para ejecutar todos los tests con pytest

cd "$(dirname "$0")/.."

echo "🧪 Ejecutando tests con pytest..."
echo ""

uv run pytest "$@"

