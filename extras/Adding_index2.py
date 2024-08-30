import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')

# Create a cursor object
cursor = conn.cursor()

# List of SQL commands to create indexes
index_commands = [
    # Indexes for the species table
    '''CREATE INDEX idx_species_name ON species (species_name);''',   
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
