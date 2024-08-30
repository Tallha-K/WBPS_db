import sqlite3

# Define database name here (e.g. "database.db")
Database_Name = ""


# Connect to a new database or create it if it doesn't exist
conn = sqlite3.connect(Database_Name)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# List of table creation commands
table_commands = [
    '''
    CREATE TABLE species (
        species_id TEXT PRIMARY KEY,
        species_name TEXT UNIQUE NOT NULL,
        alternative_species_id TEXT UNIQUE
    )
    ''',
    '''
    CREATE TABLE studies (
        study_id TEXT PRIMARY KEY,
        study_category TEXT,
        study_name TEXT,
        link TEXT
    )
    ''',
    '''
    CREATE TABLE genes (
        gene_id TEXT PRIMARY KEY,
        species_id TEXT,
        FOREIGN KEY (species_id) REFERENCES species (species_id)
    )
    ''',
    '''
    CREATE TABLE runs (
        run_id TEXT PRIMARY KEY,
        condition TEXT,
        study_id TEXT,
        metadata TEXT,
        FOREIGN KEY (study_id) REFERENCES studies (study_id)
    )
    ''',
    '''
    CREATE TABLE study_species (
        study_id TEXT,
        species_id TEXT,
        FOREIGN KEY (study_id) REFERENCES studies (study_id),
        FOREIGN KEY (species_id) REFERENCES species (species_id)
    )
    ''',
    '''
    CREATE TABLE run_genes (
        run_id TEXT,
        gene_id TEXT,
        count_value FLOAT,
        tpm_value FLOAT,
        FOREIGN KEY (run_id) REFERENCES runs (run_id),
        FOREIGN KEY (gene_id) REFERENCES genes (gene_id)
    )
    ''',
    '''
    CREATE TABLE differential_expression (
        gene_id TEXT,
        log2FoldChange FLOAT, 
        adj_p_value FLOAT,  
        condition_1 INTEGER,  
        condition_2 INTEGER, 
        study_id TEXT,
        FOREIGN KEY (gene_id) REFERENCES genes (gene_id),
        FOREIGN KEY (condition_1) REFERENCES runs (condition),
        FOREIGN KEY (condition_2) REFERENCES runs (condition),
        FOREIGN KEY (study_id) REFERENCES studies (study_id)
    )
    '''
]

print("Creating database tables...")

# Execute each table creation command
for command in table_commands:
    cursor.execute(command)
    conn.commit()

# Commit the changes and close the connection
conn.close()

print(Database_Name + " created successfully.")
