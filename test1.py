#!/usr/bin/env python
# -*- coding: utf-8 -*-

import generation
import phenotype

size = 50
solution = phenotype.prepare_solution(size)
#g = generation.DifferantialEvolution(15, size)
g = generation.MicrobalGaGeneration(100, size)
#g = generation.Generation(100, size)
g.set_destination(solution["solution_sum"], solution["solution_product"])
avg = []
i = 0
while 1:
    print(
          str(g.get_best().get_fitness()) + " " +
          str(g.get_worst().get_fitness()) + " " +
          str(g.get_avg_fitness())
          )
    if (g.population[0].get_fitness() <= 0.01):
        break
    if len(avg) < 5:
        avg.append(g.get_avg_fitness())
    elif len(set(avg)) <= 1:
            break
    g.step()
    i += 1
