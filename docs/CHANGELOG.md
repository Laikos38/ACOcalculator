# Historial de Cambios - ACOCalculator

## Versión 1.0.0 - Arquitectura Modular Profesional (2025-11-14)

### 🎯 Resumen
Refactorización completa del sistema con arquitectura modular profesional, separación de responsabilidades y nuevas funcionalidades.

### ✨ Nuevas Características

#### 1. Seguimiento de Intentos en TPs
- **Nueva columna `TP{N}_Intentos`**: Registra la cantidad de intentos por alumno en cada TP
- **Conteo automático**: El sistema cuenta todos los intentos de archivos originales múltiples
- **Visible en planilla final**: Los intentos aparecen en el reporte XLS consolidado
- **Utilidad**: Proporciona visibilidad sobre el esfuerzo y persistencia de cada estudiante

#### 2. Sistema de Configuración Externa
- **Archivo `config.ini`**: Configuración en texto plano, fácil de editar
- **Variables configurables**:
  - Directorios de entrada/salida (`source_dir`, `output_dir`)
  - Headers de columnas CSV
  - Cantidad de TPs y Parciales
  - Prefijos de archivos
  - Encoding y formatos de salida
- **Sin modificación de código**: Cambios de configuración sin tocar Python

### 🏗️ Arquitectura Modular

#### Estructura de Packages
```
src/
├── utils/              # Utilidades comunes
│   ├── config_loader.py
│   ├── csv_helpers.py
│   └── file_consolidator.py
├── managers/           # Gestores de lógica de negocio
│   ├── tp_manager.py
│   └── parcial_manager.py
└── generators/         # Generadores de reportes
    └── report_generator.py
```

#### Módulos Creados

**1. `src/utils/config_loader.py`**
- Clase `ConfigLoader` para cargar y gestionar configuración
- Métodos para acceder a todas las variables configurables
- Manejo de valores por defecto (fallbacks)

**2. `src/utils/csv_helpers.py`**
- `get_col_name()`: Búsqueda flexible de columnas
- `convertir_nota_a_entero()`: Conversión de notas a escala entera
- `leer_csv_con_mejores_notas()`: Lectura y filtrado de mejores notas
- `contar_intentos_por_alumno()`: **NUEVA** - Conteo de intentos
- `guardar_csv()`: Guardado de archivos CSV con manejo de directorios

**3. `src/utils/file_consolidator.py`**
- Clase `FileConsolidator` para consolidación de archivos múltiples
- Lógica extraída del main original
- Reutilizable por TPManager y ParcialManager

**4. `src/managers/tp_manager.py`**
- Clase `TPManager` para gestión de Trabajos Prácticos
- Método `mergear_tps()` con soporte de columnas de intentos
- Método `_contar_intentos_archivos_originales()`: **NUEVO**
- Lógica de filtrado de mejores calificaciones

**5. `src/managers/parcial_manager.py`**
- Clase `ParcialManager` para gestión de Parciales y Recuperatorios
- Método `mergear_parciales()`
- Estructura similar a TPManager para consistencia

**6. `src/generators/report_generator.py`**
- Clase `ReportGenerator` para generación de planillas finales
- Método `generar_planilla_final()` con soporte de columnas de intentos
- Manejo de archivos XLS con `xlwt`

### 🔄 Refactorización de main.py

#### Cambios principales:
- **Código reducido**: De 549 líneas a ~120 líneas
- **Uso de módulos**: Importa clases de `src/`
- **Menu mejorado**: Interfaz más clara y profesional
- **Manejo de errores**: Try-catch centralizado
- **Documentación**: Docstrings mejorados

#### Backup:
- `main_backup.py`: Preservación de la versión original

### 📝 Documentación

#### README.md actualizado:
- Sección de Arquitectura Modular
- Documentación del archivo `config.ini`
- Explicación de columnas de intentos
- Características principales
- Ejemplos actualizados con intentos

#### CHANGELOG.md (este archivo):
- Historial de cambios detallado
- Registro de nuevas funcionalidades

### 🔧 Mejoras Técnicas

#### Separación de Responsabilidades:
- **Utils**: Funciones auxiliares reutilizables
- **Managers**: Lógica de negocio específica
- **Generators**: Generación de reportes
- **Main**: Solo orquestación y UI

#### Escalabilidad:
- Fácil agregar nuevos tipos de evaluaciones
- Configuración de cantidades de TPs/Parciales
- Extensible a nuevos formatos de salida

#### Mantenibilidad:
- Código modular y organizado
- Cada archivo tiene una responsabilidad clara
- Nombres descriptivos y consistentes
- Documentación inline (docstrings)

### 📊 Impacto en Salida de Datos

#### Archivos mergeados de TPs:
**Antes (v1.x):**
```csv
Apellido(s),Nombre,Número de ID,TP1,TP1_Nota,TP2,TP2_Nota,...
```

**Con seguimiento de intentos:**
```csv
Apellido(s),Nombre,Número de ID,TP1,TP1_Nota,TP1_Intentos,TP2,TP2_Nota,TP2_Intentos,...
```

#### Planilla Final XLS:
- **Nuevas columnas**: `TP1_Intentos`, `TP2_Intentos`, `TP3_Intentos`, `TP4_Intentos`
- **Total de columnas**: 27 (antes: 19)

### 🐛 Correcciones

#### Manejo Robusto de Archivos Vacíos o Corruptos
- **Validación de headers**: `get_col_name()` ahora detecta cuando `fieldnames` es `None` o está vacío
- **Validación en procesamiento**: `FileConsolidator._filter_best_grade()` valida headers antes de procesar
- **Manejo de errores graceful**: `TPManager` y `ParcialManager` capturan `ValueError` y `KeyError` mostrando mensajes claros
- **Mensajes informativos**: Los errores muestran el nombre del archivo y la causa del problema
- **Sin crashes**: El programa continúa funcionando aunque un archivo falle
- **Tests completos**: 9 nuevos tests unitarios en `tests/unit/test_empty_files.py` que cubren:
  - Archivos completamente vacíos
  - Archivos con solo headers (sin datos)
  - Archivos con columnas faltantes o incorrectas
  - Archivos con solo espacios en blanco
  - Archivos con headers corruptos
  - Casos extremos (una sola fila, etc.)

#### Otras Correcciones
- Todas las funcionalidades originales preservadas
- Compatibilidad con archivos de entrada existentes

### ⚠️ Breaking Changes

- **Ninguno para usuarios finales**: Los archivos de entrada y el flujo de trabajo son idénticos
- **Para desarrolladores**: Si modificaste el código original, necesitarás adaptar tus cambios a la nueva estructura modular

### 🔜 Mejoras Futuras Sugeridas

- [ ] Tests unitarios para cada módulo
- [ ] Interfaz gráfica (GUI) opcional
- [ ] Exportación a otros formatos (XLSX, PDF)
- [ ] Logs detallados de procesamiento
- [ ] Estadísticas adicionales (promedios, medianas)
- [ ] Gráficos de rendimiento por curso
- [ ] API REST para integración con otros sistemas


