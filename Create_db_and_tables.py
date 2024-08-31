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
