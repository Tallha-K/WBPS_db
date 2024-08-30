from pathlib import Path
import pandas as pd
import sqlite3
import os

def split_dataframe(df_de, group_size=2):
    """
    Split the DataFrame into smaller DataFrames based on column groups.

    Args:
        df_de (DataFrame): The DataFrame to split.
        group_size (int): The number of columns per split DataFrame.

    Returns:
        List[Tuple[str, DataFrame]]: A list of tuples, each containing the name and DataFrame.
    """
    df_names = []
    cols = df_de.columns

    for i in range(0, len(cols), group_size):
        group_cols = cols[i:i + group_size]
        new_df = df_de[group_cols].copy()  # **[NEW] Create a copy of the DataFrame for safe manipulation**
        new_df.reset_index(inplace=True)   # **[NEW] Turn the index into a column**
        df_name = f'df_de{i // group_size + 1}'
        df_names.append((df_name, new_df))
    
    return df_names


def load_de_data(subdirectory_path):
    """
    Load DE data from a subdirectory.

    Args:
        subdirectory_path (Path): The path to the subdirectory.

    Returns:
        DataFrame: The loaded and processed DE data, or None if the data could not be loaded.
    """
    # Suppress SettingWithCopyWarning
    pd.options.mode.chained_assignment = None  # default='warn'
    
    all_dfs = []
    
    # Find all files that match the pattern '*de.*.tsv'
    files_to_find_de = list(Path(subdirectory_path).rglob('*de.*.tsv'))
    
    for file_path in files_to_find_de:
        dfs_to_concat = []

        print(f"Processing file: {file_path}")

        # Find the row containing "gene_id" and record its index
        with open(file_path, 'r') as file:
            for i, line in enumerate(file):
                if "gene_id" in line:
                    print(f"Found 'gene_id' in file {file_path} at row {i}")
                    # Read the file starting from the row with "gene_id"
                    df_from_tsv = pd.read_csv(file_path, sep='\t', index_col=0, skiprows=i)

                    split_dfs = split_dataframe(df_from_tsv, group_size=2)

                    # Process each split DataFrame
                    for name, df_temp in split_dfs:
                        if df_temp.empty:
                            print(f"Skipping empty DataFrame: {name}")
                            continue
                        # Retrieve the name of the first column from the current split DataFrame
                        column_name = df_temp.columns[1]
                        # Split the column name into two variables based on " vs "
                        try:
                            condition_1, condition_2 = column_name.split(' vs ')
                        except ValueError:
                            print(f"Column name '{column_name}' does not contain ' vs '")
                            continue
                        # Add new columns 'condition_1' and 'condition_2' to the current split DataFrame
                        df_temp['condition_1'] = condition_1
                        df_temp['condition_2'] = condition_2
                        # Rename columns for clarity
                        df_temp.rename(columns={
                            df_temp.columns[1]: 'log2FoldChange',
                            df_temp.columns[2]: 'adj_p_value'
                        }, inplace=True)
                        # Append the DataFrame to the list
                        dfs_to_concat.append(df_temp)
        
        # Check if dfs_to_concat is empty before concatenation
        if not dfs_to_concat:
            print(f"No DataFrames to concatenate for file {file_path}")
            continue

        # Concatenate the DataFrames for the current file
        combined_df = pd.concat(dfs_to_concat)
        # Sort the DataFrame by index 
        sorted_df = combined_df.sort_index()
        # Add a column for the study_id
        sorted_df['study_id'] = os.path.basename(os.path.dirname(file_path))
        # Append the sorted DataFrame to the list
        all_dfs.append(sorted_df)
        print(f"Concatenated DataFrame for file {file_path} added to all_dfs")
    return all_dfs
    


def insert_data_to_database(all_dfs, db_path):
    """
    Insert the data from a list of DataFrames into an SQLite database.

    Args:
        df_combined (List[DataFrame]): The list of DataFrames containing the data to be inserted.
        db_path (str): The path to the SQLite database.

    Returns:
        None
    """
    if all_dfs:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        
        # Iterate through each DataFrame in the list
        for x in all_dfs:
            # Insert the data into the SQLite database
            x.to_sql('differential_expression', conn, if_exists='append', index=False)
        
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
    
    # Load de data
    all_dfs = load_de_data(subdirectory_path)
    
    # Insert data into database
    insert_data_to_database(all_dfs, db_path)

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
