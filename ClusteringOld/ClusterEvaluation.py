from sklearn import metrics

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