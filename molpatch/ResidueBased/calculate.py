from ProteinPatch import ProteinPatch
from Bio.PDB.DSSP import dssp_dict_from_pdb_file
from os import listdir, mkdir
from os.path import isfile, isdir, join
from PisiteParser import PisiteParser
import pandas as pd
import yaml
config = yaml.safe_load(open("../config.yml"))
hydr_residues = config['hydrophobic']

path = '../data/chain/'
result_path = '../data/result/'
figure_path = '../data/figures/'

if not isdir(result_path):
    print('Output directory does not exist:', result_path, '\n Creating directory')
    mkdir(result_path)
if not isdir(figure_path):
    print('Output directory does not exist:', figure_path, '\n Creating directory')
    mkdir(figure_path)

df = pd.DataFrame()

files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.pdb')]
for file in files:
    print(path+file)
    id = ''.join(file.split('.')[:-1])
    print(id)
    proteinPatches = ProteinPatch(id,path+file,hydr_residues)
    print("patches calculated")
    patches = proteinPatches.patches
    result_dict = {'residue_ID':[], 'patch_size':[], 'patch_rank':[], 'residue_type':[], 'protein_id':[]}
    for i,patch in enumerate(patches):
        residues_in_patch = patch.get_ids()
        residues = patch.residues()

        for j, residue_in_patch in enumerate(residues_in_patch):
            result_dict['residue_ID'].append(residue_in_patch[-2:])
            result_dict['patch_size'].append(patch.size())
            result_dict['patch_rank'].append(i)
            result_dict['residue_type'].append(residues[j])
            result_dict['protein_id'].append(id)
    print("writing file")
    pd.DataFrame(result_dict).to_csv(result_path + id + '.csv', index=False)
    plotfile = figure_path + id + '.png'
    proteinPatches.plot_largest_patches(plotfile)

