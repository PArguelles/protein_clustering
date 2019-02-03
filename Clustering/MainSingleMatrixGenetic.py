


import Clustering as cl
import GeneticAlgorithm as ga
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop

from sklearn.cluster import AgglomerativeClustering

# load protein data before loop
path_to_results = 'C:/ShareSSD/scop/clustering_results/'
measure1 = 'gdt_2'
measure2 = 'gdt_2'
measure3 = 'gdt_2'
sample = 'a.1.'
sample_for_domains ='a.1'

matrix1 = rs.loadMatrixFromFile(sample, measure1)
matrix2 = rs.loadMatrixFromFile(sample, measure2)
matrix3 = rs.loadMatrixFromFile(sample, measure3)

matrix1 = mf.minMaxScale(matrix1)
matrix2 = mf.minMaxScale(matrix2)
matrix3 = mf.minMaxScale(matrix3)

#experimentar divisoes com medias e desvio padrao

#matrix1 = mf.calculateDistances(matrix1)
#matrix2 = mf.calculateDistances(matrix2)
#matrix3 = mf.calculateDistances(matrix3)

domains = rs.loadDomainListFromFile(sample_for_domains)

# read existing labels
n_labels = scop.getUniqueClassifications(sample_for_domains)
ground_truth = scop.getDomainLabels(domains)

# genetic algorithm parameters
POPULATION_SIZE = 50
MUTATION_CHANCE = 20
MAX_GENERATIONS = 10

# each pair from fittest and random produces 10 children
N_CHILDREN = 10
N_FITTEST = 5
N_RANDOM = 5
POPULATION_SIZE = ((N_FITTEST+N_RANDOM) / 2) * N_CHILDREN

# sets of random weights for each similarity measure
population = ga.generatePopulation(POPULATION_SIZE)

# track best individual convergence
MAX_CONVERGENCE = 3
convergence_counter = 0
best_fitness = 0
best_individual = []

# cached results
cache = {}

with open(path_to_results+'hierarchical_'+measure1+'_'+measure2, 'w') as nf:

    generation = 0
    while generation < MAX_GENERATIONS or convergence_counter < MAX_CONVERGENCE:
        
        for individual in population:
            
            # avoid repetition
            if tuple(individual) not in cache.keys():

                w1 = individual[0]
                w2 = individual[1]
                w3 = individual[2]

                # can set seq_id weight to 100 here
                #w1, w2, w3 = 1, 1, 1
                
                X = mf.calculateCorrelationMatrix(matrix1, matrix2, matrix3, w1, w2, w3)

                agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=n_labels, linkage='complete').fit(X)
                labels = agglomerative.labels_
                metrics = cl.clusterEvaluation(X, labels, ground_truth)

                nf.write('# Cluster evaluation: \n')
                nf.write('Individual: '+'-'.join(str(individual)))
                nf.write('Homogeneity: %0.3f \n' % metrics[0])
                nf.write('Completeness: %0.3f \n' % metrics[1])
                nf.write('V-measure: %0.3f \n' % metrics[2])
                nf.write('Adjusted Rand Index: %0.3f \n' % metrics[3])
                nf.write('Adjusted Mutual Information: %0.3f \n' % metrics[4])
                nf.write('Calinksi-Harabaz: %0.3f \n' % metrics[5])
                nf.write('Silhouette coefficient: %0.3f \n' % metrics[6])

            # recompute weights with genetic algorithm
            # calculate population fitness
            population_sorted = ga.calculatePopulationFitness(population, labels, ground_truth)

            #get the fittest individual
            current_best = population_sorted[0][0]
            current_best_fitness = population_sorted[0][1]
            
            # get parents for next generation
            breeders = ga.selectFromPopulation(population_sorted, N_FITTEST, N_RANDOM)    

            # create next generation
            next_population = ga.createChildren(breeders, N_CHILDREN)

            # mutate individuals
            population = ga.mutatePopulation(next_population, MUTATION_CHANCE)

            current_best_individual, current_max_fitness = ga.getFittestIndividual(population, labels, ground_truth)
            print(generation)
            print(str(current_best_individual)+' '+str(current_max_fitness)+'\n')
            print('---------------------------')

            # save results in order to save computation time
            # rever
            for ind, fit in population_sorted:
                cache[tuple(ind)] = fit

            # track convergence
            if current_best_fitness > best_fitness:
                best_fitness = current_best_fitness
                best_individual = current_best_individual

            if current_best_individual == current_best:
                convergence_counter += 1
            else:
                convergence_counter = 0

            generation += 1

        print('Finished')






