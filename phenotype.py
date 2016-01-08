#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
import random
import unittest


def prepare_solution(genotype_size):
    """ Prepare example solution of size genotype_size. Return dict having
    desired sum and product, which we use as a model we want to achieve.
    Returns dict having two keys:
    - solution_sum
    - solution_product
    """
    genotype = [random.randint(0, 1) for x in range(genotype_size)]
    solution_sum = 0
    solution_product = 0
    for i in range(len(genotype)):
        if genotype[i] == 0:
            solution_sum += (i + 1)
        elif genotype[i] == 1:
            if solution_product == 0:
                solution_product = 1
            solution_product *= (i + 1)

    destination = {}
    destination['solution_sum'] = solution_sum
    destination['solution_product'] = solution_product
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
            if type(kwargs["size"]) != int:
                raise RuntimeError('Bad argument "size". Must be int')
            self.genotype = [random.randint(0, 1)
                             for x in range(kwargs["size"])]
        else:
            raise RuntimeError("Bad arguments")

        # that ones will be computer later
        self.fitness = 0.0
        self.influence = 0.0

    def __str__(self):
        st = "===Genotype===\n"
        s = "".join([str(x) for x in self.genotype])
        s = st + "Genotype: " + s + " Fitness: " + str(self.fitness) + " Influence: " + str(self.influence)
        group_a = []
        group_b = []
        for bit in enumerate(self.genotype):
            if bit[1] == 0:
                group_a.append(bit[0] + 1)
            elif bit[1] == 1:
                group_b.append(bit[0] + 1)
        s += "\n"
        s += "Group 1: " + str(group_a) + "\n"
        s += "Group 2: " + str(group_b) + "\n"
        s += "========================="
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
        self.influence = float(maximum - self.fitness + 1)/float(i * (maximum + 1) - s)

    def mutation(self):
        """Flip a bit on a random position. """
        p = 0.5 # mutation probability
        for bit in enumerate(self.genotype):
            dice = random.random()
            if dice < p:
                self.genotype[bit[0]] ^= 1  # flip bit

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

        return {'a': Phenotype(genotype=children_a),
                'b': Phenotype(genotype=children_b)}

    def calc_fitness_function(self, solution_sum, solution_product):
        """For given parameters calculates how close are we from the best
        solution. If this function returns 0 we found it. The function is
        defined as:
        f(sum, product) = |solution_sum - sum| + |solution_product - product|
        where |x| is absolute value of number x
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

        sum_diff = float(solution_sum - s) / float(solution_sum)
        prod_diff = float(solution_product - i) / float(solution_product)
        self.fitness = abs(sum_diff) + abs(prod_diff)



class TestPhenotypeMethods(unittest.TestCase):

  def test_mutation(self):
      p = Phenotype(size=10)
      p.mutation()

  def test_calc_fitness_function(self):
      p = Phenotype(genotype=[0,0,0,1])
      p.calc_fitness_function(6,4)
      self.assertEqual(p.get_fitness(), 0)

      p = Phenotype(genotype=[1,0,0,1])
      p.calc_fitness_function(4,3)
      self.assertEqual(p.get_fitness(), 2)

      p = Phenotype(genotype=[1,0])
      p.calc_fitness_function(2,1)
      self.assertEqual(p.get_fitness(), 0)

      p = Phenotype(genotype=[1,0])
      p.calc_fitness_function(1,2)
      self.assertEqual(p.get_fitness(), 2)

if __name__ == '__main__':
    unittest.main()
