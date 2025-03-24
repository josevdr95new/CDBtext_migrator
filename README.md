Migrador de Textos CDB (SQLite)
Script para transferir textos desde archivos .cdb en inglés (en) a sus equivalentes en español (es), actualizando los campos name de la tabla texts.

📋 Tabla de Contenidos
Funcionalidad

Requisitos

Estructura de Carpetas

Instrucciones de Uso

Tablas y Campos Modificados

Logs

Advertencias

✨ Funcionalidad
Transferencia de textos: Actualiza el campo name de la tabla texts en archivos .cdb en español, usando como fuente los textos en inglés.

Manejo de archivos:

Detecta archivos comunes y únicos entre en y es.

Genera copias modificadas en output.

Registro detallado: Crea logs con cambios, errores y estadísticas.

⚙️ Requisitos
Python 3.6+.

Bibliotecas: sqlite3, shutil (incluidas en Python estándar).

Estructura inicial de carpetas: en, es, output, logs.

📂 Estructura de Carpetas
Copy
.
├── en/           # Archivos .cdb en inglés (fuente)
├── es/           # Archivos .cdb en español (destino original)
├── output/       # Archivos modificados (resultado final)
├── logs/         # Registros de operaciones y errores
└── cdbtext_migrator.py  # Script principal
🚀 Instrucciones de Uso
Preparación:

Coloca tus archivos .cdb en inglés en en/ y en español en es/.

Ejecuta desde la terminal:

bash
Copy
python cdbtext_migrator.py
Confirmación:

El script pedirá confirmación antes de ejecutarse:

Copy
¿Ejecutar el script? (s/n): s
Resultados:

Archivos actualizados en output/.

Logs detallados en logs/name_update_log_<fecha>.txt.

🔧 Tablas y Campos Modificados
Tabla: texts

Campo actualizado: name (texto traducible).

Operaciones:

sql
Copy
-- Desde 'en' (lectura)
SELECT id, name FROM texts; 

-- Hacia 'output' (escritura)
UPDATE texts SET name = ? WHERE id = ?;
📝 Logs
Contenido:

IDs actualizados y cambios realizados.

IDs no encontrados en la versión española.

Errores críticos (ej: archivos corruptos).

Ejemplo:

Copy
[2023-10-05 15:30:00] ejemplo.cdb - ID 42: 'Hola' -> 'Hello'
[2023-10-05 15:30:01] ejemplo.cdb - ADVERTENCIA: ID 100 no encontrado
⚠️ Advertencias
¡Haz backups!: El script modifica archivos en output/. Asegúrate de tener copias de seguridad de en/ y es/.

Consistencia de datos: Verifica que los archivos en en/ y es/ tengan la misma estructura de tablas.

📄 Licencia
Distribuido bajo la licencia MIT. Ver LICENSE para más detalles.
