import KMedoids as kmedoids


import Clustering as cl
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop
import numpy as np

from sklearn.cluster import AgglomerativeClustering

# load protein data before loop
path_to_results = '/home/pedro/Desktop/scop/clustering_results/'
measure1 = 'rmsd'

sample = 'a.1.'
sample_for_domains ='a.1'
X = rs.loadMatrixFromFile(sample, measure1)


mean = 1.79197547637771
std_dev = 0.669382812243833

#X = (X - (mean/std_dev))
X = mf.minMaxScale(X)
X = mf.calculateDistances(X)

domains = rs.loadDomainListFromFile(sample_for_domains)

# read existing labels
n_labels = scop.getUniqueClassifications(sample_for_domains)
ground_truth = scop.getDomainLabels(domains)

ground_truth = map(int, ground_truth)
ground_truth = list(map(int, ground_truth))

X = np.asmatrix(X)

medoids, clusters = kmedoids.kMedoids(X, n_labels, 100)

print('clustering result:')
for label in clusters:
    for point_idx in clusters[label]:
        print('label {0}, {1}:　{2}'.format(label, ground_truth[point_idx], X[point_idx]))

#cl.clusterEvaluationNoLabels(X, clusters)

index_list = []
new_dict = {}

for label in clusters:
        for point_idx in clusters[label]:
                new_dict[point_idx] = label

sorted_keys = sorted(new_dict.keys())

ordered_labels = []
for key in sorted_keys:
        ordered_labels.append(new_dict[key])

print(new_dict)
print(ordered_labels)

evaluation = cl.clusterEvaluation(X, ordered_labels, ground_truth)
print(evaluation)
