

import os
import shutil

#move the alignment file to the corresponding structure folder
def moveAlignmentFiles():

        path_to_source = 'C:/ShareSSD/scop2/tmalignmaxcluster/'
        path_to_destination = 'C:/ShareSSD/scop2/independent_alignments/'

        count = 0

        for filename in os.listdir(path_to_source):        
                count += 1
                structure = str(filename).split('-')[0]
                shutil.move(path_to_source+filename, path_to_destination+structure+'/'+filename)
                print(str(count)+' '+str(path_to_destination)+str(structure)+'/'+str(filename))

moveAlignmentFiles()

