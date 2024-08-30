import sqlite3
import os
import glob

def load_genes(species_path, db_path):
    # Extract species ID from the file name
    name_id = os.path.basename(species_path)
    splitted = name_id.rsplit('_', 1)
    species_id = str(splitted[-1])

    # Change the current working directory to the species folder
    original_directory = os.getcwd()
    os.chdir(species_path)

    try:
        # Search for all *.counts_per_run.tsv files in the directory
        all_CPR = glob.glob('**/*.counts_per_run.tsv', recursive=True)

        # Check if any files are found
        if not all_CPR:
            print("No *.counts_per_run.tsv files found in the directory.")
            return

        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Process each file
            for path_to_file in all_CPR:
                with open(path_to_file, 'r') as file:
                    next(file)  # Skip the header row
                    # Iterate over each line in the file
                    for line in file:
                        # Split the line into columns
                        columns = line.strip().split('\t')
                        # Extract the desired column (e.g., column index 0)
                        column_value = columns[0]

                        # Check if the column value already exists in the table
                        cursor.execute("SELECT COUNT(*) FROM genes WHERE gene_id = ?", (column_value,))
                        count = cursor.fetchone()[0]

                        # Insert the column value and species_id into the table if it does not exist
                        if count == 0:
                            cursor.execute("INSERT INTO genes (gene_id, species_id) VALUES (?, ?)", (column_value, species_id))

                    # Commit changes to the database after processing each file
                    conn.commit()
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        finally:
            # Close the cursor and the connection
            cursor.close()
            conn.close()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        # Change back to the original working directory
        os.chdir(original_directory)
