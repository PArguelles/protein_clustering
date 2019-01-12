
import os

#remove duplicate atoms and all non CA atoms
def processPDBFiles():

    path = '/home/pedro/Desktop/scop/structures/'
    path2 = '/home/pedro/Desktop/scop/structures_new/'

    counter = 0

    for filename in os.listdir(path):
        print(counter)
        with open(path+filename, 'r') as fp:
            with open(path2+filename, 'w') as fp2:
                line = fp.readline()
                while line:
                    if 'ATOM' in line:
                        parsed = str(line).strip().split()
                        if 'CA' == parsed[2]:
                            fp2.write(line)
                        previous_pos = current_pos
                    else:
                        fp2.write(line)
                    line = fp.readline()
            counter += 1

processPDBFiles()