import sqlite3
import os
import re
from datetime import datetime
import shutil

def replace_quoted_content(original_str, en_str):
    """
    Reemplaza el contenido dentro de comillas dobles de `original_str` 
    con el de `en_str`, conservando el texto fuera de las comillas.
    """
    quoted_spans_es = re.findall(r'"(.*?)"', original_str)
    quoted_spans_en = re.findall(r'"(.*?)"', en_str)
    
    if len(quoted_spans_es) == len(quoted_spans_en):
        new_str = original_str
        for i in range(len(quoted_spans_en)):
            new_str = new_str.replace(f'"{quoted_spans_es[i]}"', f'"{quoted_spans_en[i]}"', 1)
        return new_str
    return original_str  # Mantener original si hay discrepancia

def transfer_texts_between_folders():
    en_folder = './en'
    es_folder = './es'
    output_folder = './output'
    log_folder = './logs'
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(log_folder, exist_ok=True)
    log_filename = f"{log_folder}/update_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open(log_filename, 'w', encoding='utf-8') as log_file:
        en_files = {f for f in os.listdir(en_folder) if f.endswith('.cdb')}
        es_files = {f for f in os.listdir(es_folder) if f.endswith('.cdb')}
        common_files = en_files & es_files

        log_file.write(f"Registro de actualización - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write("=============================================\n\n")

        for file_name in common_files:
            log_file.write(f"Procesando: {file_name}\n")
            print(f"\nProcesando: {file_name}")

            es_original_path = os.path.join(es_folder, file_name)
            output_path = os.path.join(output_folder, file_name)
            shutil.copy2(es_original_path, output_path)

            try:
                conn_en = sqlite3.connect(os.path.join(en_folder, file_name))
                conn_es = sqlite3.connect(output_path)
                cursor_en = conn_en.cursor()
                cursor_es = conn_es.cursor()

                columns = ['name', '"desc"', 'str1', 'str2', 'str3', 'str4', 'str5', 'str6', 'str7']
                cursor_en.execute(f'SELECT id, {", ".join(columns)} FROM texts')
                en_texts = {row[0]: {col: row[i+1] for i, col in enumerate(columns)} for row in cursor_en.fetchall()}

                for text_id, en_data in en_texts.items():
                    cursor_es.execute(f'SELECT {", ".join(columns)} FROM texts WHERE id = ?', (text_id,))
                    es_row = cursor_es.fetchone()
                    
                    if es_row:
                        es_data = {col: val for col, val in zip(columns, es_row)}
                        updates = {}
                        log_entries = []

                        for col in columns:
                            es_val = es_data[col]
                            en_val = en_data.get(col)
                            
                            if col in ['"desc"', 'str1', 'str2', 'str3', 'str4', 'str5', 'str6', 'str7']:
                                if es_val and en_val:
                                    new_val = replace_quoted_content(es_val, en_val)
                                    if new_val != es_val:
                                        updates[col] = new_val
                                        log_entries.append(f"{col}: '{es_val}' → '{new_val}'")
                            else:  # Columna 'name' (reemplazo completo)
                                if en_val and en_val != es_val:
                                    updates[col] = en_val
                                    log_entries.append(f"{col}: '{es_val}' → '{en_val}'")

                        if updates:
                            set_clause = ", ".join([f"{col} = ?" for col in updates.keys()])
                            params = list(updates.values()) + [text_id]
                            cursor_es.execute(f"UPDATE texts SET {set_clause} WHERE id = ?", params)
                            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            log_file.write(f"[{timestamp}] {file_name} - ID {text_id}\n")
                            log_file.write(" | ".join(log_entries) + "\n")

                conn_es.commit()

            except Exception as e:
                log_file.write(f"ERROR en {file_name}: {str(e)}\n\n")
                print(f"Error procesando {file_name}: {str(e)}")
                conn_es.rollback()
            finally:
                conn_en.close()
                conn_es.close()

        summary = f"\nArchivos procesados: {len(common_files)}\n"
        log_file.write(summary)
        print(summary)

if __name__ == '__main__':
    print("ADVERTENCIA: Este script modificará archivos en la carpeta output.")
    confirm = input("¿Ejecutar el script? (s/n): ").lower()
    if confirm == 's':
        transfer_texts_between_folders()
    else:
        print("Operación cancelada")