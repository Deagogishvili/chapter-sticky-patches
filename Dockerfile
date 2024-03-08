# Use an official Anaconda runtime as a parent image
FROM continuumio/anaconda3:latest

# Set environment variables
ENV PATH /opt/conda/envs/molpatch/bin:$PATH

# Create and activate conda environment
RUN conda create -y -n molpatch python=3.8 && \
    echo "conda activate molpatch" >> ~/.bashrc

# Activate the conda environment
SHELL ["/bin/bash", "-c"]
RUN echo "conda activate molpatch" >> ~/.bashrc
SHELL ["/bin/bash", "-ic"]

# Install packages in conda environment
RUN conda install -y -n molpatch -c salilab dssp
RUN conda install -y -n molpatch -c conda-forge biopython
RUN conda install -y -n molpatch scipy
RUN conda install -y -n molpatch networkx
RUN conda install -y -n molpatch -c anaconda pyqt
RUN pip install vtk
RUN pip install mayavi
RUN conda install -y -n molpatch pandas
RUN conda install -y -n molpatch numpy
RUN conda install -y -n molpatch -c anaconda contextlib2
RUN pip install matplotlib
RUN pip install PyYAML
RUN conda install -y -n molpatch -c bioconda msms
RUN conda install -y -n molpatch -c conda-forge xvfbwrapper
RUN conda install -y -n molpatch -c conda-forge pyvirtualdisplay
RUN conda install -y -n molpatch libboost=1.73.0

# Activate molpatch environment before running
RUN echo "source activate molpatch" > ~/.bashrc

# Copy files and directories from the host into the image
COPY /molpatch .

# Load modules
RUN echo "module load 2022" >> ~/.bashrc
RUN echo "module load 2022 Xvfb/21.1.3-GCCcore-11.3.0" >> ~/.bashrc

CMD python /ResidueBased/preprocessing.py && python /ResidueBased/calculate.py