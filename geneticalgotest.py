'''
A genetic algorithm to predict the percentage changes of bitcoin. Only data used is the ticker price. Prices are indexed in exponential frequency, 
with lower timeframes being indexed more frequently than higher ones. Fitness function takes historical data and modifies it to percent changes,
which are then multiplied by genes (array of floats) that are optimized by PyGad. New array is summed and turned into a percent, then accuracy is 
calculated with price 20 seconds in the future and percent accurate is returned by fitness.
'''

import pygad
import cupy as cp
import random
import matplotlib.pyplot as plt
import os

numGenes = 100
timeToPredict = 60
xVals = []
yVals = []
data = cp.loadtxt(r"data\binance_prices.csv", delimiter=",", skiprows=1, usecols=1)

def fitness_function(algoInstance=None, solution=None, popi=None):
    # Parameters for setting up price checks for model
    i = random.randint(numGenes, len(data)-(timeToPredict+1))         # Starting index
    A = 300000          # Max historical price check
    N = numGenes      # Number of points
    k = -cp.log(0.5/A)/(N-1)  # minimum decay rate

    # Generate the sequence of price values from max historical price check -> starting index to be indexed
    sequence = (i - cp.round(A * cp.exp(-k * cp.arange(N))).astype(int))
    currprice = data[i]
    percentchanges = ((data[sequence] - currprice) / currprice)
    #prediction and accurate are multiplied by 100 to try to avoid fp errors (mabye?)
    prediction = cp.sum(percentchanges * cp.array(solution)) * 100
    actual = ((data[i+timeToPredict] - currprice) / currprice) * 100
    #calculate percent accuracy
    accuracy = 100 - abs((((prediction - actual) / actual) * 100))
    xVals.append(popi)
    yVals.append(float(accuracy))
    #print(prediction, actual, accuracy)
    return float(accuracy)

#display generations completed while running GA
def onGen(ga_instance):
    if ga_instance.generations_completed % 1000 == 0:
        print(ga_instance.generations_completed)
    pass


# Define the parameters for the genetic algorithm
ga_instance = pygad.GA(
    num_generations = 5000,
    num_parents_mating=100,
    fitness_func=fitness_function,
    sol_per_pop=500,
    gene_type=float,
    gene_space={'low': -1.0, 'high': 1.0},
    num_genes=numGenes,
    mutation_type="random",
    mutation_num_genes=10,
    on_generation=onGen,
)

# Run the genetic algorithm
ga_instance.run()

# Get the best solution and its fitness value
best_solution = ga_instance.best_solution()
best_layout = best_solution[0]
best_fitness = best_solution[1]

# Print the best layout and its fitness value
print("Best Layout:", best_layout)
print("Fitness Value:", best_fitness)
sol_test = cp.zeros(100)
for i in range(0, len(sol_test)):
    sol_test[i] = fitness_function(solution=best_layout)
print('General preformance: ', sol_test)


plt.scatter(xVals, yVals, label='Data Points')
plt.show()



