#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import unittest
from unittest import mock


def prepare_solution(genotype_size):
    """
    Prepare example solution of size genotype_size. Return dict having desired
    sum and product, which we use as a model we want to achieve.
    @param genotype_size: number of bits to randomly shuffle
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
        else:
            if solution_product == 0:
                solution_product = 1
            solution_product *= (i + 1)

    destination = {}
    destination['solution_sum'] = solution_sum
    destination['solution_product'] = solution_product
    destination['genotype'] = genotype
    return destination


class Phenotype:
    """
    Main class describing our agents. It has genotype vector and all operations
    which are possible to run on it encapsulated inside itself.

    Init new Phenotype object. If you specify only size it will automatically
    generate random genotype.

    kwargs Parameters:

    size : int
        specify size for random genotype vector witch will be created for
        this Phenotype

    genotype : list
        if this parameter is specified it must be table containing binary
        numbers 0,1 at all indices. This table will be used as genotype for
        this Phenotype. Size parameter will be ignored.
    """

    def __init__(self, **kwargs):
        if "genotype" in kwargs.keys():
            if type(kwargs["genotype"]) != list:
                raise RuntimeError('Bad argument "genotype". Must be list')
            for i in kwargs["genotype"]:
                if not (i == 0 or i == 1):
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

        # that ones will be compute later
        self.fitness = 0.0
        self.influence = 0.0

    def __str__(self):
        st = "===Genotype===\n"
        s = "".join([str(x) for x in self.genotype])
        s = (st + "Genotype: " + s + " Fitness: " + str(self.fitness) +
             " Influence: " + str(self.influence))
        group_a = []
        group_b = []
        for position, value in enumerate(self.genotype):
            if value == 0:
                group_a.append(position + 1)
            else:
                group_b.append(position + 1)
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
        self.influence = (float(maximum - self.fitness + 1) /
                          float(i * (maximum + 1) - s))

    def mutation(self, p, bit_probability_table):
        """Flip a bit on a random position. """
        # for bit in enumerate(self.genotype):
        bit = random.randint(0, len(self.genotype) - 1)
        probability_of_mutation = bit_probability_table[bit] * p
        dice = random.random()
        if dice < probability_of_mutation:
            self.genotype[bit] ^= 1  # flip bit

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
        """
        For given parameters calculates how close are we from the best
        solution. If this function returns 0 we found it. The function is
        defined as:
        f(sum, product) = |solution_sum - sum| + |solution_product - product|
        where |x| is absolute value of number x
        @param solution_sum: sum of destination agent
        @param solution_product: product of destination agent
        """
        s = 0
        i = 0
        for x in range(len(self.genotype)):
            if self.genotype[x] == 0:
                s += (x + 1)
            else:
                if i == 0:
                    i = 1
                i *= (x + 1)

        sum_diff = float(solution_sum - s) / float(solution_sum + 1)
        prod_diff = float(solution_product - i) / float(solution_product + 1)
        self.fitness = abs(sum_diff) + abs(prod_diff)


class TestPhenotypeMethods(unittest.TestCase):
    def test_calc_fitness_function(self):
        p = Phenotype(genotype=[0, 0, 0, 1])
        p.calc_fitness_function(6, 4)
        self.assertEqual(p.get_fitness(), 0)

        p = Phenotype(genotype=[1, 0, 0, 1])
        p.calc_fitness_function(4, 3)
        self.assertEqual(p.get_fitness(), 0.45)

        p = Phenotype(genotype=[1, 0])
        p.calc_fitness_function(2, 1)
        self.assertAlmostEqual(p.get_fitness(), 0)

        p = Phenotype(genotype=[1, 0])
        p.calc_fitness_function(1, 2)
        self.assertAlmostEqual(p.get_fitness(), 0.8333333)

    def test_prepare_solution(self):
        prepare_solution(10)

    @mock.patch('random.randint')
    @mock.patch('random.random')
    def test_mutation(self, mock_random, mock_randint):
        mock_random.return_value = 0
        mock_randint.return_value = 0
        p = Phenotype(genotype=[1, 1, 1])
        p.mutation(1, [1, 1, 1])
        self.assertEqual(p.get_genotype(), [0, 1, 1])

    @mock.patch('random.randint')
    def test_crossover(self, mock_randint):
        mock_randint.return_value = 1  # split 2 element list in half
        mother = Phenotype(genotype=[1, 1])
        father = Phenotype(genotype=[0, 0])
        children = mother.crossover(father)
        self.assertEqual(children['a'].get_genotype(), [1, 0])
        self.assertEqual(children['b'].get_genotype(), [0, 1])

    def test_constructor(self):
        self.assertRaises(RuntimeError, Phenotype, genotype=1)
        self.assertRaises(RuntimeError, Phenotype, genotype=[2, 3])
        self.assertRaises(RuntimeError, Phenotype, size=[])
        self.assertRaises(RuntimeError, Phenotype)
        p = Phenotype(size=10)
        self.assertEqual(len(p.get_genotype()), 10)

    def test_phenotype_str_operator(self):
        g = Phenotype(genotype=[1, 0, 1, 0])
        gstr = str(g)

if __name__ == '__main__':
    unittest.main()
