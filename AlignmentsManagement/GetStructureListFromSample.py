
import os

def getStructureList(sample):
    path_to_sample = '/home/pedro/Desktop/scop/samples/sample_'+sample
    path_to_structures = '/home/pedro/Desktop/scop/samples/sample_structures_'+sample

    with open(path_to_sample, 'r') as fp:
        with open(path_to_structures, 'w') as fp2:

            line = fp.readline()
            while line:
                print(line)
                fp2.write('/home/pedro/Desktop/scop/structures/'+str(line).strip().split()[0]+'\n')

                line = fp.readline()

getStructureList('a.1')
getStructureList('a.2')
getStructureList('a.3')
getStructureList('b.1')
getStructureList('b.2')
getStructureList('b.3')