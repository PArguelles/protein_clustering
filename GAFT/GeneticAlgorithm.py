

from math import sin, cos

from gaft import GAEngine
from gaft.components import BinaryIndividual
from gaft.components import DecimalIndividual
from gaft.components import Population
from gaft.operators import TournamentSelection
from gaft.operators import RouletteWheelSelection
from gaft.operators import UniformCrossover
from gaft.operators import FlipBitMutation

from gaft.plugin_interfaces.analysis import OnTheFlyAnalysis
from gaft.analysis.fitness_store import FitnessStore

# PROTEIN CLUSTERING
import Clustering as cl
import GeneticAlgorithm as ga
import KMedoids as km
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop

from sklearn import metrics

from sklearn.cluster import AgglomerativeClustering

# WORKING ON THIS
# complete, average or kmedoids
algorithm = 'complete'

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

matrix1 = mf.minMaxScale(matrix1)
matrix2 = mf.minMaxScale(matrix2)
matrix3 = mf.minMaxScale(matrix3)

matrix1 = mf.calculateDistances(matrix1)
matrix2 = mf.calculateDistances(matrix2)
matrix3 = mf.calculateDistances(matrix3)

domains = rs.loadDomainListFromFile(sample_for_domains)

# read existing labels
n_labels = scop.getUniqueClassifications(sample_for_domains)
ground_truth = scop.getDomainLabels(domains)


# Define population.
indv_template = DecimalIndividual(ranges=[(0.1, 0.9),(0.1, 0.9),(0.1, 0.9)], eps=[0.01,0.01,0.01])
population = Population(indv_template=indv_template, size=30).init()

# Create genetic operators.
#selection = TournamentSelection()
selection = RouletteWheelSelection()
crossover = UniformCrossover(pc=0.8, pe=0.5)
mutation = FlipBitMutation(pm=0.6)

# Create genetic algorithm engine.
engine = GAEngine(population=population, selection=selection,
                  crossover=crossover, mutation=mutation,
                  analysis=[FitnessStore])

# Define fitness function.
@engine.fitness_register
def fitness(indv):
    w1, w2, w3 = indv.solution
    #return x + 10*sin(5*x) + 7*cos(4*x)
    corr = mf.calculateCorrelationMatrix(matrix1, matrix2, matrix3, w1, w2, w3)
    agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=n_labels, linkage='complete').fit(corr)
    labels = agglomerative.labels_

    metrics = cl.clusterEvaluation(corr, labels, ground_truth)

    if metrics[0] <= 0:
        return 1

    print(metrics[0] * 100)
    return float(metrics[0]) * 100

# Define on-the-fly analysis.
@engine.analysis_register
class ConsoleOutputAnalysis(OnTheFlyAnalysis):
    interval = 1
    master_only = True

    def register_step(self, g, population, engine):
        best_indv = population.best_indv(engine.fitness)
        msg = 'Generation: {}, best fitness: {:.3f}'.format(g, engine.ori_fmax)
        print(msg)
        #print(str(best_indv[0])+str(best_indv[1])+str(best_indv[2]))
        #self.logger.info(msg)

    # added path
    def finalize(self, population, engine):
        best_indv = population.best_indv(engine.fitness)
        x = best_indv.solution
        y = engine.ori_fmax
        msg = 'Optimal solution: ({}, {})'.format(x, y)
        print(msg)
        print(x)
        #self.logger.info(msg)

if '__main__' == __name__:
    # Run the GA engine.
    engine.run(ng=10)