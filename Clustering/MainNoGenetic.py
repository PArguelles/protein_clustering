
import Clustering as cl
import KMedoids as km
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop
import numpy as np

from sklearn.cluster import AgglomerativeClustering

# load protein data before loop
path_to_results = 'C:/ShareSSD/scop/clustering_results/'
measure1 = 'rmsd'
measure2 = 'gdt_2'
measure3 = 'seq'

sample = 'a.1.'
sample_for_domains = 'a.1'

matrix1 = rs.loadMatrixFromFile(sample, measure1)
matrix2 = rs.loadMatrixFromFile(sample, measure2)
matrix3 = rs.loadMatrixFromFile(sample, measure3)

#matrix3 = 1 - matrix3

domains = rs.loadDomainListFromFile(sample)

# read existing labels
n_labels = scop.getUniqueClassifications(sample_for_domains)

ground_truth = scop.getDomainLabels(domains)
ground_truth = map(int, ground_truth)
ground_truth = list(map(int, ground_truth))

matrix1 = mf.minMaxScale(matrix1)
matrix2 = mf.minMaxScale(matrix2)
matrix3 = mf.minMaxScale(matrix3)

matrix1 = mf.calculateDistances(matrix1)
matrix2 = mf.calculateDistances(matrix2)
matrix3 = mf.calculateDistances(matrix3)

#for w1 in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
w1 = 0.43
w2 = 0.05
w3 = 0

corr = mf.calculateCorrelationMatrix(matrix1, matrix2, matrix3, w1, w2, w3)

agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=n_labels, linkage='complete').fit(corr)
labels = agglomerative.labels_
metrics = cl.clusterEvaluation(corr, labels, ground_truth)
#cl.saveResults(measure1, measure2, 'hierarchical_'+link, sample, metrics)

print(metrics)