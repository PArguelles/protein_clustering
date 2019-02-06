
import operator
import random 
from sklearn import metrics

import Clustering as cl
import GeneticAlgorithm as ga
import KMedoids as km
import MatrixFunctions as mf
import ReadSimilarities as rs
import UtilitiesSCOP as scop

from sklearn.cluster import AgglomerativeClustering

def generateIndividual():
    p1 = generateRandomInt()
    p2 = generateRandomInt()
    p3 = generateRandomInt()
    weights = [p1,p2,p3]
    #weights = [x / 100 for x in weights]
    return weights

def generateRandomInt():
    num = random.randint(0,100)
    num /= 100
    return num

def generatePopulation(population_size):
    population = []
    i = 0
    while i < population_size:
        population.append(generateIndividual())
        i += 1
    return population

def fitnessFunction(individual, algorithm, n_labels, ground_truth, m1, m2, m3):
    # maximize with respect to ARI
    w1 = individual[0]
    w2 = individual[1]
    w3 = individual[2]
    corr = mf.calculateCorrelationMatrix(m1, m2, m3, w1, w2, w3)

    if algorithm == 'complete':
        agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=n_labels, linkage='complete').fit(corr)
        labels = agglomerative.labels_
    elif algorithm == 'average':
        agglomerative = AgglomerativeClustering(affinity='precomputed', n_clusters=n_labels, linkage='average').fit(corr)
        labels = agglomerative.labels_
    elif algorithm == 'kmedoids':
        _, clusters = km.kMedoids(corr, n_labels, 100)
        labels = km.sortLabels(clusters)
    
    fitness = metrics.adjusted_rand_score(labels, ground_truth)

    return fitness
    
def calculatePopulationFitness(population, algorithm, n_labels, ground_truth, m1, m2, m3):
    population_fitness = []
    for i in range(len(population)):
        fitness = fitnessFunction(population[i], algorithm, n_labels, ground_truth, m1, m2, m3)
        population_fitness.append(fitness)

    to_sort = list(zip(population, population_fitness))
    sorted_by_fitness = sorted(to_sort, key=lambda x: x[1], reverse=True)
    return sorted_by_fitness

def selectFromPopulation(population, n_fittest, n_random):
    next_generation = []
    for i in range(n_fittest):
        next_generation.append(population[i][0])

    for i in range(n_random):
	    next_generation.append(random.choice(population)[0])

    random.shuffle(next_generation)
    return next_generation

def createChild(individual1, individual2):
    # create child with weights chosen randomly from parents
    child = []
    for i in range(len(individual1)):
        choice = random.randint(1,2)
        if choice == 1:
            child.append(individual1[i])
        elif choice == 2:
            child.append(individual2[i])
    return child

def createChildren(breeders, number_of_children):
	next_population = []
	for i in range(int(len(breeders)/2)):
		for j in range(number_of_children):
			next_population.append(createChild(breeders[i], breeders[len(breeders) -1 -i]))
	return next_population

def mutateIndividual(individual):
    #choose mutation
    rand = random.randint(0,1)
    if rand == 0:
        return swapWeightsMutation(individual)
    else:
        return generateNewWeightsMutation(individual)

def generateNewWeightsMutation(individual):
    position = random.randint(0,2)
    new_weight = generateRandomInt()
    individual[position] = new_weight
    return individual

def swapWeightsMutation(individual):
    #swap weight positions
    position1 = random.randint(0,2)
    position2 = random.randint(0,2)
    while position1 == position2:
        position2 = random.randint(0,2)
    tmp = individual[position1]
    individual[position1] = position2
    individual[position2] = tmp
    return individual

def mutatePopulation(population, mutation_chance):
    for i in range(len(population)):
        chance = generateRandomInt()
        if chance >= mutation_chance:
            population[i] = mutateIndividual(population[i])
    return population

# def getFittestIndividual(population, labels, ground_truth):

#     max_fitness = 0
#     best_individual = []

#     for individual in population:
#         if fitnessFunction(individual, labels, ground_truth) > max_fitness:
#             best_individual = individual
#             max_fitness = fitnessFunction(individual, labels, ground_truth)

#     return best_individual, max_fitness    
