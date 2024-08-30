import json
import sqlite3
import os

def load_runs(species_path, db_path):
    # Extract species name and ID from the file name
    name_id = os.path.basename(species_path)
    splitted = name_id.rsplit('_', 1)
    species_name = splitted[0]
    species_id = splitted[-1]
    # Change the current working directory to the species folder
    original_directory = os.getcwd()
    os.chdir(species_path)

    try:
        # Read JSON file if it exists
        json_file = species_name + '.studies.json'
        if os.path.exists(json_file):
            with open(json_file) as file:
                data = json.load(file)

            # Connect to the SQLite database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            try:
                # Execute the appropriate SQL query
                for item in data:
                    for run in item['runs']:
                        # Check if run_id already exists
                        cursor.execute('SELECT COUNT(*) FROM runs WHERE run_id = ?', (run['run_id'],))
                        if cursor.fetchone()[0] == 0:
                            condition = run.get('condition', None)
                            cursor.execute('''
                                INSERT INTO runs (run_id, condition, study_id)
                                VALUES (?, ?, ?)
                            ''', (run['run_id'], condition, item['study_id']))
                        else:
                            print(f"Duplicate run_id found: {run['run_id']}")
                    
                    # Commit the changes to the database
                    conn.commit()
            except sqlite3.Error as e:
                print(f"SQLite error: {e}")
            finally:
                # Close the cursor and the connection
                cursor.close()
                conn.close()
        else:
            print(f"JSON file not found: {json_file}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Change back to the original working directory
        os.chdir(original_directory)







