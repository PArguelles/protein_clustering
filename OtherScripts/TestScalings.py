import numpy as np
from sklearn import preprocessing

def getStatistics(data):
    stats = []
    stats.append(np.mean(data))
    stats.append(np.std(data))
    stats.append(np.var(data))
    return stats

def dataScaler(data):
    X_train = np.array(data)
    X_scaled = preprocessing.scale(X_train)
    return X_scaled

def minMaxScaler(data):
    min_max_scaler = preprocessing.MinMaxScaler()
    X_train_minmax = min_max_scaler.fit_transform(data)
    return X_train_minmax

def minMax(data):
    maxv = np.amax(data)
    minv = np.amin(data)

    print(data)
    print(getStatistics(data))
    data = ((data - minv)/(maxv - minv))
    print(data)
    print(getStatistics(data))

data = np.random.uniform(0,16,(4,4))
minMax(data)