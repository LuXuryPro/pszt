#!/usr/bin/env python
# -*- coding: utf-8 -*-

import generation
import phenotype

size = 40
solution = phenotype.prepare_solution(size)
# g = generation.DifferentialEvolution(100, size)
g = generation.MicrobalGaGeneration(5, size)
# g = generation.Generation(100, size)
g.set_destination(solution["solution_sum"], solution["solution_product"])
avg = []
i = 0
graph = 1
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
    if i == 300:
        break
    g.step()
    i += 1
