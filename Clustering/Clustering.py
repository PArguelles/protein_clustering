from sklearn.cluster import AffinityPropagation
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn import metrics

def computeAgglomerative(X, n):
    
    for link in ['complete','average']:
        agglo = AgglomerativeClustering(affinity='precomputed', n_clusters=n, linkage=link).fit(X)
        labels = agglo.labels_

    return labels

def computeDBSCAN(X):
    
    db = DBSCAN(metric='precomputed', eps=10, min_samples=2).fit(X)
    labels = db.labels_

    return labels

def clusterEvaluation(X, labels, labels_true):
    values = []
    values.append(metrics.homogeneity_score(labels_true, labels))
    values.append(metrics.completeness_score(labels_true, labels))
    values.append(metrics.v_measure_score(labels_true, labels))
    values.append(metrics.adjusted_rand_score(labels_true, labels))
    values.append(metrics.adjusted_mutual_info_score(labels_true, labels))
    values.append(metrics.calinski_harabaz_score(X, labels))
    values.append(metrics.silhouette_score(X, labels, metric='precomputed'))
    return values

def clusterEvaluationNoLabels(X, labels):
    values = []
    values.append(metrics.calinski_harabaz_score(X, labels))
    values.append(metrics.silhouette_score(X, labels, metric='precomputed'))
    return values

def saveResults(measure1, measure2, algorithm, sample, metrics):

    path_to_results = 'C:/ShareSSD/scop/clustering_results/'
    
    with open(path_to_results+algorithm+'_'+sample+'_'+measure1+'_'+measure2, 'w') as nf:
        nf.write('# Cluster evaluation: \n')
        #nf.write('Individual: '+'-'.join(str(individual)))
        nf.write('Homogeneity: %0.3f \n' % metrics[0])
        nf.write('Completeness: %0.3f \n' % metrics[1])
        nf.write('V-measure: %0.3f \n' % metrics[2])
        nf.write('Adjusted Rand Index: %0.3f \n' % metrics[3])
        nf.write('Adjusted Mutual Information: %0.3f \n' % metrics[4])
        nf.write('Calinksi-Harabaz: %0.3f \n' % metrics[5])
        nf.write('Silhouette coefficient: %0.3f \n' % metrics[6]) 