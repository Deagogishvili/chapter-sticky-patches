# calculate_patches.py
from ProteinPatch import ProteinPatch
from os import listdir, mkdir
from os.path import isfile, isdir, join
import pandas as pd
import yaml

# Load configuration
config = yaml.safe_load(open("../config.yml"))
hydr_residues = config['hydrophobic']
path = config['path']['processed']
result_path = config['path']['result']

# Ensure the result directory exists
if not isdir(result_path):
    print('Output directory does not exist:', result_path, '\nCreating directory')
    mkdir(result_path)

# Iterate through .pdb files and calculate patches
files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.pdb')]
for file in files:
    try:
        id = ''.join(file.split('.')[:-1])
        proteinPatches = ProteinPatch(id, join(path, file), hydr_residues)
        patches = proteinPatches.patches
        result_dict = {'residue_ID': [], 'patch_size': [], 'patch_rank': [], 'residue_type': [], 'protein_id': []}
        for i, patch in enumerate(patches):
            residues_in_patch = patch.get_ids()
            residues = patch.residues()
            for j, residue_in_patch in enumerate(residues_in_patch):
                result_dict['residue_ID'].append(residue_in_patch[-2:])
                result_dict['patch_size'].append(patch.size())
                result_dict['patch_rank'].append(i)
                result_dict['residue_type'].append(residues[j])
                result_dict['protein_id'].append(id)
        pd.DataFrame(result_dict).to_csv(join(result_path, id + '.csv'), index=False)
    except Exception as e:
        print(file, 'failed due to', e)
