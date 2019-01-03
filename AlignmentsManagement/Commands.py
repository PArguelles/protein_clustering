import os
import shutil
import re

def listProcessingSCOP():
    path_to_file = 'C:/ShareSSD/list_sample_maxcluster'
    path_to_results = 'C:/ShareSSD/listProcessing/'

    domains = []

    with open(path_to_file, 'r') as fp:
        line = fp.readline()
        while line:
            domains.append(str(line).strip().split('/')[-1])
            line = fp.readline()

    
        for dom in domains:
            with open(path_to_results, 'w') as nf:
                cmd = './maxcluster64bit -e '+dom+' -l '+path_to_file+' -in -Rl C:/ShareSSD/listProcessing/'+dom+' -tm'
                nf.write(cmd+'\n')

def getValidDomains():
    path_to_matrix = 'C:/ShareSSD/tests/rmsdfile'

    with open(path_to_matrix, 'r') as fp:

        size = 0
        domains = []

        #get number of structures
        line = fp.readline()
        while line:
            if 'PDB  :' in str(line): 
                if '#' not in str(line):
                    size += 1
                    domain = str(line).strip().split()[-1].split('/')[-1]
                    domains.append(str(domain))
            if 'Distance records' in str(line):
                break
            line = fp.readline()

    with open('C:/ShareSSD/tests/valid_structures', 'w') as nf:
        for dom in domains:
            nf.write('/home/pedro/ShareSSD/scop/structures/'+dom+'\n')

def filterMaxclusterResults():

    path_to_alignments = 'C:/ShareSSD/scop/test/aaa/'
    path_to_filtered = 'C:/ShareSSD/scop/maxcluster_to_delete/'

    for filename in os.listdir(path_to_alignments):

        with open(path_to_alignments+filename,'r') as fp:

            line = fp.readline()

            if 'RMSD' not in line:
                shutil.copy2(path_to_alignments+filename,path_to_filtered+filename)
                #os.rename(path_to_alignments+filename,path_to_filtered+filename)

def generateWinCommands():
    path_to_data = 'C:/ShareSSD/scop/structure_list'
    path_to_commands = 'C:/ShareSSD/scop/win_commands'

    structures = []

    with open(path_to_data, 'r') as fp:

        line = fp.readline()
        while line:
            parsed = str(line).strip()
            structures.append(parsed)
            line = fp.readline()

    structures_copy = structures.copy()

    part = 1
    count = 0

    with open(path_to_commands, 'w') as fp2:
        for structure1 in structures:
            for structure2 in structures_copy:
                count += 1
                cmd = 'C:/ShareSSD/scop/maxcluster.exe -e C:/ShareSSD/scop/structures/'+str(structure1)+' -p C:/ShareSSD/scop/structures/'+str(structure2)+' -in -noalign -gdt 2 > C:/ShareSSD/tests/gdt_2_part_'+str(part)+'/'+str(structure1)+'-'+str(structure2)+'-gdt-2 2>&1'
                fp2.write(str(cmd).strip()+'\n')
                if count % 500000 == 0:
                    part += 1
            break

def redoCommands():

    path_to_redo = 'C:/ShareSSD/scop2/delete/'
    path_to_commands = 'C:/ShareSSD/scop2/redo_commands'

    with open(path_to_commands, 'w') as fp:
        for filename in os.listdir(path_to_redo):

            parsed = str(filename).split('-')
            structure1 = parsed[0]
            structure2 = parsed[1]

            if 'gdt-2' in filename:
                measure = '2'
            else: 
                measure = '4'

            cmd = 'C:/ShareSSD/scop/maxcluster.exe -e C:/ShareSSD/scop/structures/'+str(structure1)+' -p C:/ShareSSD/scop/structures/'+str(structure2)+' -in -noalign -gdt '+measure+' > C:/ShareSSD/scop2/redo/'+str(structure1)+'-'+str(structure2)+'-gdt-'+measure+' 2>&1'
            fp.write(str(cmd).strip()+'\n')

