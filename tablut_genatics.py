
import pygad
import numpy
import csv

def play_game(solution,oppunent,indicator):


    #####################################
    if indicator == 0: #white

      white_heuristics = heuristics(0, solution)
      tablut_client(white_heuristics)

      black_heuristics = heuristics(1, oppunent)
      tablut_client(black_heuristics)

    if indicator == 1: #black

      white_heuristics = heuristics(0, oppunent)
      tablut_client(white_heuristics)

      black_heuristics = heuristics(1, solution)
      tablut_client(black_heuristics)
    #####################################

    """
    #play the game
    here it should return:
       1. winner = 0 or 1
       2. Number0fMoves = .....
    """
    output = [winner, Number0fMoves]
    return output


indicator = 0 #decides the player that we want to optimize
oppunent = [0.25,0.25,0.25,0.25] #first since indicator is 0 the oppunent is black

wh_sol = [] #white player list where we save the best solution (weights) for each iterations
bl_sol = [] #black player list where we save the best solution (weights) for each iterations

for step in range(0,10):



    def fitness_func(ga_instance, solution, solution_idx):
        output = play_game(solution,oppunent,indicator) # play the game one time and return the winner and number of steps taking
        if indicator == output[0]: # if the player we are trying to optimize wins
          fitness = 100 / output[1] # give higher fitness value for less number of moves
        else: # if the player loses then give negative fitness
          fitness = -1
        return fitness


    num_generations = 10 # Number of generations.
    num_parents_mating = 2 # Number of solutions to be selected as parents in the mating pool.
    sol_per_pop = 10 # Number of solutions in the population.

    if indicator == 0:
      num_genes = 5   #white player have 5 parameters
    if indicator == 1:
      num_genes = 4 #black player have 4 parameters

    last_fitness = 0  #here to see if we are progressing at each iteration
    def on_generation(ga_instance):
        global last_fitness
        print(f"Generation = {ga_instance.generations_completed}")
        print(f"Fitness    = {ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]}")
        print(f"Change     = {ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1] - last_fitness}")
        last_fitness = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]

    gene_space = {'low': 0.0, 'high': 1.0} # keep the parameters between 0 and 1

    ga_instance = pygad.GA(num_generations=num_generations,
                          num_parents_mating=num_parents_mating,
                          sol_per_pop=sol_per_pop,
                          num_genes=num_genes,
                          fitness_func=fitness_func,
                          on_generation=on_generation,
                          gene_space=gene_space)

    # Running the GA to optimize the parameters and plot.
    ga_instance.run()
    ga_instance.plot_fitness()

    # Returning the details of the best solution.
    solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
    print(f"Parameters of the best solution : {solution}")
    print(f"Fitness value of the best solution = {solution_fitness}")
    print(f"Index of the best solution : {solution_idx}")

    if indicator == 0: #append best solution in the list, for each iteration
      wh_sol.append(solution)
    if indicator == 1:
      bl_sol.append(solution)

    # here we change the player for example:
    #if we were optimizing the white then we take the best white player
    # start to optimize the black players against the best white
    indicator = 1 - indicator  #change the player to optimize
    oppunent = solution   #play againest the best parameters from the previus iterations


with open("list.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(wh_sol)
    writer.writerow(bl_sol)