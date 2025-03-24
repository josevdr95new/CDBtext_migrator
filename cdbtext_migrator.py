import sqlite3
import os
from datetime import datetime
import shutil

def transfer_texts_between_folders():
    # Configuración de carpetas
    en_folder = './en'
    es_folder = './es'
    output_folder = './output'
    log_folder = './logs'

    # Crear carpetas si no existen
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(log_folder, exist_ok=True)

    # Crear archivo log general
    log_filename = f"{log_folder}/name_update_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(log_filename, 'w', encoding='utf-8') as log_file:
        # Obtener lista de archivos en ambas carpetas
        en_files = {f for f in os.listdir(en_folder) if f.endswith('.cdb')}
        es_files = {f for f in os.listdir(es_folder) if f.endswith('.cdb')}

        # Encontrar archivos comunes
        common_files = en_files & es_files
        unique_en = en_files - es_files
        unique_es = es_files - en_files

        # Escribir encabezado en el log
        log_file.write(f"Registro de actualización - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write("=============================================\n\n")

        # Procesar archivos comunes
        total_processed = 0
        for file_name in common_files:
            log_file.write(f"Procesando: {file_name}\n")
            print(f"\nProcesando: {file_name}")

            # Crear rutas de archivos
            en_path = os.path.join(en_folder, file_name)
            es_original_path = os.path.join(es_folder, file_name)
            output_path = os.path.join(output_folder, file_name)

            # Copiar archivo español a la carpeta output
            shutil.copy2(es_original_path, output_path)

            try:
                # Conectar a ambas bases de datos
                conn_en = sqlite3.connect(en_path)
                conn_es = sqlite3.connect(output_path)
                
                cursor_en = conn_en.cursor()
                cursor_es = conn_es.cursor()

                # Obtener textos en inglés
                cursor_en.execute('SELECT id, name FROM texts')
                en_texts = {row[0]: row[1] for row in cursor_en.fetchall()}

                updated_ids = 0
                missing_ids = 0

                # Actualizar textos en la copia española
                for text_id, en_name in en_texts.items():
                    cursor_es.execute('SELECT name FROM texts WHERE id = ?', (text_id,))
                    result = cursor_es.fetchone()
                    
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    if result:
                        current_name = result[0]
                        log_entry = f"[{timestamp}] {file_name} - ID {text_id}: '{current_name}' -> '{en_name}'\n"
                        updated_ids += 1
                        cursor_es.execute('UPDATE texts SET name = ? WHERE id = ?', (en_name, text_id))
                    else:
                        log_entry = f"[{timestamp}] {file_name} - ADVERTENCIA: ID {text_id} no encontrado\n"
                        missing_ids += 1

                    log_file.write(log_entry)

                conn_es.commit()
                log_file.write(f"Actualizados: {updated_ids} | No encontrados: {missing_ids}\n\n")
                total_processed += 1

            except Exception as e:
                log_file.write(f"ERROR en {file_name}: {str(e)}\n\n")
                print(f"Error procesando {file_name}: {str(e)}")
                if conn_es:
                    conn_es.rollback()
            finally:
                if 'conn_en' in locals(): conn_en.close()
                if 'conn_es' in locals(): conn_es.close()

        # Resumen final
        summary = f"\nResumen de la actualización:\n"
        summary += f"Archivos procesados: {len(common_files)}\n"
        summary += f"Archivos únicos en 'en': {len(unique_en)}\n"
        summary += f"Archivos únicos en 'es': {len(unique_es)}\n"
        summary += f"Archivos modificados guardados en: {output_folder}\n"
        
        log_file.write(summary)
        print(summary)

if __name__ == '__main__':
    print("ADVERTENCIA: Este script modificará archivos en la carpeta output.")
    print("Asegúrate de tener backups de las carpetas 'es' y 'en'.")
    confirm = input("¿Ejecutar el script? (s/n): ").lower()
    
    if confirm == 's':
        transfer_texts_between_folders()
    else:
        print("Operación cancelada")