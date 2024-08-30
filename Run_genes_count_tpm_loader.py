import sqlite3
from pathlib import Path
import pandas as pd
import logging
import logging
import os

# Process_folders_in_directory function calls the process_subdirectory function for each subdirectory in the main directory (species_path folder), 
# which in turn calls the load_gene_data function to load gene data from the tpm_per_run.tsv and counts_per_run.tsv files and the insert_data_to_database function to insert the data into the SQLite database.
# The load_gene_data function reads the tpm_per_run.tsv and counts_per_run.tsv files and combines the data into a single DataFrame. 
# The insert_data_to_database function inserts the data from the DataFrame into the SQLite database. The process_subdirectory function processes a single subdirectory by calling the load_gene_data and 
# insert_data_to_database functions. 
# The process_folders_in_directory function processes all subdirectories in the main directory by calling the process_subdirectory function for each subdirectory.

def load_gene_data(species_path):
    """
    Load gene data from tpm_per_run.tsv and counts_per_run.tsv files.

    Args:
        species_path (str): The path to the directory containing the files.

    Returns:
        df_combined (DataFrame): Combined DataFrame containing gene data from both tpm_per_run.tsv and counts_per_run.tsv files.
    """
    # Search for the study tpm_per_run.tsv file in subdirectories and count_per_run.tsv file
    file_to_find_tpm = next(Path(species_path).rglob('*tpm_per_run.tsv'), None)
    file_to_find_counts = next(Path(species_path).rglob('*counts_per_run.tsv'), None)

    if file_to_find_tpm:
        try:
            # Find the row containing "gene_id" and read the file from that row
            with open(file_to_find_tpm, 'r') as file:
                for i, line in enumerate(file):
                    if "gene_id" in line:
                        break

            df_tpm = pd.read_csv(file_to_find_tpm, sep='\t', index_col=0, skiprows=i)

        except pd.errors.ParserError as e:
            logging.error(f"Error reading TPM file {file_to_find_tpm}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error reading TPM file {file_to_find_tpm}: {e}")
            return None
    else:
        print(f"TPM File not found in {species_path}.")
        return None

    if file_to_find_counts:
        try:
            df_counts = pd.read_csv(file_to_find_counts, sep='\t', index_col=0)
        except pd.errors.ParserError as e:
            logging.error(f"Error reading counts file {file_to_find_counts}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error reading counts file {file_to_find_counts}: {e}")
            return None
    else:
        print(f"Counts File not found in {species_path}.")
        return None

    # Melt the DataFrame to long format for tpm values
    df_tpm_long = df_tpm.reset_index().melt(id_vars=['gene_id'], var_name='run_id', value_name='tpm_value')
    
    # Melt the DataFrame to long format for count values
    df_counts_long = df_counts.reset_index().melt(id_vars=['gene_id'], var_name='run_id', value_name='count_value')

    # Combine the two dataframes based on 'gene_id' and 'run_id'
    df_combined = pd.merge(df_tpm_long, df_counts_long, on=['gene_id', 'run_id'])

    return df_combined


def insert_data_to_database(df_combined, db_path):
    """
    Insert the data from a DataFrame into an SQLite database.

    Args:
        df_combined (DataFrame): The DataFrame containing the data to be inserted.
        db_path (str): The path to the SQLite database.

    Returns:
        None
    """
    if df_combined is not None:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        # Insert the data into the SQLite database
        df_combined.to_sql('run_genes', conn, if_exists='append', index=False)
        # Commit the changes
        conn.commit()
        # Close the connection
        conn.close()
    else:
        print("No data to insert into the database.")

def process_subdirectory(subdirectory_path, db_path):
    """
    Process a subdirectory using two processing functions.

    Args:
        subdirectory_path (Path): The path to the subdirectory.
        db_path (str): The path to the SQLite database.

    Returns:
        None
    """
    print(f"Processing subdirectory: {subdirectory_path}")
    
    # Load gene data
    df_combined = load_gene_data(subdirectory_path)
    
    # Insert data into database
    insert_data_to_database(df_combined, db_path)

def process_folders_in_directory(species_path, db_path):
    """
    Opens each folder in the specified directory and applies two processing functions to the subdirectories.

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
