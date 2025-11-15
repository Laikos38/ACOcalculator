# Scripts de Utilidad - ACOCalculator

Colección de scripts para facilitar el uso del proyecto con UV.

## 📜 Scripts Disponibles

### setup.sh
**Configuración inicial completa del proyecto**

```bash
./scripts/setup.sh
```

Realiza:
- ✅ Verifica que UV esté instalado
- ✅ Crea entorno virtual (`.venv`)
- ✅ Instala todas las dependencias
- ✅ Crea directorios necesarios (`inputs/`, `outputs/`)

Úsalo cuando:
- Clonas el repositorio por primera vez
- Quieres resetear el entorno de desarrollo

---

### run.sh
**Ejecuta el programa principal**

```bash
./scripts/run.sh
```

Ejecuta `main.py` usando el entorno virtual de UV.

Equivalente a: `uv run python main.py`

---

### test.sh
**Ejecuta todos los tests**

```bash
./scripts/test.sh
```

Ejecuta la suite completa de tests con pytest.

Equivalente a: `uv run pytest`

---

### test-unit.sh
**Ejecuta solo tests unitarios**

```bash
./scripts/test-unit.sh
```

Ejecuta únicamente los tests marcados como `@pytest.mark.unit`.

Equivalente a: `uv run pytest -m unit`

---

### test-integration.sh
**Ejecuta solo tests de integración**

```bash
./scripts/test-integration.sh
```

Ejecuta únicamente los tests marcados como `@pytest.mark.integration`.

Equivalente a: `uv run pytest -m integration`

---

### test-coverage.sh
**Ejecuta tests con análisis de cobertura**

```bash
./scripts/test-coverage.sh
```

Ejecuta todos los tests y genera reporte de cobertura en HTML.

Equivalente a: `uv run pytest --cov=src --cov-report=html`

---

## 🏗️ Build Scripts

### build-macos.sh
**Genera ejecutable standalone para macOS**

```bash
./scripts/build-macos.sh
```

Genera binarios que no requieren Python instalado:
- `dist/ACOCalculator` - Ejecutable CLI
- `dist/ACOCalculator.app` - Bundle macOS

**Requisitos:**
- macOS 10.13+
- UV instalado
- 500 MB espacio libre

Equivalente a: `uv run pyinstaller acocalculator.spec --clean`

---

### build-windows.bat
**Genera ejecutable standalone para Windows**

```cmd
scripts\build-windows.bat
```

Genera binario que no requiere Python instalado:
- `dist\ACOCalculator.exe` - Ejecutable Windows

**Requisitos:**
- Windows 10+
- UV instalado
- 500 MB espacio libre

Compatible con CMD, PowerShell y Git Bash.

---

### build-linux.sh
**Genera ejecutable standalone para Linux**

```bash
chmod +x scripts/build-linux.sh
./scripts/build-linux.sh
```

Genera binario que no requiere Python instalado:
- `dist/ACOCalculator` - Ejecutable Linux

**Requisitos:**
- Linux (cualquier distribución)
- UV instalado
- 500 MB espacio libre

**Nota:** El binario funciona solo en la misma arquitectura donde se compiló.

---

### create-release.sh
**Crea paquetes distribuibles para todas las plataformas**

```bash
./scripts/create-release.sh
```

Genera releases completos listos para distribuir:

**Detecta automáticamente:**
- macOS: `release/ACOCalculator-v1.0.0-macos.zip`
- Windows: `release/ACOCalculator-v1.0.0-windows.zip`
- Linux: `release/ACOCalculator-v1.0.0-linux-{arch}.tar.gz`

**Cada release incluye:**
- ✓ Binario ejecutable
- ✓ config.ini (configuración editable)
- ✓ README.md (manual completo)
- ✓ LEEME.txt (inicio rápido por plataforma)
- ✓ docs/ (documentación completa)
- ✓ inputs/ y outputs/ (directorios vacíos)

**Requisitos:**
Debes haber construido los binarios primero con los scripts `build-*.sh`

---

## 🚀 Flujo de Trabajo Típico

### Primera Vez

```bash
# 1. Instalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Configurar proyecto
./scripts/setup.sh

# 3. Ejecutar
./scripts/run.sh
```

### Uso Diario

```bash
# Simplemente ejecutar
./scripts/run.sh
```

### Después de Actualizar Dependencias

```bash
# Reinstalar
./scripts/setup.sh
```

---

## 🔧 Personalización

Todos los scripts están en bash y pueden ser modificados según necesites.

### Ejemplo: Agregar flags al programa

Edita `run.sh`:
```bash
#!/bin/bash
cd "$(dirname "$0")/.."
uv run python main.py --debug "$@"  # Agrega --debug
```

### Ejemplo: Usar Python específico

Edita `setup.sh`:
```bash
uv venv --python 3.11  # Usa Python 3.11
```

---

## 📚 Más Información

- Ver [UV_GUIDE.md](../UV_GUIDE.md) para guía completa de UV
- Ver [QUICK_START.md](../QUICK_START.md) para inicio rápido
- Ver [README.md](../README.md) para documentación completa

