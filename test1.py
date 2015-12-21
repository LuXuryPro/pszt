#!/usr/bin/env python
# -*- coding: utf-8 -*-

import generation
import phenotype

solution = phenotype.prepare_solution(4)
g = generation.Generation(10, 4)
g.set_destination(solution["solution_sum"], solution["solution_product"])

for i in range(100):
    g.step()
    print(g)
