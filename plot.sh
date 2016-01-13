#!/bin/bash

./test.py > result.txt
gnuplot plot.gp > result.png
