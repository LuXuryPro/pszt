#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pdb



def prepare_solution(genotype_size):
    """ Prepare example solution of size genotype_size
    return dict having desired sum and product
    """
    genotype = [random.randint(0,1) for x in range(genotype_size)]
    s = 0
    i = 0
    for x in range(len(genotype)):
        if genotype[x] == 0:
            s += (x + 1)
        elif genotype[x] == 1:
            if i == 0:
                i = 1
            i *= (x + 1)

    d = {}
    d['s'] = s
    d['i'] = i
    return d

class Phenotype:
    def __init__(self, size = None, genotype = None):
        if genotype:
            self.genotype = genotype
        else:
            self.genotype = [random.randint(0,1) for x in range(size)]
        self.fitness = 0.0
        self.influence = 0.0
    def __str__(self):
        s = "".join([str(x) for x in self.genotype])
        s += " Fitness: " + str(self.fitness)
        return s
    def __repr__(self):
        return self.__str__()
    def get_fitness(self):
        return self.fitness
    def get_influence(self):
        return self.influence
    def calc_influence(self, s, maximum, i):
        self.influence = ( maximum - self.fitness + 1 )/( i*( maximum + 1 ) - s )
    def mutation(self):
        position = random.randint(0,len(self.genotype) - 1)
        self.genotype[position] ^= 1 #flip bit
    def crossover(self, other):
        position = random.randint( 0, len( self.genotype ) - 1 )
        childeren_a = []
        childeren_b = []
        for x in range(len(self.genotype)):
            if x < position:
                childeren_a.append(self.genotype[x])
                childeren_b.append(other.genotype[x])
            else:
                childeren_b.append(self.genotype[x])
                childeren_a.append(other.genotype[x])

        return {'a': Phenotype(0, childeren_a), 'b': Phenotype(0, childeren_b)}

    def calc_fitness_function(self, solution_sum, solution_product):
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


for solution_size in range(1,14):
    solution = prepare_solution(solution_size)
    #print ("Solution: " + str(solution))
    for population_size in range(2,51):
        population = [Phenotype(solution_size) for x in range(population_size)]
        j = 0
        while 1:
            for x in population:
                x.calc_fitness_function(solution['s'], solution['i'])

            s = 0
            m = 0

            for x in population:
                s += x.get_fitness()
                if m < x.get_fitness():
                    m = x.get_fitness()

            for x in population:
                x.calc_influence(s,m,len(population))

            population.sort(key=lambda x: x.get_influence(), reverse=True)
            if population[0].get_fitness() == 0:
                break
            i = 0
            while i < population[0].get_fitness()*population_size/5 and i < (len(population) - 1):
                population[random.randint(0, population_size-1)].mutation()
                i += 1

            population = population[0:population_size]
            #print (population)
            #print (str(j) +  ": " + str(population[0].get_influence()) + " " + str(population[0].get_fitness()))
            #input("Press Enter to continue...")

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
            j+=1

        #print ("Ilosc genow: " + str(solution_size) + " Wielkosc populacji: " + str(population_size) + " => Rozwiazanie: po " + str(j) + " iteracjach" +  ": " + str(population[0]))
        print (str(solution_size) + "\t" + str(population_size) + "\t" + str(j))
