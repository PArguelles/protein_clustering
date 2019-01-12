

def processSCOPSequences():
    path_to_sequences = '/home/pedro/Desktop/scop/scope/astral-scopedom-seqres-gd-all-2.07-stable.fa.txt'
    path_to_files = '/home/pedro/Desktop/scop/sequences/'

    with open(path_to_sequences, 'r') as fp:

        line = fp.readline()
        while line:

            if '>' in line:

                domain_id = str(line).strip().split()[0][1:]
                with open(path_to_files+domain_id+'.ent', 'w') as nf:
                    while line:

                        print(line)
                        line = fp.readline()
                        if '>' in line:
                            break

                        nf.write(str(line))
            else: break


processSCOPSequences()