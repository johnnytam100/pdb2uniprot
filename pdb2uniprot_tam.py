# This script maps pdb ID with chain ID in the input formats of 1) tab-delimited table without header OR 2) .csv input to uniprot ID.
# Credit to https://github.com/johnnytam100/pdb2uniprot

# Usage examples
# 1) csv
# python pdb2uniprot_tam.py --input pdb_chain_table.csv --pdb_col PDB_ID --chain_col CHAIN_ID

# 2) tab-delimited table (with header in output)
# python pdb2uniprot_tam.py --input pdb_chain_table

# 3) tab-delimited table (no header in output)
# python pdb2uniprot_tam.py --input pdb_chain_table --no_header

from six.moves.urllib.request import urlopen
import json
import pandas as pd
from argparse import ArgumentParser

### Define command line arguments
parser = ArgumentParser()
parser.add_argument('--input', type=str)
parser.add_argument('--pdb_col', type=str)
parser.add_argument('--chain_col', type=str)
parser.add_argument('--no_header', action='store_true')
args = parser.parse_args()

input = args.input

if not args.no_header:
    header = True
else:
    header = False

if all([args.pdb_col!=None,
        args.chain_col!=None]):
    pdb_col = args.pdb_col
    chain_col = args.chain_col

# load
if input.endswith('.csv'):

    csv_df = pd.read_csv(input)
    pdb_chain_df = csv_df[[pdb_col, chain_col]]
    pdb_chain_df.columns = ['pdb','chain']

else:

    pdb_chain_df = pd.read_csv(input,sep='\t',header=None)
    pdb_chain_df.columns = ['pdb','chain']

# result
result = {'pdb':[],'chain':[],'uniprot':[]}

for pdb, chain in zip(pdb_chain_df['pdb'], pdb_chain_df['chain']):

    print('mapping...', pdb, chain)

    # fetch pdb -> uniprot mapping + check if pdb exists
    try:
        content = urlopen('https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/' + pdb).read()
    except:
        print(pdb,chain,"PDB Not Found (HTTP Error 404). Skipped.")
        continue
    
    content = json.loads(content.decode('utf-8'))

    # check if chain exists
    chain_exist_boo_list = []

    # find uniprot id
    for uniprot in content[pdb.lower()]['UniProt'].keys():

        for mapping in content[pdb.lower()]['UniProt'][uniprot]['mappings']:

            if mapping['chain_id'] == chain:

                result['pdb'].append(pdb)
                result['chain'].append(chain)
                result['uniprot'].append(uniprot)

                chain_exist_boo_list.append(True)

            else:

                chain_exist_boo_list.append(False)

    if not any(chain_exist_boo_list):

        print(pdb,chain,"PDB Found but Chain Not Found. Skipped.")

# result df
result_df = pd.DataFrame(result)

# save
if input.endswith('.csv'):

    # join
    csv_df.set_index([pdb_col, chain_col], inplace=True)
    result_df.columns=[pdb_col,chain_col,'uniprot']
    result_df.set_index([pdb_col,chain_col], inplace=True)
    csv_df = csv_df.join(result_df)

    # save
    csv_df.to_csv(input.replace('.csv','') + '_uniprot.csv', na_rep='NaN', header=header)

else:

    # save
    result_df.to_csv(input + '_uniprot', sep='\t', index=None, na_rep='NaN', header=header)
