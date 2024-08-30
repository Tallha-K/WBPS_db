import sqlite3
import json
from pathlib import Path
import pandas as pd

def load_metadata_to_database(species_path):
    """
    Load metadata from a TSV file into a DataFrame.

    Args:
        species_path (str): The path to the directory containing the metadata file.

    Returns:
        df_transformed (DataFrame): DataFrame containing 'run_id' and 'metadata' columns.
    """
    # Search for the study metadata_per_run.tsv file in subdirectories
    file_to_find_metadata = next(Path(species_path).rglob('*metadata_per_run.tsv'), None)
    
    if file_to_find_metadata is None:
        print(f"Metadata file not found in {species_path}.")
        return None

    # Read the TSV file as a DataFrame
    df = pd.read_csv(file_to_find_metadata, delimiter='\t')

    # Function to create dictionary from row excluding the first column
    def row_to_dict(row):
        return row[1:].to_dict()

    # Apply the function to each row and create new DataFrame
    df['metadata'] = df.apply(row_to_dict, axis=1)
    # Rename the first column to 'run_id'
    df.rename(columns={df.columns[0]: 'run_id'}, inplace=True)
    # Keep only the 'run_id' and 'metadata' columns
    df_transformed = df[['run_id', 'metadata']]

    df_transformed = df_transformed.map(lambda x: None if pd.isna(x) else x)

    return df_transformed

def insert_data_to_database(df_transformed, db_path):
    """
    Insert the data from a DataFrame into an SQLite database.

    Args:
        df_transformed (DataFrame): The DataFrame containing the data to be inserted.
        db_path (str): The path to the SQLite database.

    Returns:
        None
    """
    if df_transformed is None:
        print("No data to insert into the database.")
        return

    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Update existing record if run_id exists
    for _, row in df_transformed.iterrows():
        run_id = row['run_id']
        metadata = json.dumps(row['metadata'])
        cursor.execute("UPDATE runs SET metadata = ? WHERE run_id = ?", (metadata, run_id))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Data has been successfully inserted into the database.")

def process_subdirectory(subdirectory_path, db_path):
    """
    Process a subdirectory using processing functions.

    Args:
        subdirectory_path (Path): The path to the subdirectory.
        db_path (str): The path to the SQLite database.

    Returns:
        None
    """
    print(f"Processing subdirectory: {subdirectory_path}")
    
    # Load metadata to database
    df_transformed = load_metadata_to_database(subdirectory_path)
    
    # Insert data into database
    insert_data_to_database(df_transformed, db_path)

def process_folders_in_directory(species_path, db_path):
    """
    Opens each folder in the specified directory and applies processing functions to the subdirectories.

    Args:
        species_path (str): The path to the main directory containing subdirectories.
        db_path (str): The path to the SQLite database.

    Returns:
        None
    """
    # Iterate through each subdirectory in the main directory
    for subdirectory in Path(species_path).iterdir():
        if subdirectory.is_dir():
            process_subdirectory(subdirectory, db_path)
