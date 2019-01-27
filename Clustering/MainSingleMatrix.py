
import Clustering as cl
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop
import numpy as np

from sklearn.cluster import AgglomerativeClustering

# load protein data before loop
path_to_results = 'C:/ShareSSD/scop/clustering_results/'
measure1 = 'rmsd'

sample = 'a.1.'
sample_for_domains = 'a.1'
X = rs.loadMatrixFromFile(sample, measure1)


mean = 1.79197547637771
std_dev = 0.669382812243833

#X = (X - (mean/std_dev))

X = mf.calculateDistances(X)

domains = rs.loadDomainListFromFile(sample)

# read existing labels
n_labels = scop.getUniqueClassifications(sample_for_domains)
ground_truth = scop.getDomainLabels(domains)

ground_truth = map(int, ground_truth)
ground_truth = list(map(int, ground_truth))

X = np.asmatrix(X)

agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=n_labels, linkage='complete').fit(X)
labels = agglomerative.labels_

metrics = cl.clusterEvaluation(X, labels, ground_truth)

print(metrics)
print(len(labels))
print(len(ground_truth))






