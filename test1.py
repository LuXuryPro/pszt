#!/usr/bin/env python
# -*- coding: utf-8 -*-

import generation
import phenotype

size = 10
solution = phenotype.prepare_solution(size)
mg = generation.MicrobalGaGeneration(10, size)
mg.set_destination(solution["solution_sum"], solution["solution_product"])
g = generation.Generation(10, size)
g.set_destination(solution["solution_sum"], solution["solution_product"])
r = generation.RuletteGeneration(10,size)
r.set_destination(solution["solution_sum"], solution["solution_product"])

i = 0
while 1:
    print(str(g.get_best().get_fitness()) + " " +
          str(g.population[-1].get_fitness()) + " " +
          str(g.get_avg_fitness())
          )
    print(str(r.get_best().get_fitness()) + " " +
          str(r.population[-1].get_fitness()) + " " +
          str(r.get_avg_fitness()) + " " +
          str(mg.get_best().get_fitness()) + " " +
          str(mg.population[-1].get_fitness()) + " " +
          str(mg.get_avg_fitness()) + " " +
          str(g.get_best().get_fitness()) + " " +
          str(g.population[-1].get_fitness()) + " " +
          str(g.get_avg_fitness())
          )
    if (g.population[0].get_fitness() == 0 and
            mg.population[0].get_fitness() == 0 and
            r.population[0].get_fitness() == 0
        ):
        break
    g.step()
    mg.step()
    r.step()
    i += 1
