import os

from loaders import Species_loader  # Import the loader for species data
from loaders import Studies_loader  # Import the loader for studies data
from loaders import Genes_loader  # Import the loader for genes data
from loaders import Runs_loader  # Import the loader for runs data
from loaders import Studies_species_loader  # Import the loader for studies_species data
from loaders import Run_genes_count_tpm_loader  # Import the loader for run_genes_count_tpm data
from loaders import Metadata_loader  # Import the loader for metadata data
from loaders import Differential_Expression_loader  # Import the loader for differential_expression data

# Set the file_path and db_path, consider using r'' for Windows paths
file_path = ""  # Set the path to the chosen directory
db_path = ""  # Set the path to the database


# Get the path to the chosen in the file_path directory
for root, dirs, files in os.walk(file_path):
    if dirs:  # Check if there are directories in the current root
        species_folder = dirs[4]  # CHOOSE FOLDER INDEX HERE
        species_path = os.path.join(root, species_folder)
        break  # Exit the loop after finding the first directory
else:
    species_path = None  # No directories found

print("Populating database with data from:", species_path)
print("Populating database at:", db_path)

# Load data into the database
try:
    print("     Loading species data...")
    Species_loader.load_species_data(species_path, db_path) # Load species data into the database
    print("         Species data loaded successfully.")
except Exception as e:
    print("         Error loading species data:", str(e))

try:
    print("     Loading studies data...")
    Studies_loader.load_studies(species_path, db_path) # Load studies data into the database
    print("         Studies data loaded successfully.")
except Exception as e:
    print("         Error loading studies data:", str(e))

try:
    print("     Loading genes data...")
    Genes_loader.load_genes(species_path, db_path) # Load genes data into the database
    print("         Genes data loaded successfully.")
except Exception as e:
    print("         Error loading genes data:", str(e))

try:
    print("     Loading runs data...")
    Runs_loader.load_runs(species_path, db_path) # Load runs data into the database
    print("         Runs data loaded successfully.")
except Exception as e:
    print("         Error loading runs data:", str(e))

try:
    print("     Loading studies_species data...")
    Studies_species_loader.load_studies_species(species_path, db_path) # Load studies_species data into the database
    print("         Studies_species data loaded successfully.")
except Exception as e:
    print("         Error loading studies_species data:", str(e))

try:
    print("     Processing run_genes_count_tpm data...")
    Run_genes_count_tpm_loader.process_folders_in_directory(species_path, db_path) # Process folders in the species_path directory to load run_genes_count_tpm data into the database
    print("         Run_genes_count_tpm data processed successfully.")
except Exception as e:
    print("         Error processing run_genes_count_tpm data:", str(e))

try:
    print("     Processing metadata data...")
    Metadata_loader.process_folders_in_directory(species_path, db_path) # Process folders in the species_path directory to load metadata data into the database
    print("         Metadata data processed successfully.")
except Exception as e:
    print("         Error processing metadata data:", str(e))

try:
    print("     Loading differential_expression data...")
    Differential_Expression_loader.process_folders_in_directory(species_path, db_path) # Process folders in the species_path directory to load differential_expression data into the database
    print("         Differential_expression data loaded successfully.")
except Exception as e:
    print("         Error loading differential_expression data:", str(e))

print("Data loading and processing complete for " + species_path)
