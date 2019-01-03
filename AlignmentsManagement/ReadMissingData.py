
import os
import re
import pickle

path_to_redo = 'C:/ShareSSD/scop2/delete/'
path_to_sum = 'C:/ShareSSD/scop2/sum2'

todo = set()
structures = set()

for filename in os.listdir(path_to_redo):
    parsed = str(filename).split('-')
    structure1 = parsed[0]
    structure2 = parsed[1]
    todo.add(structure1+' '+structure2)
    structures.add(structure1)
    structures.add(structure2)

path_to_data = 'C:/ShareSSD/scop/data/'
id_map = {}

s1 = []
s2 = []
gdts_2 = []
gdts_4 = []
maxsubs1 = []
maxsubs2 = []
pairs = []
rmsds = []
seq_ids = []
tmscores1 = []
tmscores2 = []

with open(path_to_sum,'w') as nf:

    #READ GDT2
    with open(path_to_data+'sim_gdt2','r') as fp:
        line = fp.readline()
        while line:
            if 'PDB  :' in line and any(structure in line for structure in structures):
                print(str(line).split())
                domain = str(line).strip().split()[-1].split('/')[-1]
                key = str(line).strip().split()[2]
                id_map[key] = domain
            if 'Distance records' in str(line):
                    break
            line = fp.readline()

        line = fp.readline()
        while line:
            if '#' not in str(line) and 'DIST :' in str(line): 
                parsed = str(line).strip().split()
                if parsed[2] in id_map.keys() and parsed[3] in id_map.keys():
                    if str(id_map[parsed[2]]+' '+id_map[parsed[3]]) in todo or str(id_map[parsed[3]]+' '+id_map[parsed[2]]) in todo:
                        s1.append(id_map[parsed[2]])
                        s2.append(id_map[parsed[3]])
                        gdts_2.append(parsed[4])
            line = fp.readline()

    #READ GDT4
    with open(path_to_data+'sim_gdt4','r') as fp2: 
        line = fp2.readline()
        while line:
            if '#' not in str(line) and 'DIST :' in str(line): 
                parsed = str(line).strip().split()
                if parsed[2] in id_map.keys() and parsed[3] in id_map.keys():
                    if str(id_map[parsed[2]]+' '+id_map[parsed[3]]) in todo or str(id_map[parsed[3]]+' '+id_map[parsed[2]]) in todo:
                        gdts_4.append(parsed[4])
            line = fp2.readline()

    #READ RMSD
    with open(path_to_data+'sim_rmsd','r') as fp3: 
        line = fp3.readline()
        while line:
            if '#' not in str(line) and 'DIST :' in str(line): 
                parsed = str(line).strip().split()
                if parsed[2] in id_map.keys() and parsed[3] in id_map.keys():
                    if str(id_map[parsed[2]]+' '+id_map[parsed[3]]) in todo or str(id_map[parsed[3]]+' '+id_map[parsed[2]]) in todo:
                        rmsds.append(parsed[4])
            line = fp3.readline()

    #READ MAXSUB
    with open(path_to_data+'sim_maxsub','r') as fp4: 
        line = fp4.readline()
        while line:
            if '#' not in str(line) and 'MS :' in str(line): 
                parsed = str(line).strip().split()
                if parsed[2] in id_map.keys() and parsed[3] in id_map.keys():
                    if str(id_map[parsed[2]]+' '+id_map[parsed[3]]) in todo or str(id_map[parsed[3]]+' '+id_map[parsed[2]]) in todo:
                        maxsubs1.append(str(parsed[4]))
                        maxsubs2.append(str(parsed[5]))
                        pairs.append(str(parsed[6]))
            line = fp4.readline()

    #READ TMSCORES AND SEQ_ID
    for structure1, structure2 in list(zip(s1, s2)):
        with open('C:/ShareSSD/scop2/tmalign/'+structure1+'-'+structure2+'-tm','r') as fp5:
            line = fp5.readline()
            while line:
                if 'Seq_ID=' in line:
                    parsed = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                    seq_ids.append(parsed[2])
                if 'TM-score=' in line and '(if normalized by length of Chain_1)' in line:
                    parsed = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                    tmscores1.append(parsed[0])
                if 'TM-score=' in line and '(if normalized by length of Chain_2)' in line:
                    parsed = re.findall(r"[-+]?\d*\.\d+|\d+", line)
                    tmscores2.append(parsed[0])
                    break
                line = fp5.readline()

    to_write = list(zip(s1,s2,rmsds,maxsubs1,maxsubs2,tmscores1,tmscores2,gdts_2,gdts_4,seq_ids))

    with open('C:/ShareSSD/scop2/missing', 'w') as fp6:
        fp6.write('\n'.join('%s %s %s %s %s %s %s %s %s %s' % x for x in to_write))