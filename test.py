#!/usr/bin/env python
# -*- coding: utf-8 -*-

import generation
import phenotype

size = 4
solution = phenotype.prepare_solution(size)
#g = generation.DifferantialEvolution(10, size)
#g = generation.MicrobalGaGeneration(3, size)
g = generation.Generation(5, size)
#g.set_destination(solution["solution_sum"], solution["solution_product"])
g.set_destination(0,24)
avg = []
i = 0
graph = 0
while 1:
    if graph:
        print(str(g.get_best().get_fitness()) + " " +
              str(g.get_worst().get_fitness()) + " " +
              str(g.get_avg_fitness())
              )
    else:
        g.get_best()
        print(solution['genotype'])
        print(g)
    if g.population[0].get_fitness() <= 0.01:
        break
    if len(avg) < 10:
        avg.append(g.get_avg_fitness())
    elif len(set(avg)) <= 1:
            break
    if i == 500:
        break
    g.step()
    i += 1
