#!/usr/bin/python3

# Preprocessing of PDB files for MolPatch
from Bio.PDB.DSSP import dssp_dict_from_pdb_file
from Bio.PDB import Select, PDBIO
from Bio.PDB.PDBParser import PDBParser
#from Bio.PDB.MMCIFParser import MMCIFParser
from os import listdir, mkdir
from os.path import isfile, isdir, join
import yaml

class ChainSelect(Select):
    def __init__(self, chain):
        self.chain = chain

    def accept_chain(self, chain):
        if chain.get_id() == self.chain:
            return 1
        else:
            return 0


def remove_hetatm(indir, outdir):
	""" Remove heteroatoms from PDB file """
	
	infiles = listdir(indir)

	for file in infiles:
		f1 = join(indir, file)
		f2 = join(outdir, file)
		with open(f1, 'r') as infile:
			with open(f2, 'w') as outfile:
				for line in infile:
					if not line.startswith('HETATM'):
						outfile.write(line)


def remove_hoh(indir, outdir):
	""" Remove water molecules from PDB file """
	
	infiles = listdir(indir)

	for file in infiles:
		f1 = join(indir, file)
		f2 = join(outdir, file)
		with open(f1, 'r') as infile:
			with open(f2, 'w') as outfile:
				for line in infile:
					if not line[17:20] == 'HOH':
						outfile.write(line)


def split_chains(indir, outdir):
	""" Split PDB file into separate PDB files, each containing one chain of the PDB structure """
	
	infiles = listdir(indir)
	pdb_ids = [name.split('.')[0] for name in infiles]
	
	for i in range(len(infiles)):
		print(infiles[i])
		# Get structure from PDB file
		p = PDBParser(QUIET=1)
		structure = p.get_structure(pdb_ids[i], join(indir, infiles[i]))
		chains = structure.get_chains()
		
		io_w_no_h = PDBIO()
		io_w_no_h.set_structure(structure)
		
		# Split into chains and save each chain to a new file
		for chain in chains:
			# Output file
			outfile = join(outdir, ''.join([pdb_ids[i], '_', chain.id, '.pdb']))
			io_w_no_h.save(outfile, ChainSelect(chain.id))

def main():
	config = yaml.safe_load(open("../config.yml"))
	
	pdbdir = config['path']['protein']
	hetatmdir = config['path']['hetatm']
	chaindir = config['path']['chain']
	hohdir = config['path']['hoh']
	
	if not isdir(pdbdir):
		print('ERROR: directory with PDB files does not exist, check path\n', pdbdir)
		exit(-1)
	if not isdir(hetatmdir):
		print('Directory does not exist:', hetatmdir, '\n Creating directory')
		mkdir(hetatmdir)
	if not isdir(hohdir):
		print('Directory does not exist:', hohdir, '\n Creating directory')
		mkdir(hohdir)
	if not isdir(chaindir):
		print('Directory does not exist:', chaindir, '\n Creating directory')
		mkdir(chaindir)
	
	remove_hetatm(pdbdir, hetatmdir)
	remove_hoh(hetatmdir, hohdir)
	split_chains(hohdir, chaindir)

if __name__ == '__main__':
	main()
