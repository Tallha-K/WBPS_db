# Bioinformatics Data Processing and Analysis

## Project Overview

This repository contains Python scripts developed as part of my Bioinformatics MSc dissertation project. The scripts are designed for processing and analyzing Gene Expression data acquired from WormBase Parasite, focusing on tasks creating the database, cleaning, loading and managing data

## Repository Structure

### 1. **Production_Code**
   - **create_database_and_tables.py**: This script initializes a database and creates the necessary tables to store biological data.
   - **populate_database_schema.py**: This script populates the database with schema and initial data, preparing it for further analysis.
   - **loaders/**: This directory contains various data loader scripts that are responsible for importing and organizing different types of biological data into the database.

### 2. **Loaders**
   - **species_data_loader.py**: Loads species-related data into the database.
   - **study_data_loader.py**: Handles the loading of study data.
   - **gene_data_loader.py**: Manages the import of gene-related data.
   - **run_data_loader.py**: Imports data related to specific experimental runs.
   - **study_species_data_loader.py**: Loads data linking studies to species.
   - **run_gene_count_tpm_loader.py**: Loads gene count data in TPM (Transcripts Per Million) format for runs.
   - **metadata_loader.py**: Handles the import of metadata associated with the studies and experiments.
   - **differential_expression_loader.py**: Loads data related to differential expression analysis results.

## Prerequisites

- Python 3.x
- Required Python packages
- SQLite3

## Installation

1. Clone the repository:
   
2. Acquire data from FTP (https://ftp.ebi.ac.uk/pub/databases/wormbase/parasite/web_data/rnaseq_studies/releases/current/)

3. Install the required packages above


## Usage

### 1. Database Setup

Open the following script, in an IDE such as Visual Studio Code and define your database name, then run script to create the database and necessary tables:

python create_database_and_tables.py

### 2. Populate Database

Open the following script, in an IDE such as Visual Studio Code, define your database pathway and your data source pathway acquired from the FTP for WBPS.

python populate_database_schema.py


## Contact
For any questions or concerns, please reach out to tallha-khan@hotmail.com

## Acknowledgements and License

This code set was created as a part of my final project BIO702P, for MSc Bioinformatics at Queen Mary University, London. 