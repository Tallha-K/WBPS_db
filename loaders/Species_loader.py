import sqlite3
import os

def load_species_data(species_path, db_path):
    # Extract the current directory name
    name_id = os.path.basename(species_path)
    # split everything before and after the last underscore in the species_id
    splitted = name_id.rsplit('_', 1)

    species_name = str(splitted[0])
    species_id = str(splitted[-1])

    # Print the species being loaded
    print(f"Loading species: {species_name} with ID: {species_id}")

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute the appropriate SQL query
    cursor.execute("INSERT INTO species (species_id, species_name, alternative_species_id) VALUES (?, ?, ?)", (species_id, species_name, None))

    # Commit the changes to the database
    conn.commit()
    # Close the cursor and the connection
    cursor.close()
    conn.close()
