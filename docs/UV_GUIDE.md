# Guía de Uso con UV - ACOCalculator

## ¿Qué es UV?

`uv` es un gestor de paquetes y entornos virtuales ultrarrápido para Python, desarrollado por Astral (creadores de Ruff). Es una alternativa moderna a pip/virtualenv que ofrece:

- ⚡ **10-100x más rápido** que pip
- 🔒 **Resolución de dependencias determinista** con archivos lock
- 🎯 **Manejo automático de entornos virtuales**
- 📦 **Compatibilidad total con PyPI**
- 🛠️ **Sintaxis simple y moderna**

## Instalación de UV

### macOS y Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Verificar instalación

```bash
uv --version
```

## Configuración Inicial del Proyecto

### Opción 1: Script Automático (Recomendado)

```bash
# Ejecutar script de configuración
./scripts/setup.sh
```

Este script automáticamente:
- ✅ Verifica que uv esté instalado
- ✅ Crea el entorno virtual (`.venv`)
- ✅ Instala todas las dependencias
- ✅ Crea los directorios necesarios

### Opción 2: Manual

```bash
# 1. Crear entorno virtual
uv venv

# 2. Instalar el proyecto y dependencias
uv pip install -e .

# 3. Crear directorios
mkdir -p inputs outputs
```

## Uso Diario

### Ejecutar el Programa

**Opción A: Con script (más fácil)**
```bash
./scripts/run.sh
```

**Opción B: Con uv directamente**
```bash
uv run python main.py
```

**Opción C: Activando el entorno virtual**
```bash
# Activar entorno
source .venv/bin/activate

# Ejecutar programa
python main.py

# Desactivar cuando termines
deactivate
```

### Verificar Instalación

```bash
./scripts/verify.sh
# o
uv run python verify_installation.py
```

## Gestión de Dependencias

### Ver dependencias instaladas

```bash
uv pip list
```

### Agregar una nueva dependencia

```bash
# Opción 1: Editar pyproject.toml manualmente
nano pyproject.toml
# Luego instalar
uv pip install -e .

# Opción 2: Instalar directamente y luego actualizar pyproject.toml
uv pip install nombre-paquete
```

### Actualizar dependencias

```bash
# Actualizar todas las dependencias
uv pip install --upgrade -e .

# Actualizar una dependencia específica
uv pip install --upgrade nombre-paquete
```

### Regenerar archivo lock

```bash
uv lock
```

## Archivos de Configuración

### pyproject.toml

Archivo principal de configuración del proyecto:

```toml
[project]
name = "acocalculator"
version = "1.0.0"
dependencies = [
    "xlwt==1.3.0",
]
```

### uv.lock

Archivo de bloqueo que garantiza instalaciones reproducibles. **No editar manualmente**.

### .python-version

Especifica la versión de Python a usar (3.13).

## Comandos Útiles

### Crear nuevo entorno virtual

```bash
uv venv [nombre]
```

### Instalar desde requirements.txt (legacy)

```bash
uv pip install -r requirements.txt
```

### Sincronizar entorno con pyproject.toml

```bash
uv pip sync
```

### Desinstalar un paquete

```bash
uv pip uninstall nombre-paquete
```

### Exportar dependencias

```bash
# A requirements.txt
uv pip freeze > requirements.txt

# Ver solo dependencias directas
uv pip list --not-required
```

## Ventajas de UV para este Proyecto

### 1. Velocidad
- Instalación de xlwt: **<1 segundo** (vs 3-5 segundos con pip)
- Resolución de dependencias: **instantánea**

### 2. Reproducibilidad
- `uv.lock` garantiza que todos usen las mismas versiones
- Ideal para colaboración en equipo

### 3. Simplicidad
- Un solo comando: `uv run python main.py`
- No necesitas activar/desactivar entornos manualmente

### 4. Confiabilidad
- Detección automática de conflictos de dependencias
- Menos errores de instalación

## Comparación: pip vs uv

| Operación | pip | uv |
|-----------|-----|-----|
| Crear entorno | `python -m venv .venv` | `uv venv` |
| Activar entorno | `source .venv/bin/activate` | No necesario |
| Instalar deps | `pip install -r requirements.txt` | `uv pip install -e .` |
| Ejecutar script | `python main.py` | `uv run python main.py` |
| Velocidad | ⭐⭐ | ⭐⭐⭐⭐⭐ |

## Solución de Problemas

### "uv: command not found"

```bash
# Reinstalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Agregar al PATH (si es necesario)
export PATH="$HOME/.local/bin:$PATH"
```

### El entorno virtual no funciona

```bash
# Eliminar y recrear
rm -rf .venv
uv venv
uv pip install -e .
```

### Dependencias no se instalan

```bash
# Limpiar cache y reinstalar
uv cache clean
uv pip install -e . --reinstall
```

### Error con xlwt

```bash
# Verificar instalación
uv pip show xlwt

# Reinstalar si es necesario
uv pip install --reinstall xlwt==1.3.0
```

## Workflows Recomendados

### Desarrollo Local

```bash
# 1. Configuración inicial (una sola vez)
./scripts/setup.sh

# 2. Uso diario
./scripts/run.sh
```

### Nuevo Colaborador

```bash
# 1. Clonar repositorio
git clone <repo-url>
cd ACOCalculator

# 2. Instalar uv (si no lo tiene)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Configurar proyecto
./scripts/setup.sh

# 4. Verificar instalación
./scripts/verify.sh

# 5. ¡Listo para usar!
./scripts/run.sh
```

### Actualización de Dependencias

```bash
# 1. Editar pyproject.toml
nano pyproject.toml

# 2. Actualizar instalación
uv pip install -e .

# 3. Actualizar lock file
uv lock

# 4. Commit cambios
git add pyproject.toml uv.lock
git commit -m "Update dependencies"
```

## Recursos Adicionales

- 📚 Documentación oficial: https://docs.astral.sh/uv/
- 🐙 GitHub: https://github.com/astral-sh/uv
- 💬 Discord: https://discord.gg/astral-sh

---

**¡Disfruta de la velocidad de uv! ⚡**

