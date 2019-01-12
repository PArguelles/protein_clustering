import numpy as np
import sklearn.preprocessing as pp

def symmetrizeMatrix(a):
    a = a + a.T - np.diag(a.diagonal())
    np.savetxt("/home/pedro/Desktop/scop/data_old/matrix4", a,delimiter=' ', newline='\n')
    return a    
   
def calculateCorrelation(w, a, b):
    a = np.asmatrix(a)
    b = np.asmatrix(b)
    w1 = w
    w2 = 1 - w1
    a *= w1
    b *= w2
    
    rows, cols = a.shape

    corr = np.zeros((rows,cols))

    for x in range(0, rows):
        for y in range(0, cols):
            corr[x,y] = a[x,y] + b[x,y]

    return corr

def processGDTMatrix(a):
    a = np.divide(a,100)
    return a

def normalize(a):
    a = pp.normalize(a, norm='l1', axis=1)
    return a

def calculateDistances(a, b):
    from sklearn.metrics.pairwise import euclidean_distances
    corr = euclidean_distances(a, b)
    return corr
