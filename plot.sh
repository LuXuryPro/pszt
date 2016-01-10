#!/bin/bash

./test.py > result.txt
gnuplot plot.gp | zathura -
