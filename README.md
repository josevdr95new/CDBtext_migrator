# 🛠️ Migrador de Textos CDB (SQLite)

**Script para sincronizar textos entre archivos `.cdb` (inglés → español)**  
Actualiza automáticamente el campo `name` de la tabla `texts` manteniendo la integridad de los datos.

---

## 📌 Tabla de Contenidos
- [Funcionalidad](#✨-funcionalidad)
- [Requisitos](#⚙️-requisitos)
- [Estructura de Carpetas](#📂-estructura-de-carpetas)
- [Instrucciones](#🚀-instrucciones)
- [Tablas Modificadas](#🔧-tablas-modificadas)
- [Ejemplo de Logs](#📝-ejemplo-de-logs)
- [Advertencias](#⚠️-advertencias)
- [Licencia](#📄-licencia)

---

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
