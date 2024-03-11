FROM janvaneck1994/msms_dssp

RUN apt-get install -y libgl1-mesa-glx libxrender1

RUN pip3 install numpy
RUN pip3 install biopython scipy networkx pandas PyYAML mayavi

COPY ./molpatch /molpatch/

WORKDIR /molpatch/ResidueBased

CMD ["python3", "calculate.py"]