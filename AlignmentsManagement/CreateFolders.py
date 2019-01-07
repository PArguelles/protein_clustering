
import os

def createFoldersByStructures():

    path = '/home/pedro/Desktop/Data/alignments/sample_b.3/'
    structures = '/home/pedro/Desktop/Data/samples/sample_structures_b.3'

    with open(structures, 'r') as fp:
        line = fp.readline()
        while line:
            line = str(line).strip()
            if not os.path.exists(path+str(line)):
                os.makedirs((path+str(line)))
            line = fp.readline()

def getStructureList

createFoldersByStructures()