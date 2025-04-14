# Extractor de Pares Item Name - Alias

Script Python que extrae y procesa pares de datos "Item Name" y "Alias" de archivos de configuración de sistemas LonWorks. Detecta automáticamente la codificación, procesa archivos grandes y exporta los resultados a CSV. Ideal para migración de configuraciones, documentación y análisis de dispositivos.

## Características
- Detección automática de codificación (UTF-16, UTF-8)
- Procesamiento eficiente de archivos grandes
- Múltiples patrones de búsqueda
- Exportación a CSV
- Estadísticas del proceso

## Requisitos
- Python 3.x
- Bibliotecas estándar: csv, re, os, sys

## Uso
```bash
python extract_pairs.py
```

El script procesará automáticamente el archivo `pru.txt` y generará `item_alias_pairs.csv` con los resultados. 