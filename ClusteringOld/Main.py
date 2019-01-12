import MatrixFunctions as mf
import UtilitiesSCOP as scop
import FileFunctions as ff
import ClusterEvaluation as ce
import numpy as np
from sklearn.cluster import AgglomerativeClustering

path_to_results = '/home/pedro/Desktop/scop/clustering_results/'
sample = 'a.1'
sample_for_file_name = 'a.1.'

#read how many unique superfamilies there are in the sample
n = scop.getUniqueClassifications(sample)

measure1 = 'gdt4'
measure2 = 'gdt4'
#measure2 = 'maxsub'

#read matrices
domains, matrix1 = ff.readDistances(measure1)
matrix2 = matrix1
#domains, matrix2 = ff.readDistances(measure2)
#matrix2 = ff.loadMatrixFromFile('a.1.', measure2)

ground_truth = scop.getDomainLabels(domains)

#matrix1 = mf.calculateDistances(matrix1, matrix1)
#matrix2 = mf.calculateDistances(matrix2, matrix2)

multiple_weight = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
single_weight = [1.0]

for w1 in single_weight:

    corr = mf.calculateCorrelation(w1, matrix1, matrix2)

    for link in ['complete','average']:

        with open(path_to_results+sample_for_file_name+'_hiearchical_noeuclidean_'+link+'_'+str(w1)+'_'+measure1+'_'+measure2,'w') as file:

            agglo = AgglomerativeClustering(affinity='precomputed', n_clusters=n, linkage=link).fit(corr)
            labels = agglo.labels_
            metrics = ce.clusterEvaluation(corr, labels, ground_truth)

            print(w1)

            file.write('# Cluster evaluation: \n')
            file.write('Measure1: '+measure1+'\n')
            file.write('Measure2: '+measure2+'\n')
            file.write('W1: %0.3f \n' % w1)
            file.write('Homogeneity: %0.3f \n' % metrics[0])
            file.write('Completeness: %0.3f \n' % metrics[1])
            file.write('V-measure: %0.3f \n' % metrics[2])
            file.write('Adjusted Rand Index: %0.3f \n' % metrics[3])
            file.write('Adjusted Mutual Information: %0.3f \n' % metrics[4])
            file.write('Calinksi-Harabaz: %0.3f \n' % metrics[5])
            file.write('Silhouette coefficient: %0.3f \n' % metrics[6])
            file.write('\n')
