@echo off
REM Script para generar ejecutable standalone para Windows
REM Ejecutar desde CMD o PowerShell

cd /d "%~dp0\.."

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║          CONSTRUCCION DE BINARIO PARA WINDOWS               ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

REM Verificar que UV este instalado
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error: UV no esta instalado
    echo    Instalalo desde: https://github.com/astral-sh/uv
    echo    O con: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    exit /b 1
)

echo 📦 Paso 1: Instalando PyInstaller...
uv sync --group build
echo ✅ PyInstaller instalado
echo.

echo 🧹 Paso 2: Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec.bak del /q *.spec.bak
echo ✅ Limpieza completada
echo.

echo 🔨 Paso 3: Construyendo ejecutable...
uv run pyinstaller acocalculator.spec --clean
echo ✅ Ejecutable construido
echo.

echo 📊 Paso 4: Verificando binarios generados...
echo.

if exist "dist\ACOCalculator.exe" (
    echo ✅ Ejecutable Windows generado:
    dir "dist\ACOCalculator.exe"
    echo.
)

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║              ✅ CONSTRUCCION COMPLETADA                     ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📁 Binario generado en: dist\
echo.
echo 🚀 FORMAS DE EJECUTAR:
echo.
echo 1. Doble clic en:
echo    dist\ACOCalculator.exe
echo.
echo 2. Desde CMD/PowerShell:
echo    .\dist\ACOCalculator.exe
echo.
echo 3. Distribuir:
echo    Comprime dist\ACOCalculator.exe en un ZIP
echo    o usa un instalador como InnoSetup/NSIS
echo.
echo 📝 NOTA: El ejecutable incluye Python y todas las dependencias.
echo    No requiere instalacion adicional.
echo.

