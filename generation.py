#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import phenotype
import math
import ipdb


class Generation:
    def __init__(self, number_of_individuals, size_of_genotype):
        self.population = [phenotype.Phenotype(size=size_of_genotype)
                           for i in range(number_of_individuals)]
        self.num_iterations = 0
        self.number_of_individuals = number_of_individuals

    def __str__(self):
        s = "\n".join([str(x) for x in self.population])
        s = "Population: \n" + s
        return s

    def set_destination(self, destination_sum, destination_product):
        self.destination_sum = destination_sum
        self.destination_product = destination_product

    def calc_fitness(self):

        for individiual in self.population:
            individiual.calc_fitness_function(self.destination_sum,
                                              self.destination_product)

        curr_f = self.population[0].get_fitness()
        curr_rank = len(self.population)
        for agent in self.population:
            if agent.get_fitness() == curr_f:
                agent.fitness = curr_rank
            else:
                curr_rank -= 1
                curr_f = agent.get_fitness()
                agent.fitness = curr_rank

        s = 0
        # Sum all influences and get the biggest one - we will use it
        # in calc_influence
        for agent in self.population:
            s += agent.get_fitness()

        f_ave = 0
        for x in self.population:
            f_ave += x.get_fitness()

        f_ave /= len(self.population)

        f_max = 0
        for x in self.population:
            if x.get_fitness() > f_max:
                f_max = x.get_fitness()

        c = 2
        a = (c*f_ave - f_ave)/(f_max - f_ave)
        b = c*f_ave - a*f_max

        for x in self.population:
            x.fitness = a*x.fitness + b

        for x in self.population:
            x.calc_influence(s)

    def mutation(self):
        i = 0
        p = 1
        while i < self.number_of_individuals*0.1:
            self.population[
                    random.randint(0, len(self.population) - 1)
                    ].mutation(p)
            i += 1

    def selection(self):
        pass

    def step(self):
        """Do one step of generation including mutations, crossovers, and
        selection.
        TODO This will be overwriten by child class
        """
        self.calc_fitness()

        # select parents
        parents = []

        for i in self.population:
            # roll dice
            dice = random.random()
            for agent in self.population:
                dice -= agent.get_influence()
                if dice <= 0:
                    parents.append(agent)
                    break

        assert(len(parents) == len(self.population))

        list_of_indices = list(range(self.number_of_individuals))

        assert(self.number_of_individuals % 2 == 0)

        fitness_sum = 0
        for parent in parents:
            fitness_sum += parent.get_fitness()

        probability_of_mutation = 1 - math.exp(-fitness_sum*0.001)

        childrens = []
        for pair in range(int(self.number_of_individuals/2)):
            first = random.randint(0, len(list_of_indices) - 1)
            del list_of_indices[first]
            second = random.randint(0, len(list_of_indices) - 1)
            del list_of_indices[second]

            first_parent = parents[first]
            second_parent = parents[second]

            children = first_parent.crossover(second_parent)
            children['a'].mutation(probability_of_mutation)
            children['b'].mutation(probability_of_mutation)
            first_parent.calc_fitness_function(self.destination_sum, self.destination_product)
            second_parent.calc_fitness_function(self.destination_sum, self.destination_product)
            children['a'].calc_fitness_function(self.destination_sum, self.destination_product)
            children['b'].calc_fitness_function(self.destination_sum, self.destination_product)

            selector = []
            selector.append(first_parent)
            selector.append(second_parent)
            selector.append(children['a'])
            selector.append(children['b'])
            selector.sort(key=lambda x: x.get_fitness(), reverse=True)

            childrens.append(selector[0])
            childrens.append(selector[1])

        assert(len(childrens) == len(self.population))
        self.population = childrens
