#!/bin/bash
# Script para ejecutar tests con reporte de cobertura

cd "$(dirname "$0")/.."

echo "🧪 Ejecutando tests con análisis de cobertura..."
echo ""

uv run pytest --cov=src --cov-report=term-missing --cov-report=html "$@"

echo ""
echo "📊 Reporte HTML de cobertura generado en: htmlcov/index.html"

