import json
import sqlite3
import os

def load_studies_species(species_path, db_path):
    # Extract species name and ID from the file name
    name_id = os.path.basename(species_path)
    splitted = name_id.rsplit('_', 1)
    species_name = str(splitted[0])
    species_id = str(splitted[-1])
    
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
                
                # Debug print to check connection
                print("Connected to the database.")
                
                # Iterate over each study in the data list
                for item in data:
                    study_id = item.get('study_id', '')
                                       
                    try:
                        # Execute the SQL query to insert the study into the table
                        cursor.execute('''
                            INSERT INTO study_species (study_id, species_id)
                            VALUES (?, ?)
                        ''', (study_id, species_id))
                    except sqlite3.Error as e:
                        print(f"Error executing SQL query: {e}")
                    
                # Commit the changes to the database after the loop
                conn.commit()
                print("Data committed to the database.")

                # Close the cursor and the connection
                cursor.close()
                conn.close()
        else:
            print(f"File {json_file} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Change back to the original working directory
        os.chdir(original_directory)
