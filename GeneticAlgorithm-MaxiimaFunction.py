# Author:   Al Timofeyev
# Date:     2/7/2019
# Desc:     Use a Genetic Algorithm to solve Project 2.
#           I am solving part 2: Maximize the function
#           f(x,y)=sin(π∗10∗x+10/(1+y^2)) + ln(x^2+y^2)

import random
from operator import add
import math
import matplotlib.pyplot as plt

def randomPoint(min, max):
    num = random.random()*max+1
    if num < min:
        num += min
    elif num > max:
        num = max
    return num

def individual(xMin, xMax, yMin, yMax):
    return [randomPoint(xMin, xMax), randomPoint(yMin, yMax)]

def population(popSize, xMin, xMax, yMin, yMax):
    return [individual(xMin, xMax, yMin, yMax)
            for x in range(popSize)]

def fitness(indi):
    """
    Determines the fitness of an individual.
    
    indi:   The individual contains the x and y variables.
    """
    x = indi[0]
    y = indi[1]
    fit = math.sin(math.pi*10*x+(10/(1+y**2)) + math.log(x**2 + y**2))
    return fit

def grade(pop):
    """
    Determines the average fitness for the whole population.
    
    pop:   The population.
    """
    summed = 0
    for i in range(len(pop)):
        summed += fitness(pop[i])
    
    return summed / (len(pop) * 1.0)

def evolve(pop, xMin, xMax, yMin, yMax, retain=0.2, select=0.05, mutate=0.01):
    """
    Evolves the population to the next generation.

    pop:                Population.
    xMin/Max, yMin/Max: The max/min of the x and y points.
    retain:             Retain 20% of old population.
    select:             Randomly select 5% of the remaining old population and
                        add to retained population to promote genetic diversity.
    mutate:             Mutate 1% of retained population.
    """
    # Grade the population and store tuples of individuals and their fitnesses.
    # Then sort the graded population based on fitness, higher fitness at the
    # front, and only save the sorted individuals, exclude thier fitnesses.
    graded = [(fitness(x), x) for x in pop]
    graded = [x[1] for x in sorted(graded, reverse = True)]
    retain_length = int(len(graded)*retain)
    parents = graded[:2]                    # Only two parents with best fitness.
    retained = graded[2:retain_length+2]    # Retain 20%, except for parents.

    # Randomly add other individuals to promot genetic diversity.
    for indi in graded[retain_length+2:]:
        if select > random.random():
            retained.append(indi)

    # Randomly Mutate retained individuals.
    # Based on mutation rate.
    for indi in retained:
        if mutate > random.random():
            positionToMutate = random.randint(0, len(indi)-1)
            # if mutate X
            if positionToMutate == 0:
                indi[positionToMutate] = randomPoint(xMin, xMax)
            # else mutate Y
            else:
                indi[positionToMutate] = randomPoint(yMin, yMax)

    # Crossover parents to create new children
    # Randomly select children from retained and crossover with
    # one of the parents.
    parentsLength = len(parents)
    retainedLength = len(retained)
    # Basically the length of the remaining population that needs to
    # be made to complete the new population.
    desiredLength = len(pop) - parentsLength - retainedLength
    children = []
    
    while len(children) < desiredLength:
        randRetained = retained[random.randint(0, retainedLength-1)]
        randParent = random.randint(0, parentsLength-1)
        parent = parents[randParent]
        half = int(len(randRetained)/2)
        if randParent == 0:
            child = randRetained[:half] + parent[half:]
        else:
            child = parent[:half] + randRetained[half:]
        children.append(child)

    parents.extend(retained)
    parents.extend(children)
    return parents





#*************************************************************************
#*************************** MAIN CODE SECTION ***************************
#*************************************************************************
# ****** NOTE: So far, population sizes and fitness counter (while loop
# ******        limits) that worked.
# ******        popSize:          1000, 1000, 1500, 2000
# ******        while loop limit: 20,   50,   30,   2
# Setup variables.
generation = 0
genFitness = 0
bestX = 0
bestY = 0
bestFitness = 0    # Only the best (highest) fitness is stored here.
fitnessCounter = 0 # Keeps track of how many times best fitness occurs.
popSize = 1500
xMin = 3
xMax = 10
yMin = 4
yMax = 8

# Initialize population.
pop = population(popSize, xMin, xMax, yMin, yMax)

# Grade generation 0 (get avg fitness).
genFitness = grade(pop)
bestFitness = genFitness

# Keep a fitness history!
fitnessHistory = [genFitness]

# While best fitness hasn't been changed in 20 generations.
while fitnessCounter < 30:
    # Update generation and evolve the population
    generation += 1
    pop = evolve(pop, xMin, xMax, yMin, yMax)

    # Grade the generation.
    genFitness = grade(pop)

    # If the new fitness is better than the old one, update the
    # best fitness and reset the fitness counter.
    if genFitness > bestFitness:
        bestFitness = genFitness
        fitnessCounter = 0
    # Else if the same best fitness was found, increment fitness counter.
    elif genFitness == bestFitness:
        fitnessCounter += 1

    # Add the current generations avg fitness to fitness history.
    fitnessHistory.append(genFitness)

# Get the best X and Y of the population.
bestX = pop[0][0]
bestY = pop[0][1]
print("\n****************************************")
print("***** GENERATIONS:     ", generation)
print("***** Population Size: ", popSize)
print("****************************************\n")
print("Best X and Y: ", bestX, " ", bestY)
print("Best fitness: ", fitnessHistory[len(fitnessHistory)-1])
print("\n\n")

# Plot the fitness History
plt.plot(fitnessHistory)
plt.ylabel('Fitness History')
plt.xlabel('Generations')
plt.show()


      
# Print out the fitness history.
#for datum in fitnessHistory:
#    print(datum, "\n")
    
    



#*************************************************************************
# ************************ TESTING BELOW (IGNORE) ************************
#*************************************************************************

#print("\n*****\n*****Populations:")
#for x in range(len(pop)):
#    print(pop[x])
#print("\nGrade Avg Fitness of Population:\n", grade(pop))

#print("\n*****\n*****Population Individuals and their Fitness:")
# Stored as a list of touples of fitness and individual.
#graded = [(fitness(x), x) for x in pop]
#for x in range(len(graded)):
#    print(graded[x][0], "\t", graded[x][1])

#print("\n*****\n*****Population Sorted Based on Fitness:")
# Sorts the population based on fitness and then stores
# the individuals into graded2. Lowest fitness infividuals
# are stored first and highest fitness stored last.
#*************************************************
# Modified to reverse list to choose best fitness (highest fit)!!!!
#graded2 = [x[1] for x in sorted(graded, reverse = True)]
#for x in range(len(graded2)):
#    print(graded2[x])

#print("\n\n ******* Graded 3 ********")
#graded3 = [x for x in sorted(graded)]
#for x in range(len(graded3)):
#    print(graded3[x][0], "\t", graded3[x][1])

#print("\n\n ******* Graded 4 ********")
#graded4 = [x for x in sorted(pop)]
#for x in range(len(graded4)):
#    print(graded4[x])

#print("\n\n\n")

#parents = graded2[:2]
#print("\nParents:\n", parents)

#retain = 0.2
#retain_length = int(len(graded2)*retain)

#print("\nRetain Length:\n", retain_length)

#retain = graded2[2:retain_length+2]
#print("\nRetained Original:\n", retain)

# Randomly add other individuals to promot genetic diversity.
#random_select = 0.05
#for indi in graded2[retain_length+2:]:
#    if random_select > random.random():
#        retain.append(indi)

#print("\nRetained New:\n", retain)

# Mutate retained individuals.
#mutate = 0.01
#for indi in retain:
#    if mutate > random.random():
#        print("\nMUTATING**********\n")
#        positionToMutate = random.randint(0, len(indi)-1)
#        # if mutate X
#        if positionToMutate == 0:
#            indi[positionToMutate] = randomPoint(3, 10)
#        # else mutate Y
#        else:
#            indi[positionToMutate] = randomPoint(4, 8)

#print("\nRetained Mutated:\n", retain)


#crossover parents to create new children
#parentsLength = len(parents)
#retainedLength = len(retain)
#desiredLength = len(pop) - parentsLength - retainedLength
#children = []
#while len(children) < desiredLength:
#    randRetained = retain[random.randint(0, retainedLength-1)]
#    randParent = random.randint(0, parentsLength-1)
#    parent = parents[randParent]
#    half = int(len(randRetained)/2)
#    if randParent == 0:
#        child = randRetained[:half] + parent[half:]
#    else:
#        child = parent[:half] + randRetained[half:]
#    children.append(child)

#parents.extend(retain)
#parents.extend(children)
#print("\n\nNew Population:\n")
#for x in range(len(parents)):
#    print(parents[x])

#print("\nGrade Avg Fitness of Population:\n", grade(parents))

#print("\n*****\n*****Population Individuals and their Fitness:")
# Stored as a list of touples of fitness and individual.
#graded = [(fitness(x), x) for x in parents]
#for x in range(len(graded)):
#    print(graded[x][0], "\t", graded[x][1])
