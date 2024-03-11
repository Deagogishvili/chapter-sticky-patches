#!/usr/bin/python3

from Bio.PDB import Select, PDBIO
from Bio.PDB.PDBParser import PDBParser
from os import listdir
from os.path import isdir, join
import yaml
import tempfile

class ChainSelect(Select):
    def __init__(self, chain):
        self.chain = chain

    def accept_chain(self, chain):
        if chain.get_id() == self.chain:
            return 1
        else:
            return 0

def remove_hetatm(infile, outfile):
    """ Remove heteroatoms from PDB file """
    with open(infile, 'r') as inf, open(outfile, 'w') as outf:
        for line in inf:
            if not line.startswith('HETATM'):
                outf.write(line)

def remove_hoh(infile, outfile):
    """ Remove water molecules from PDB file """
    with open(infile, 'r') as inf, open(outfile, 'w') as outf:
        for line in inf:
            if not line[17:20] == 'HOH':
                outf.write(line)

def split_chains(infile, outdir, pdb_id):
    """ Split PDB file into separate PDB files, each containing one chain of the PDB structure """
    # Get structure from PDB file
    p = PDBParser(QUIET=1)
    structure = p.get_structure(pdb_id, infile)
    chains = structure.get_chains()

    io_w_no_h = PDBIO()
    io_w_no_h.set_structure(structure)

    # Split into chains and save each chain to a new file
    for chain in chains:
        # Output file
        outfile = join(outdir, ''.join([pdb_id, '_', chain.id, '.pdb']))
        io_w_no_h.save(outfile, ChainSelect(chain.id))

def main():
    config = yaml.safe_load(open("../config.yml"))
    
    pdb_dir = config['path']['input']
    processed_dir = config['path']['processed']
    
    if not isdir(pdb_dir):
        print('ERROR: directory with PDB files does not exist, check path\n', pdb_dir)
        return
    
    if not isdir(processed_dir):
        print('ERROR: directory with for processed PDB files does not exist, check path\n', processed_dir)
        return
    
    for pdb_file in listdir(pdb_dir):
        try:
            pdb_id = pdb_file.split('.')[0]
            infile_path = join(pdb_dir, pdb_file)
            
            # Create temporary directories for intermediate steps
            with tempfile.TemporaryDirectory() as hetatm_dir, tempfile.TemporaryDirectory() as hoh_dir:
                # Process through remove_hetatm
                hetatm_path = join(hetatm_dir, pdb_file)
                remove_hetatm(infile_path, hetatm_path)
                
                # Process through remove_hoh
                hoh_path = join(hoh_dir, pdb_file)
                remove_hoh(hetatm_path, hoh_path)
                
                # Final step: split_chains
                split_chains(hoh_path, processed_dir, pdb_id)
        except:
            print(f"unable to preprocess {pdb_file}")

if __name__ == '__main__':
    main()
