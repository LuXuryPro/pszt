#!/usr/bin/env python
# -*- coding: utf-8 -*-

import generation
import phenotype

size = 10
solution = phenotype.prepare_solution(size)
g = generation.Generation(10, size)
g.set_destination(solution["solution_sum"], solution["solution_product"])

i = 0
while 1:
    print(str(g.get_best().get_fitness()) + " " +
          str(g.population[-1].get_fitness())
          )
    if g.population[0].get_fitness() == 0:
        break
    g.step()
    i += 1
