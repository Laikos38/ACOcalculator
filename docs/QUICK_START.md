# Guía de Inicio Rápido - ACOCalculator v1.0

## 🚀 Instalación Rápida con UV (Recomendado)

### 1. Instalar UV (si no lo tienes)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Configurar Proyecto (Todo en uno)
```bash
cd ACOCalculator
./scripts/setup.sh
```

### 3. Ejecutar el Programa
```bash
./scripts/run.sh
# o
uv run python main.py
```

## 📦 Instalación Tradicional con pip

### 1. Verificar Requisitos
```bash
python3 --version  # Debe ser Python 3.8 o superior
```

### 2. Instalar Dependencias
```bash
pip install xlwt
```

### 3. Ejecutar el Programa
```bash
cd ACOCalculator
python3 main.py
```

## 📂 Preparar Archivos

### Estructura Esperada
```
ACOCalculator/
├── inputs/          # ← COLOCA AQUÍ tus archivos CSV de Moodle
│   ├── TP1_1K2.csv
│   ├── TP2_1K2.csv
│   ├── Parcial1_1K2.csv
│   └── ...
└── outputs/         # ← AQUÍ se generarán los resultados
```

### Nomenclatura de Archivos

**Trabajos Prácticos:**
- `TP1_1K2.csv`, `TP2_1K2.csv`, etc.
- Múltiples archivos: `TP1_1K2_1.csv`, `TP1_1K2_2.csv` (se consolidan automáticamente)

**Parciales:**
- `Parcial1_1K2.csv`, `Parcial2_1K2.csv`, etc.

**Recuperatorios:**
- `Recuperatorio1_1K2.csv`, `Recuperatorio2_1K2.csv`, etc.

**✨ Flexibilidad Case-Insensitive:**

El sistema acepta **cualquier combinación de mayúsculas y minúsculas**:

```
✅ VÁLIDOS (todos funcionan igual):
   • TP1_1K15.csv
   • tp1_1k15.csv
   • Tp1_1K15.csv
   • TP1_1k15.csv
   
   • Parcial1_1K2.csv
   • parcial1_1k2.csv
   • PARCIAL1_1K2.csv
   
   • Recuperatorio1_1K4.csv
   • recuperatorio1_1k4.csv
```

> **Nota:** Los archivos de salida siempre se normalizan a mayúsculas para mantener consistencia (ej: `TP1_1K15_filtrado.csv`).

## 🎯 Flujo de Trabajo Típico

### Para Generar Planilla Final del Curso 1K2:

1. **Colocar archivos CSV** en `inputs/`

2. **Ejecutar programa**:
   ```bash
   python3 main.py
   ```

3. **Seleccionar opción 1** (Generar planilla de notas)

4. **Ingresar curso**: `1K2`

5. **Resultado**: `outputs/1K2/Planilla_Final_1K2.xls`

**¡Eso es todo!** El sistema automáticamente:
- ✅ Filtra mejores calificaciones
- ✅ Consolida archivos múltiples
- ✅ Unifica TPs y Parciales
- ✅ Cuenta intentos por TP
- ✅ Crea planilla final consolidada

## 🎛️ Opciones del Menú

### Menú Principal

```
1) Generar planilla de notas (XLS)
   → Crea archivo XLS completo con todo consolidado

2) Operaciones intermedias
   → Accede a operaciones de procesamiento individual
   
h) Ayuda - Abrir manual de usuario
q) Salir
```

### Submenú de Operaciones Intermedias

```
1) Filtrar mejor calificación por alumno
   → Para procesar un archivo CSV individual

2) Unificar TPs
   → Consolida todos los TPs de un curso (incluye intentos)

3) Unificar Parciales
   → Consolida Parciales y Recuperatorios de un curso

v) Volver al menú principal
```

## ⚙️ Personalización Rápida

### Editar `config.ini`:

```ini
[Directorios]
source_dir = inputs    # Cambiar si usas otro directorio
output_dir = outputs   # Cambiar si usas otro directorio

[TrabajoPractico]
cantidad_tps = 4       # Cambiar si tienes más o menos TPs

[Parciales]
cantidad_parciales = 2
cantidad_recuperatorios = 2
```

## 📊 Resultado Final

### Archivo XLS Generado Incluye:

| Apellido | Nombre | ID | TP1 | TP1_Nota | TP1_Intentos | ... | Parcial1 | Parcial1_Nota | ... |
|----------|--------|----|----|---------|-------------|-----|----------|--------------|-----|
| García   | Juan   | 123| 9.5 | 9      | 3           | ... | 8.5      | 8            | ... |
| López    | María  | 456| 8.2 | 8      | 2           | ... | 9.0      | 9            | ... |

**Columnas de seguimiento de intentos:**
- `TP1_Intentos`, `TP2_Intentos`, `TP3_Intentos`, `TP4_Intentos`

## ❓ Preguntas Frecuentes

### ¿Qué pasa si no tengo todos los TPs?
✅ No hay problema. El sistema solo procesa los archivos que existen y deja vacías las columnas de TPs faltantes.

### ¿Puedo cambiar la cantidad de TPs?
✅ Sí, edita `cantidad_tps` en `config.ini`.

### ¿Qué formato deben tener los CSV?
✅ Exportaciones directas de Moodle (UTF-8 con BOM). El sistema maneja diferentes versiones de headers automáticamente.

### ¿Se pierden datos del archivo original?
✅ No, el sistema guarda backups filtrados en `outputs/` y preserva toda la información relevante.

### ¿Puedo procesar múltiples cursos?
✅ Sí, procesa un curso a la vez. Los resultados se organizan en subcarpetas: `outputs/1K2/`, `outputs/1K4/`, etc.

## 🐛 Problemas Comunes

### Error: "No se encontró el archivo de configuración"
**Solución:** Asegúrate de que `config.ini` existe en el directorio raíz.

### Error: "No existe el directorio 'inputs'"
**Solución:** Crea la carpeta `inputs/` y coloca tus archivos CSV allí.

### Error: "Se requiere la librería 'xlwt'"
**Solución:** 
```bash
pip install xlwt
```

### No encuentra las columnas en el CSV
**Solución:** Verifica que el CSV es una exportación válida de Moodle. Puedes personalizar los headers en `config.ini`.

## 📚 Más Información

- **README.md**: Documentación completa
- **CONTRIBUTING.md**: Guía para desarrolladores

## 💡 Tip Pro

Usa la **opción 1 directamente** (Generar planilla de notas) - el sistema preguntará automáticamente si quieres generar los merges necesarios (respuesta por defecto: Sí). Solo presiona Enter dos veces y listo! 🎉

Para operaciones avanzadas de procesamiento individual, usa la **opción 2** (Operaciones intermedias) que te da acceso completo a filtrado y merge de archivos individuales.

---

**¿Necesitas ayuda?** Revisa la documentación completa en README.md

