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

### verify.sh
**Verifica la instalación del sistema**

```bash
./scripts/verify.sh
```

Ejecuta el script de verificación que comprueba:
- Versión de Python
- Configuración correcta
- Módulos instalados
- Dependencias externas
- Estructura de directorios

Úsalo para:
- Diagnosticar problemas de instalación
- Verificar que todo está correcto después de setup

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

### build-macos.sh
**Genera ejecutable standalone para macOS**

```bash
./scripts/build-macos.sh
```

Genera binarios que no requieren Python instalado:
- `dist/ACOCalculator` - Ejecutable CLI
- `dist/ACOCalculator.app` - Bundle macOS

Equivalente a: `uv run pyinstaller acocalculator.spec --clean`

---

### create-release.sh
**Crea un paquete distribuible completo**

```bash
./scripts/create-release.sh
```

Crea un ZIP listo para distribuir que incluye:
- Ejecutables
- Configuración
- Documentación
- Directorios necesarios

Salida: `release/ACOCalculator-v1.0.0-macos.zip`

---

## 🚀 Flujo de Trabajo Típico

### Primera Vez

```bash
# 1. Instalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Configurar proyecto
./scripts/setup.sh

# 3. Verificar (opcional)
./scripts/verify.sh

# 4. Ejecutar
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

