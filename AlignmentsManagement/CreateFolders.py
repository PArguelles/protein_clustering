
import os

def createFoldersByStructures():

    path = 'C:/ShareSSD/scop/alignments_new/sample_b.3/'
    structures = 'C:/ShareSSD/scop/samples/sample_structures_b.3'

    with open(structures, 'r') as fp:
        line = fp.readline()
        while line:
            line = str(line).strip()
            if not os.path.exists(path+str(line)):
                os.makedirs((path+str(line)))
            line = fp.readline()

createFoldersByStructures()