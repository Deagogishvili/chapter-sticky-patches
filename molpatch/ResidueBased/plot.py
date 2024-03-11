from ProteinPatch import ProteinPatch
import yaml
import sys
from os.path import join, isdir
from os import mkdir

config = yaml.safe_load(open("../config.yml"))
hydr_residues = config['hydrophobic']
path = config['path']['processed']
figure_path = config['path']['figure']
processed_path = config['path']['processed']

if not isdir(processed_path):
    print('Output directory does not exist:', figure_path, '\nCreating directory')
    exit()

if not isdir(figure_path):
    print('Output directory does not exist:', figure_path, '\nCreating directory')
    mkdir(figure_path)

# Process single PDB file
pdb_filename = sys.argv[1]  # The PDB filename is expected as the first argument
try:
    id = ''.join(pdb_filename.split('.')[:-1])
    print(join(path, pdb_filename))
    proteinPatches = ProteinPatch(id, join(path, pdb_filename), hydr_residues)
    plotfile = join(figure_path, id + '.png')
    proteinPatches.plot_largest_patches(plotfile)
except Exception as e:
    print(pdb_filename, 'failed due to', e)
