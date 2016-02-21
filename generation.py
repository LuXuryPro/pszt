#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import random
import unittest

import phenotype


def prepare_lookup_table(size_of_genotype):
    """
    @param size_of_genotype:
    @return:
    """
    p = 100
    bit_probability_table = []
    for bit in range(size_of_genotype):
        if bit != size_of_genotype - 1:
            # Bit is not last one
            bit_probability = 100 / (2**(bit + 1))
            p -= bit_probability
        else:
            # This is last bit so give it ramaining probability
            bit_probability = p
        bit_probability_table.append(bit_probability)
    return bit_probability_table


class Generation:
    """Generic generation class. It contains common fields for all other
    algorithm variations.
    """

    def __init__(self, number_of_individuals, size_of_genotype):
        self.population = [phenotype.Phenotype(size=size_of_genotype)
                           for i in range(number_of_individuals)]
        self.num_iterations = 0
        self.number_of_individuals = number_of_individuals
        self.destination_sum = 0
        self.destination_product = 0
        self.bit_probability_table = prepare_lookup_table(size_of_genotype)

    def __str__(self):
        s = "\n".join([str(x) for x in self.population])
        s = "\n\n************Population: **************\n" + s + "\n\n"
        return s

    def set_destination(self, destination_sum, destination_product):
        self.destination_sum = destination_sum
        self.destination_product = destination_product

    def calc_fitness(self):
        """
        Fitness calculation based on actual fitness function
        """
        for individual in self.population:
            individual.calc_fitness_function(self.destination_sum,
                                             self.destination_product)

        s = 0
        m = 0

        # Sum all influences and get the biggest one - we will use it
        # in calc_influence
        for agent in self.population:
            s += agent.get_fitness()
            if m < agent.get_fitness():
                m = agent.get_fitness()

        for x in self.population:
            x.calc_influence(s, m, self.number_of_individuals)

        self.population.sort(key=lambda x: x.get_influence(), reverse=True)

    def mutation(self):
        i = 0
        while i < self.number_of_individuals * 0.1:
            self.population[
                random.randint(0, len(self.population) - 1)].mutation()
            i += 1

    def get_best(self):
        for individual in self.population:
            individual.calc_fitness_function(self.destination_sum,
                                             self.destination_product)
            self.population.sort(key=lambda x: x.get_fitness(), reverse=False)
        return self.population[0]

    def get_worst(self):
        self.get_best()  # sorts population
        return self.population[-1]

    def get_avg_fitness(self):
        fitness_sum = 0.0
        for individual in self.population:
            individual.calc_fitness_function(self.destination_sum,
                                             self.destination_product)
            fitness_sum += individual.get_fitness()

        return float(fitness_sum) / float(self.number_of_individuals)

    def step(self):
        i = 0
        while (i < self.population[0].get_fitness() *
               self.number_of_individuals * 10 and
               i < (len(self.population) - 1)):
            self.population[
                random.randint(0, self.number_of_individuals - 1)].mutation(
                    0.5, self.bit_probability_table)
            i += 1

        # Crossovers
        i = 0
        while (i < 10 * self.population[0].get_fitness() and
               i < (len(self.population) - 1)):
            one = self.population[i]
            i += 1
            second = self.population[i]
            i += 1
            r = one.crossover(second)
            r['a'].mutation(0.01, self.bit_probability_table)
            r['b'].mutation(0.01, self.bit_probability_table)
            self.population.append(r['a'])
            self.population.append(r['b'])

        self.get_best()
        # Get rid of half of the population
        self.population = self.population[0:self.number_of_individuals]
        assert (len(self.population) == self.number_of_individuals)


class MicrobalGaGeneration(Generation):
    def step(self):
        """Do one step of generation including mutations, crossovers, and
        selection.
        TODO This will be overwrr+iten by child class
        """

        a = random.choice(self.population)
        b = random.choice(self.population)

        a.calc_fitness_function(self.destination_sum, self.destination_product)
        b.calc_fitness_function(self.destination_sum, self.destination_product)

        if a.get_fitness() < b.get_fitness():
            w = a
            l = b
        elif b.get_fitness() < a.get_fitness():
            w = b
            l = a
        else:
            return

        for bit in enumerate(w.genotype):
            if random.random() < 0.5:
                l.genotype[bit[0]] = bit[1]
            if random.random() < 0.1 * self.bit_probability_table[bit[0]]:
                l.genotype[bit[0]] ^= 1


class RuletteGeneration(Generation):
    def mutation(self):
        i = 0
        p = 1
        while i < self.number_of_individuals * 0.1:
            self.population[
                random.randint(0, len(self.population) - 1)].mutation(p)
            i += 1

    def step(self):
        self.calc_fitness()

        # select parents
        parents = []
        self.get_best()

        for i in self.population:
            # roll dice
            dice = random.random()
            for agent in self.population:
                dice -= agent.get_influence()
                if dice <= 0:
                    parents.append(agent)
                    break

        assert (len(parents) == len(self.population))

        list_of_indices = list(range(self.number_of_individuals))

        assert (self.number_of_individuals % 2 == 0)

        fitness_sum = 0
        for parent in parents:
            fitness_sum += parent.get_fitness()

        probability_of_mutation = 1 - math.exp(-fitness_sum * 0.001)

        childrens = []
        for pair in range(int(self.number_of_individuals / 2)):
            first = random.randint(0, len(list_of_indices) - 1)
            del list_of_indices[first]
            second = random.randint(0, len(list_of_indices) - 1)
            del list_of_indices[second]

            first_parent = parents[first]
            second_parent = parents[second]

            children = first_parent.crossover(second_parent)
            children['a'].mutation(probability_of_mutation)
            children['b'].mutation(probability_of_mutation)
            first_parent.calc_fitness_function(self.destination_sum,
                                               self.destination_product)
            second_parent.calc_fitness_function(self.destination_sum,
                                                self.destination_product)
            children['a'].calc_fitness_function(self.destination_sum,
                                                self.destination_product)
            children['b'].calc_fitness_function(self.destination_sum,
                                                self.destination_product)

            selector = []
            selector.append(first_parent)
            selector.append(second_parent)
            selector.append(children['a'])
            selector.append(children['b'])
            selector.sort(key=lambda x: x.get_fitness(), reverse=True)

            childrens.append(selector[0])
            childrens.append(selector[1])

        assert (len(childrens) == len(self.population))
        self.population = childrens


class DifferentialEvolution(Generation):
    def step(self):
        # differential weight [0,2]
        F = 1
        # crossover probability [0,1]
        CR = 0.5
        for j in range(self.number_of_individuals):
            x = random.randint(0, self.number_of_individuals - 1)
            a = x
            b = x
            c = x
            while a == x:
                a = random.randint(0, self.number_of_individuals - 1)
            while b == x or b == a:
                b = random.randint(0, self.number_of_individuals - 1)
            while c == x or c == a or c == b:
                c = random.randint(0, self.number_of_individuals - 1)
            R = random.randint(0, len(self.population[0].genotype) - 1)
            candidate = phenotype.Phenotype(
                genotype=self.population[x].get_genotype())
            for k in range(len(self.population[0].genotype)):
                if (random.randint(0, len(self.population[0].genotype) - 1) ==
                        R or random.random() < CR):
                    candidate.set_bit(k, (self.population[a].get_bit(k) + F *
                                          (self.population[b].get_bit(k) -
                                           self.population[c].get_bit(k))))
                    self.population[x].calc_fitness_function(
                        self.destination_sum, self.destination_product)
                    candidate.calc_fitness_function(self.destination_sum,
                                                    self.destination_product)
                    if candidate.get_fitness() == 0:
                        break
            if candidate.get_fitness() > self.population[x].get_fitness():
                del self.population[x]
                self.population.append(candidate)


class TestGenerationMethods(unittest.TestCase):
    def test_get_best(self):
        g = Generation(4, 2)
        g.set_destination(3, 0)  # 00 bits
        g.population[0].genotype = [0, 0]
        selected_best = g.population[0]
        g.population[1].genotype = [1, 1]
        g.population[2].genotype = [1, 0]
        g.population[3].genotype = [0, 1]
        best = g.get_best()
        self.assertEqual(best, selected_best)

    def test_get_avg_fitness(self):
        g = Generation(4, 2)
        g.set_destination(3, 0)  # 00 bits
        g.population[0].genotype = [0, 0]
        g.population[1].genotype = [0, 0]
        g.population[2].genotype = [0, 0]
        g.population[3].genotype = [0, 0]
        self.assertEqual(g.get_avg_fitness(), 0)

    def test_prepare_lookup_table(self):
        print(prepare_lookup_table(5))


if __name__ == '__main__':
    unittest.main()
