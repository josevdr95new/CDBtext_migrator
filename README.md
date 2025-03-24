# CDB Text Migrator

Este script transfiere los campos "name" de una base de datos SQLite en inglés (`en_cards.cdb`) a una base de datos en español (`es_cards.cdb`), generando un registro detallado de los cambios.

## 📋 Requisitos Previos
- Python 3.x instalado.
- Archivos de base de datos `en_cards.cdb` (otras db compatibles entre ellas) y `es_cards.cdb` en el mismo directorio que el script.
- **¡Haz backup de ambas bases de datos antes de ejecutar el script!**

## 🚀 Cómo Usar
1. Coloca los archivos `en_cards.cdb`, `es_cards.cdb` y `cdbtext_migrator.py` en la misma carpeta.
2. Abre una terminal en ese directorio.
3. Ejecuta el script:
   ```bash
   python cdbtext_migrator.py
