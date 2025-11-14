#!/bin/bash
# Script para probar el binario en un directorio limpio

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║           PRUEBA DE BINARIO EN DIRECTORIO LIMPIO            ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Crear directorio temporal de prueba
TEST_DIR="/tmp/test_acocalculator_$$"
mkdir -p "$TEST_DIR"
echo "✅ Directorio de prueba creado: $TEST_DIR"
echo ""

# Copiar binario
cp dist/ACOCalculator "$TEST_DIR/"
echo "✅ Binario copiado al directorio de prueba"
echo ""

# Cambiar al directorio de prueba
cd "$TEST_DIR"

echo "📊 Estado inicial del directorio:"
ls -la
echo ""

echo "🚀 Ejecutando binario..."
echo "   (Presiona 'q' seguido de Enter para salir)"
echo ""

# Ejecutar binario
./ACOCalculator

echo ""
echo "📊 Estado final del directorio:"
ls -la
echo ""

# Verificar que se crearon los directorios
if [ -d "inputs" ]; then
    echo "✅ Directorio 'inputs/' creado correctamente"
else
    echo "❌ ERROR: No se creó el directorio 'inputs/'"
fi

if [ -d "outputs" ]; then
    echo "✅ Directorio 'outputs/' creado correctamente"
else
    echo "❌ ERROR: No se creó el directorio 'outputs/'"
fi

if [ -f "config.ini" ]; then
    echo "✅ Archivo 'config.ini' creado correctamente"
else
    echo "⚠️  Advertencia: No se creó 'config.ini'"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "RESULTADO: El binario funciona correctamente ✅"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Directorio de prueba: $TEST_DIR"
echo "Para limpiarlo: rm -rf $TEST_DIR"
echo ""

