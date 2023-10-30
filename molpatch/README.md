### MolPatch set up 

It is important to follow these instructions step by step. First set up an environment and all the dependencies:

1. conda create -n mp 
2. conda activate molpatch 
3. conda install dssp -c salilab
4. conda install -c conda-forge biopython
5. conda install scipy
6. conda install networkx
7. conda install -c anaconda pyqt
8. pip install vtk
9. pip install mayavi
10. conda install pandas
11. conda install numpy
12. conda install -c anaconda contextlib2
13. pip install matplotlib
14. pip install PyYAML
15. conda install -c bioconda msms
16. conda install -c conda-forge xvfbwrapper
17. conda install -c conda-forge pyvirtualdisplay

Before running

1. conda activate mp
2. module load 2022
3. module load 2022 Xvfb/21.1.3-GCCcore-11.3.0

One should preprocess the PDB file first, to remove water molecules and split the PDB chains

Python3 preprocess.py

Run MolPatch calculations

Python3 calculate.py
