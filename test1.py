#!/usr/bin/env python
# -*- coding: utf-8 -*-

import generation
import phenotype

size = 20
solution = phenotype.prepare_solution(size)
g = generation.Generation(10, size)
g.set_destination(solution["solution_sum"], solution["solution_product"])

i = 0
while 1:
    g.calc_fitness()
    print(g)
    if g.population[0].get_fitness() == 0:
        print(i)
        break
    g.step()
    i += 1
