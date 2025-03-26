# 🛠️ Migrador de Textos CDB (SQLite)

**Script para sincronizar textos entre archivos `.cdb` (inglés → español)**  
Actualiza automáticamente el campo `name` de la tabla `texts` manteniendo la integridad de los datos.

## ✨ Funcionalidad
- ✅ **Transferencia de textos**:  
  Reemplaza el campo `name` en archivos `.cdb` en español con los valores de la versión inglesa.
- 🔍 **Detección inteligente**:  
  Identifica archivos comunes y únicos entre las carpetas `en` y `es`.
- 📂 **Manejo seguro**:  
  Crea copias modificadas en `output` sin alterar los archivos originales.
- 📝 **Registro detallado**:  
  Genera logs con cambios, errores y estadísticas en tiempo real.

---

## ⚙️ Requisitos
- **Python 3.6+** ([Descarga aquí](https://www.python.org/downloads/)).
- **Bibliotecas nativas**:  
  ```bash
  sqlite3 | shutil | os | datetime
  ```
 ## 😊 Ejecutar el script:
  ```bash
  python cdbtext_migrator.py
   ```
## cdb full
https://github.com/josevdr95new/cdbespa-alternativo
