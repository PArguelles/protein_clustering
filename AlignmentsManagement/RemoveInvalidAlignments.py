import os
import shutil
import re

#extracts files that do not have valid alignment information
def removeInvalidFiles():

    path = 'C:/ShareSSD/scop2/independent_alignments/'
    path_to_filtered = 'C:/ShareSSD/scop2/delete/'

    remove = False

    count = 0

    #iterate folders
    for folder in os.listdir(path):

        #iterate files in folder
        for filename in os.listdir(path+folder+'/'):
            
            count += 1
            print(str(count)+' '+filename)
                
            #open file and read data
            with open(path+folder+'/'+filename) as nf:
                line = nf.readline()
                if 'RMSD' not in line:
                    remove = True
                
            if remove:
                #shutil.copy2(path+folder+'/'+filename, path_to_filtered+filename)
                shutil.move(path+folder+'/'+filename, path_to_filtered+filename)

            remove = False

removeInvalidFiles()