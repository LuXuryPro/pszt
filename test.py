#!/usr/bin/env python
# -*- coding: utf-8 -*-

import generation
import phenotype
import argparse

parser = argparse.ArgumentParser(
        description='Genetic Algorithm')
parser.add_argument(
        '--population-size',
        required=True,
        type=int)

parser.add_argument(
        '--destination',
        help="Binary string representing destination agent",
        required=True,
        type=str)

parser.add_argument(
        '--algorithm',
        help="Binary string representing destination agent",
        required=False,
        choices=["s", "m", "d"]
        )

args = parser.parse_args()
if not args.algorithm:
    args.algorithm = "s"


genotype = [int(x) for x in args.destination]
solution_sum = 0
solution_product = 0
for i in range(len(genotype)):
    if genotype[i] == 0:
        solution_sum += (i + 1)
    elif genotype[i] == 1:
        if solution_product == 0:
            solution_product = 1
        solution_product *= (i + 1)
groups = ""
group_a = []
group_b = []
for position, value in enumerate(genotype):
    if value == 0:
        group_a.append(position + 1)
    elif value == 1:
        group_b.append(position + 1)
groups += "Group 1: " + str(group_a) + "\n"
groups += "Group 2: " + str(group_b) + "\n"



size = len(genotype)
if args.algorithm == "s":
    g = generation.Generation(args.population_size, size)
elif args.algorithm == "m":
    g = generation.MicrobalGaGeneration(args.population_size, size)
elif args.algorithm == "d":
    g = generation.DifferantialEvolution(args.population_size, size)
g.set_destination(solution_sum, solution_product)
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
        print("Solution genotype = " + str(genotype))
        print("Solution sum = " + str(solution_sum))
        print("Solution product = " + str(solution_product))
        print(groups)
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

print("Num steps = " + str(i))
