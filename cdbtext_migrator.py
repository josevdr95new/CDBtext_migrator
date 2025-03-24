import sqlite3
from datetime import datetime

def transfer_texts():
    # Crear archivo log con timestamp
    log_filename = f"name_update_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(log_filename, 'w', encoding='utf-8') as log_file:
        # Conectar a ambas bases de datos
        conn_en = sqlite3.connect('en_cards.cdb')
        conn_es = sqlite3.connect('es_cards.cdb')
        
        cursor_en = conn_en.cursor()
        cursor_es = conn_es.cursor()

        try:
            # Escribir encabezado en el log
            log_file.write(f"Registro de actualización - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write("=============================================\n")

            # Obtener todos los textos en inglés con sus IDs
            cursor_en.execute('SELECT id, name FROM texts')
            en_texts = {row[0]: row[1] for row in cursor_en.fetchall()}

            total_ids = len(en_texts)
            updated_ids = 0
            missing_ids = 0

            # Actualizar los textos en español
            for text_id, en_name in en_texts.items():
                # Verificación
                cursor_es.execute('SELECT name FROM texts WHERE id = ?', (text_id,))
                result = cursor_es.fetchone()
                
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                if result:
                    current_name = result[0]
                    log_entry = f"[{timestamp}] Actualizando ID {text_id}: '{current_name}' -> '{en_name}'\n"
                    updated_ids += 1
                else:
                    log_entry = f"[{timestamp}] ADVERTENCIA: ID {text_id} no encontrado en es_cards.cdb\n"
                    missing_ids += 1
                
                # Escribir en log y mostrar en consola
                log_file.write(log_entry)
                print(log_entry.strip())

                # Ejecutar actualización si existe el ID
                if result:
                    cursor_es.execute('''
                        UPDATE texts
                        SET name = ?
                        WHERE id = ?
                    ''', (en_name, text_id))

            conn_es.commit()
            
            # Resumen final
            summary = f"\nResumen de la actualización:\n"
            summary += f"Total de IDs procesados: {total_ids}\n"
            summary += f"IDs actualizados: {updated_ids}\n"
            summary += f"IDs no encontrados: {missing_ids}\n"
            summary += f"¡Actualización completada con éxito!\n"
            
            log_file.write(summary)
            print(summary)

        except sqlite3.Error as e:
            error_msg = f"\n[{timestamp}] Error: {e}\n"
            log_file.write(error_msg)
            print(error_msg)
            conn_es.rollback()

        finally:
            conn_en.close()
            conn_es.close()
            log_file.write("\nConexiones a BD cerradas")

if __name__ == '__main__':
    print("ADVERTENCIA: ¡Haz backup de ambas bases de datos antes de continuar!")
    confirm = input("¿Ejecutar el script? (s/n): ").lower()
    
    if confirm == 's':
        transfer_texts()
    else:
        print("Operación cancelada")