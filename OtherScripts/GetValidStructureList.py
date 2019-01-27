

def getValidStructuresFromMaxcluster(sample):

    path_to_sim = 'C:/ShareSSD/scop/data/sim_'+sample+'_rmsd'
    path_to_structures = 'C:/ShareSSD/scop/domains_'+sample

    with open(path_to_sim, 'r') as fp:

        with open(path_to_structures, 'w') as nf:
            line = fp.readline()
            while line:

                if 'PDB' in line and '#' not in line:
                    structure = str(line).strip().split()[3].split('/')[-1]
                    print(structure)
                    nf.write(structure+'\n')
                    
                line = fp.readline()

getValidStructuresFromMaxcluster('a.1.')
getValidStructuresFromMaxcluster('a.2.')
getValidStructuresFromMaxcluster('a.3.')
getValidStructuresFromMaxcluster('b.2.')
getValidStructuresFromMaxcluster('b.3.')