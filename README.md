# pdb2uniprot
This script maps pdb ID with chain ID in the input formats of 1) tab-delimited table without header OR 2) .csv to uniprot ID.

# Usage examples


**1) csv**
````
python pdb2uniprot_tam.py --input pdb_chain_table.csv --pdb_col PDB_ID --chain_col CHAIN_ID
````

**2) tab-delimited table (with header in output)**
````
python pdb2uniprot_tam.py --input pdb_chain_table
````

**3) tab-delimited table (no header in output)**
````
python pdb2uniprot_tam.py --input pdb_chain_table --no_header
````
