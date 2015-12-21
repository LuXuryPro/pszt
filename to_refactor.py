#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pdb
import argparse

parser = argparse.ArgumentParser(description='Genetic algorithm')
parser.add_argument('-n',
                    '--problem-size',
                    help='Size of problem (number of cards)',
                    required=True,
                    type=int)
parser.add_argument('-p',
                    '--population-size',
                    help='Size of population (number of agents)',
                    required=True,
                    type=int)
args = parser.parse_args()


def prepare_solution(genotype_size):
    """ Prepare example solution of size genotype_size. Return dict having
    desired sum and product, which we use as a model we want to achieve.
    """
    genotype = [random.randint(0, 1) for x in range(genotype_size)]
    solution_sum = 0
    solution_product = 0
    for i in enumerate(genotype):
        if genotype[i] == 0:
            solution_sum += (x + 1)
        elif genotype[i] == 1:
            if solution_product == 0:
                solution_product = 1
            solution_product *= (x + 1)

    destination = {}
    destination['s'] = s
    destination['i'] = i
    destination['genotype'] = genotype
    return destination


class Phenotype:
    """Main class describling our agents. It has genotype vector and all
    operations witch are possible to run on it encapsulated inside itself.
    """
    def __init__(self, **kwargs):
        """Init new Phenotype object. If you specify only size it will
        automatically generate random genotype.
        Parameters:
        size - specify size for random genotype vector witch will be created
        for this Phenotype
        genotype - if this parametr is specified it must be table containing
        binary numbers 0,1 at all indices. This table will be used as genotype
        for this Phenotype. Size parameter will be ignored.
        """
        if "genotype" in kwargs.keys():
            if type(kwargs["genotype"]) != list:
                raise RuntimeError('Bad argument "genotype". Must be list')
            for i in kwargs["genotype"]:
                if not (i != 0 or i != 1):
                    raise RuntimeError('Bad "argument" genotype. '
                                       "Not a binary list")
            self.genotype = kwargs["genotype"]
        elif "size" in kwargs.keys():
            if type(kwargs["genotype"]) != int:
                raise RuntimeError('Bad argument "size". Must be int')
            self.genotype = [random.randint(0, 1)
                             for x in range(kwargs["size"])]
        else:
            raise RuntimeError("Bad arguments")

        # that ones will be computer later
        self.fitness = 0.0
        self.influence = 0.0

    def __str__(self):
        s = "".join([str(x) for x in self.genotype])
        s = "Genotype: " + s + " Fitness: " + str(self.fitness)
        return s

    def __repr__(self):
        return self.__str__()

    def set_bit(self, index, bit):
        self.genotype[index] = bit % 2

    def get_bit(self, index):
        return self.genotype[index]

    def get_genotype(self):
        return self.genotype

    def get_size(self):
        return len(self.genotype)

    def get_fitness(self):
        return self.fitness

    def get_influence(self):
        return self.influence

    def calc_influence(self, s, maximum, i):
        """Instead of killing agent with the lowest fittest we use this formula.
        It is improving speed of finding the best solution"""
        self.influence = (maximum - self.fitness + 1)/(i * (maximum + 1) - s)

    def mutation(self):
        """Flip a bit on a random position. """
        position = random.randint(0, len(self.genotype) - 1)
        self.genotype[position] ^= 1  # flip bit

    def crossover(self, other):
        """Select a random index in genotype. Child A gets all bits before it,
        from self genotype and the rest from other. Child B vice versa."""
        position = random.randint(0, len(self.genotype) - 1)
        children_a = []
        children_b = []
        for x in range(len(self.genotype)):
            if x < position:
                children_a.append(self.genotype[x])
                children_b.append(other.genotype[x])
            else:
                children_b.append(self.genotype[x])
                children_a.append(other.genotype[x])

        return {'a': Phenotype(0, children_a), 'b': Phenotype(0, children_b)}

    def calc_fitness_function(self, solution_sum, solution_product):
        """For given parameters calculates how close are we from the best
        solution. If this function returns 0 we found it. The function is
        defined as:
        f(sum, product) = |solution_sum - sum| + |solution_product - product|
        where || is absolute value of number
        """
        s = 0
        i = 0
        for x in range(len(self.genotype)):
            if self.genotype[x] == 0:
                s += (x + 1)
            elif self.genotype[x] == 1:
                if i == 0:
                    i = 1
                i *= (x + 1)

        self.fitness = (abs(solution_sum-s) + abs(solution_product-i))


# normal algorithm
for solution_size in range(args.problem_size, args.problem_size + 1):
    # TODO: zrobic parser argumentow
    solution = prepare_solution(solution_size)
    print("Solution: " + str(solution['genotype']))
    # print ("Solution: " + str(solution))
    for population_size in range(args.population_size,
                                 args.population_size + 1):
        # TODO: zrobic parser argumentow
        population = [Phenotype(solution_size) for x in range(population_size)]
        j = 0
        while 1:
            for x in population:
                x.calc_fitness_function(solution['s'], solution['i'])

            s = 0
            m = 0

            # Sum all influences and get the biggest one - we will use it
            # in calc_influence
            for ageng in population:
                s += ageng.get_fitness()
                if m < ageng.get_fitness():
                    m = ageng.get_fitness()

            for x in population:
                x.calc_influence(s, m, len(population))

            population.sort(key=lambda x: x.get_influence(), reverse=True)

            print(str(solution_size) + "\t" + str(population_size) + "\t" + str(j) + "\t" + str(population[0]))
            if population[0].get_fitness() == 0:  # We found the best solution
                break

            # Mutation
            i = 0
            while (i < population[0].get_fitness()*population_size/5 and
                   i < (len(population) - 1)):
                population[random.randint(0, population_size-1)].mutation()
                i += 1

            # Get rid of half of the population
            population = population[0:population_size]
            print (population)
            #print (population)
            #print (str(j) +  ": " + str(population[0].get_influence()) + " " + str(population[0].get_fitness()))
            #input("Press Enter to continue...")


            # Crossovers
            i = 0
            while i < population[0].get_fitness() and i < (len(population) - 1):
                one = population[i]
                i += 1
                second = population[i]
                i += 1
                r = one.crossover(second)
                r['a'].mutation()
                r['b'].mutation()
                population.append(r['a'])
                population.append(r['b'])

            j += 1

        #print ("Ilosc genow: " + str(solution_size) + " Wielkosc populacji: " + str(population_size) + " => Rozwiazanie: po " + str(j) + " iteracjach" +  ": " + str(population[0]))


#differential evolution algorithm
def differential_evolution_algorith():
    for solution_size in range(1,20):
        solution = prepare_solution(solution_size)
        #differential weight [0,2]
        F=1
        #crossover probability [0,1]
        CR=0.5
        #IMPORTANT population min size needs to be 4 agents
        for population_size in range(4,20):
            population = [Phenotype(solution_size) for x in range(population_size)]
            v = 0
            for l in range(100):
                v += 1
                for j in range(population_size):
                    x = random.randint(0,population_size - 1)
                    a = x
                    b = x
                    c = x
                    while a == x:
                        a = random.randint(0,population_size - 1)
                    while b == x or b == a:
                        b = random.randint(0,population_size-1)
                    while c == x or c == a or c == b:
                        c = random.randint(0,population_size-1)
                    R = random.randint(0, solution_size - 1)
                    candidate = Phenotype(None, population[x].get_genotype())
                    for k in range(solution_size):
                        if random.randint(0, solution_size - 1) == R or random.random() < CR:
                            candidate.set_bit(k, population[a].get_bit(k) + F*(population[b].get_bit(k)-population[c].get_bit(k)))
                    population[x].calc_fitness_function(solution['s'], solution['i'])
                    candidate.calc_fitness_function(solution['s'], solution['i'])
                    if candidate.get_fitness() == 0:
                        break
                    if candidate.get_fitness() > population[x].get_fitness():
                        del population[x]
                        population.append(candidate)
                best_solution = population[0]
                for c in population[1:]:
                    c.calc_fitness_function(solution['s'], solution['i'])
                    if c.get_fitness() < best_solution.get_fitness():
                        best_solution = c

                #if c is valid solution
                if best_solution.get_fitness() == 0:
                    print (str(solution_size) + "\t" + str(population_size) + "\t" + str(v))
                    break
                #else:
                    #print (str(solution_size) + "\t" + str(population_size) + "\t" + str(l) + "\t" + str(best_solution))
