

import Clustering as cl
import GeneticAlgorithm as ga
import KMedoids as km
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop

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

# genetic algorithm parameters
# default 50, 20, 10
POPULATION_SIZE = 50
MUTATION_CHANCE = 40
MAX_GENERATIONS = 10

# each pair from fittest and random produces 10 children
# default values 10, 5, 5
N_CHILDREN = 10
N_FITTEST = 5
N_RANDOM = 5
POPULATION_SIZE = ((N_FITTEST+N_RANDOM) / 2) * N_CHILDREN

# create initial population
population = ga.generatePopulation(POPULATION_SIZE)

# track best individual convergence
MAX_CONVERGENCE = 5
convergence_counter = 0

overall_best_individual = []
overall_best_fitness = 0

# cached results
cache = {}

with open(path_to_results+'hierarchical_'+measure1+'_'+measure2, 'w') as nf:

    generation = 0
    while generation < MAX_GENERATIONS and convergence_counter < MAX_CONVERGENCE:

        # recompute weights with genetic algorithm
        # calculate population fitness
        population_sorted = ga.calculatePopulationFitness(population, algorithm, n_labels, ground_truth, matrix1, matrix2, matrix3)

        population.clear()

        # get the fittest individual
        current_best_individual = population_sorted[0][0]
        current_best_fitness = population_sorted[0][1]

        # calculate metrics for the best individual here

        # get parents for next generation
        breeders = ga.selectFromPopulation(population_sorted, N_FITTEST, N_RANDOM)

        # create next generation
        next_population = ga.createChildren(breeders, N_CHILDREN)

        # mutate individuals
        population = ga.mutatePopulation(next_population, MUTATION_CHANCE)

        # track convergence
        if current_best_individual == overall_best_individual:
            convergence_counter += 1
        else:
            convergence_counter = 0

        # update best individual
        if current_best_fitness > overall_best_fitness:
            overall_best_fitness = current_best_fitness
            overall_best_individual = current_best_individual

        print(current_best_fitness)
        print(current_best_individual)
        print(generation)
        print(convergence_counter)
        print('-------------------------')
        generation += 1

print('Finished')
print(overall_best_fitness)
print(overall_best_individual)
print(generation)
print(convergence_counter)
print('-------------------------')


# K-Medoids
#medoids, clusters = km.kMedoids(corr, n_labels, 100)
#labels = km.sortLabels(clusters)
#metrics = cl.clusterEvaluation(corr, labels, ground_truth)
#cl.saveResults(measure1, measure2, 'kmedoids', sample, metrics)

# nf.write('# Cluster evaluation: \n')
# nf.write('Individual: '+'-'.join(str(individual)))
# nf.write('Homogeneity: %0.3f \n' % metrics[0])
# nf.write('Completeness: %0.3f \n' % metrics[1])
# nf.write('V-measure: %0.3f \n' % metrics[2])
# nf.write('Adjusted Rand Index: %0.3f \n' % metrics[3])
# nf.write('Adjusted Mutual Information: %0.3f \n' % metrics[4])
# nf.write('Calinksi-Harabaz: %0.3f \n' % metrics[5])
# nf.write('Silhouette coefficient: %0.3f \n' % metrics[6])
