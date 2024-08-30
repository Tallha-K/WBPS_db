import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')

# Create a cursor object
cursor = conn.cursor()

# List of SQL commands to create indexes
index_commands = [
    # Indexes for the species table
    '''CREATE INDEX idx_species_name ON species (species_name);''',
    
    # Indexes for the studies table
    '''CREATE INDEX idx_study_category ON studies (study_category);''',
    '''CREATE INDEX idx_study_name ON studies (study_name);''',
    
    # Indexes for the genes table
    '''CREATE INDEX idx_species_id ON genes (species_id);''',
    
    # Indexes for the runs table
    '''CREATE INDEX idx_study_id ON runs (study_id);''',
    '''CREATE INDEX idx_condition ON runs (condition);''',
    
    # Indexes for the study_species table
    '''CREATE INDEX idx_study_species ON study_species (study_id, species_id);''',
    
    # Indexes for the run_genes table
    '''CREATE INDEX idx_run_id ON run_genes (run_id);''',
    '''CREATE INDEX idx_gene_id ON run_genes (gene_id);''',
    
    # Indexes for the differential_expression table
    '''CREATE INDEX idx_gene_id ON differential_expression (gene_id);''',
    '''CREATE INDEX idx_conditions ON differential_expression (condition_1, condition_2);''',
    '''CREATE INDEX idx_study_id ON differential_expression (study_id);'''
]

# Execute each command in the index_commands list
for command in index_commands:
    cursor.execute(command)

# Commit the changes
conn.commit()

# Close the connection
conn.close()
