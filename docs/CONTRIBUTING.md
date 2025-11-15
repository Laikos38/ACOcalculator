# Guía de Contribución y Desarrollo

## 📐 Arquitectura del Sistema

### Principios de Diseño

1. **Separación de Responsabilidades**: Cada módulo tiene una función específica
2. **Configuración Externa**: Variables configurables en `config.ini`
3. **Modularidad**: Código organizado en packages temáticos
4. **Reutilización**: Funciones comunes en módulo `utils`
5. **Claridad**: Nombres descriptivos y documentación inline

### Flujo de Datos

```
Archivos CSV (inputs/)
    ↓
FileConsolidator (src/utils/)
    ↓
TPManager / ParcialManager (src/managers/)
    ↓
ReportGenerator (src/generators/)
    ↓
Archivos XLS (outputs/)
```

## 🛠️ Agregar Nuevas Funcionalidades

### 1. Agregar un Nuevo Tipo de Evaluación

**Ejemplo: Agregar "Quizzes"**

1. **Actualizar `config.ini`:**
```ini
[Quizzes]
cantidad_quizzes = 3
quiz_prefix = Quiz
```

2. **Crear `src/managers/quiz_manager.py`:**
```python
from ..utils import ConfigLoader, FileConsolidator

class QuizManager:
    def __init__(self, config: ConfigLoader):
        self.config = config
        # ... inicialización similar a TPManager
    
    def mergear_quizzes(self, curso: str):
        # ... lógica de merge
        pass
```

3. **Actualizar `main.py`:**
```python
from src import QuizManager

# En menu():
quiz_manager = QuizManager(config)

# Agregar opción en menú
print("5) Mergear Quizzes")
```

### 2. Agregar Nueva Métrica o Estadística

**Ejemplo: Calcular promedio general**

1. **Agregar función en `src/utils/csv_helpers.py`:**
```python
def calcular_promedio(notas: List[float]) -> float:
    """Calcula el promedio de una lista de notas."""
    notas_validas = [n for n in notas if n != "FALTA"]
    if not notas_validas:
        return 0
    return sum(notas_validas) / len(notas_validas)
```

2. **Usar en managers o generators según necesidad**

### 3. Agregar Nuevo Formato de Salida

**Ejemplo: Exportar a JSON**

1. **Crear `src/generators/json_generator.py`:**
```python
import json
from ..utils import ConfigLoader

class JSONGenerator:
    def generar_json(self, curso: str):
        # ... leer datos mergeados
        # ... convertir a estructura JSON
        # ... guardar archivo
        pass
```

2. **Actualizar menú para incluir nueva opción**

## 🔧 Modificar Configuración

### Variables Disponibles

Todas las variables están en `config.ini` y se acceden mediante `ConfigLoader`:

```python
config = ConfigLoader("config.ini")

# Directorios
source_dir = config.get_source_dir()
output_dir = config.get_output_dir()

# Headers
header_map = config.get_header_map()

# TPs
cantidad_tps = config.get_cantidad_tps()
tp_prefix = config.get_tp_prefix()

# Parciales
cantidad_parciales = config.get_cantidad_parciales()
cantidad_recuperatorios = config.get_cantidad_recuperatorios()

# Formatos
encoding = config.get_csv_encoding()
```

### Agregar Nueva Variable de Configuración

1. **Agregar en `config.ini`:**
```ini
[MiSeccion]
mi_variable = valor
```

2. **Agregar método en `ConfigLoader`:**
```python
def get_mi_variable(self):
    """Retorna mi variable."""
    return self.config.get('MiSeccion', 'mi_variable', fallback='default')
```

## 🧪 Testing (Recomendado)

### Estructura de Tests (Por Implementar)

```
tests/
├── __init__.py
├── test_config_loader.py
├── test_csv_helpers.py
├── test_tp_manager.py
├── test_parcial_manager.py
└── test_report_generator.py
```

### Ejemplo de Test Unitario

```python
import unittest
from src.utils import convertir_nota_a_entero

class TestCSVHelpers(unittest.TestCase):
    def test_convertir_nota_10(self):
        self.assertEqual(convertir_nota_a_entero("10.0"), 10)
    
    def test_convertir_nota_falta(self):
        self.assertEqual(convertir_nota_a_entero(""), "FALTA")
```

## 📝 Convenciones de Código

### Nombres de Variables
- **snake_case** para funciones y variables: `mergear_tps()`, `archivo_filtrado`
- **PascalCase** para clases: `TPManager`, `ConfigLoader`
- **UPPER_CASE** para constantes (si las hay): `DEFAULT_ENCODING`

### Documentación
- **Docstrings** en todas las funciones y clases
- **Comentarios inline** para lógica compleja
- **Type hints** cuando sea apropiado

### Estructura de Archivos
```python
"""
Descripción del módulo.
"""
# Imports estándar
import os
import csv

# Imports de terceros
import xlwt

# Imports locales
from ..utils import ConfigLoader


class MiClase:
    """Descripción de la clase."""
    
    def __init__(self, config: ConfigLoader):
        """
        Inicializa la clase.
        
        Args:
            config: Instancia de ConfigLoader
        """
        self.config = config
```

## 🐛 Debugging

### Logging (Por Implementar)

Recomendación para agregar logging:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='acocalculator.log'
)

logger = logging.getLogger(__name__)
logger.info("Procesando archivo: %s", archivo)
```

### Mensajes de Depuración

El sistema usa emojis para mensajes claros:
- ✅ Éxito
- ⚠️ Advertencia
- ❌ Error
- 📦 Consolidación
- 🔄 Procesamiento
- 📊 Generación de reporte

## 🔄 Workflow de Desarrollo

1. **Crear rama para nueva feature:**
   ```bash
   git checkout -b feature/nombre-feature
   ```

2. **Realizar cambios** siguiendo las convenciones

3. **Probar manualmente** con datos de prueba

4. **Commit y push:**
   ```bash
   git add .
   git commit -m "feat: descripción del cambio"
   git push origin feature/nombre-feature
   ```

5. **Crear Pull Request** (si aplica)

## 📚 Recursos Adicionales

### Dependencias
- **xlwt**: Generación de archivos XLS - [Documentación](https://xlwt.readthedocs.io/)
- **configparser**: Manejo de archivos INI - [Documentación](https://docs.python.org/3/library/configparser.html)

### Formato Moodle CSV
- Los archivos vienen con encoding UTF-8 con BOM
- Separador: coma (,)
- Decimales: pueden ser coma o punto
- Headers pueden variar entre versiones de Moodle

## 💡 Tips y Trucos

### Verificar Sintaxis Rápidamente
```bash
python3 -m py_compile main.py src/**/*.py
```

### Ver Estructura del Proyecto
```bash
find . -name "*.py" -o -name "*.ini" | grep -v __pycache__ | sort
```

### Formatear Código (Opcional)
```bash
pip install black
black .
```

### Lint (Opcional)
```bash
pip install pylint
pylint src/
```

## 🤝 Contacto

Para preguntas o sugerencias sobre el desarrollo del sistema, consulta la documentación en README.md o revisa el código fuente.

---

**¡Gracias por contribuir al proyecto ACOCalculator!**

