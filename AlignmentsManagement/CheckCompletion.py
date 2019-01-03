
import os

path_to_alignments = 'C:/ShareSSD/scop2/independent_alignments/'
path_to_redo = 'C:/ShareSSD/scop2/incomplete_structure_alignments'

with open(path_to_redo, 'w') as fp:
    for folder in os.listdir(path_to_alignments):
        path = path_to_alignments+folder+'/'
        _, _, files = next(os.walk(path))
        file_count = len(files)
        if file_count != 4880:
            print(folder)
            fp.write(folder+'\n')