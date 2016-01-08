#!/usr/bin/env python
# -*- coding: utf-8 -*-

import generation
import phenotype
import sys

size = 5
solution = phenotype.prepare_solution(size)
g = generation.Generation(10, size)
g.set_destination(solution["solution_sum"], solution["solution_product"])
graph = 0
i = 0
while 1:
    g.step()
    g.mutation()
    if graph:
        diff_max = g.population[0].get_fitness()
        print(str(diff_max))
        if diff_max == 1:
            break
    else:
        g.calc_fitness()
        print(solution['genotype'])
        print(g)
    if g.population[0].get_fitness() == 0:
        # print(i)
        break
    i += 1
