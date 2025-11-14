#!/bin/bash
# Script para crear un release distribuible

set -e

cd "$(dirname "$0")/.."

VERSION="1.0.0"
RELEASE_NAME="ACOCalculator-v${VERSION}-macos"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║           CREACIÓN DE RELEASE DISTRIBUIBLE                  ║"
echo "║                   Versión: ${VERSION}                          ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Verificar que el build existe
if [ ! -f "dist/ACOCalculator" ]; then
    echo "❌ Error: No se encontró el ejecutable"
    echo "   Ejecuta primero: ./scripts/build-macos.sh"
    exit 1
fi

echo "📦 Paso 1: Creando estructura de release..."
rm -rf release
mkdir -p release/${RELEASE_NAME}
echo "✅ Estructura creada"
echo ""

echo "📋 Paso 2: Copiando archivos..."
# Copiar bundle
cp -r dist/ACOCalculator.app release/${RELEASE_NAME}/
# Copiar ejecutable CLI
cp dist/ACOCalculator release/${RELEASE_NAME}/
# Copiar configuración
cp config.ini release/${RELEASE_NAME}/
# Copiar README
cp README.md release/${RELEASE_NAME}/
# Crear directorios
mkdir -p release/${RELEASE_NAME}/inputs
mkdir -p release/${RELEASE_NAME}/outputs
echo "✅ Archivos copiados"
echo ""

echo "📝 Paso 3: Creando README de distribución..."
cat > release/${RELEASE_NAME}/LEEME.txt << 'EOFREADME'
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║               ACOCALCULATOR v1.0.0 para macOS               ║
║    Sistema de Gestión de Calificaciones de Moodle          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🚀 INICIO RÁPIDO
═══════════════════════════════════════════════════════════════

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

📁 ESTRUCTURA
═══════════════════════════════════════════════════════════════

inputs/     - Coloca aquí tus archivos CSV de Moodle
outputs/    - Aquí se guardarán los resultados
config.ini  - Configuración del sistema

📖 DOCUMENTACIÓN COMPLETA
═══════════════════════════════════════════════════════════════

Ver README.md para:
- Guía de uso detallada
- Formato de archivos
- Ejemplos
- Solución de problemas

✅ CARACTERÍSTICAS
═══════════════════════════════════════════════════════════════

✓ No requiere Python instalado
✓ Incluye todas las dependencias
✓ Procesamiento automático de calificaciones
✓ Merge de TPs y Parciales
✓ Generación de planillas finales en XLS
✓ Seguimiento de intentos por estudiante

🆘 SOPORTE
═══════════════════════════════════════════════════════════════

Si encuentras problemas:

1. Ejecutar desde terminal para ver errores:
   ./ACOCalculator

2. Verificar que config.ini existe

3. Asegurarse de que los CSV están en inputs/

═══════════════════════════════════════════════════════════════

Versión: 1.0.0
Copyright © 2025 ACOCalculator
EOFREADME
echo "✅ README creado"
echo ""

echo "🗜️  Paso 4: Comprimiendo release..."
cd release
zip -r -q ${RELEASE_NAME}.zip ${RELEASE_NAME}
cd ..
echo "✅ ZIP creado"
echo ""

echo "📊 Paso 5: Información del release..."
echo ""
echo "Tamaño del ZIP:"
ls -lh release/${RELEASE_NAME}.zip | awk '{print "  " $9 ": " $5}'
echo ""
echo "Contenido:"
unzip -l release/${RELEASE_NAME}.zip | head -20
echo ""

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║              ✅ RELEASE CREADO EXITOSAMENTE                 ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📦 Archivo listo para distribuir:"
echo "   release/${RELEASE_NAME}.zip"
echo ""
echo "🚀 Para probar el release:"
echo "   cd release/${RELEASE_NAME}"
echo "   open ACOCalculator.app"
echo ""
echo "📤 Para compartir:"
echo "   Envía el archivo: release/${RELEASE_NAME}.zip"
echo "   El usuario solo necesita:"
echo "   1. Descomprimir el ZIP"
echo "   2. Doble clic en ACOCalculator.app"
echo ""

