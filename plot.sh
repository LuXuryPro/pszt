#!/bin/bash

./test1.py >result.txt
gnuplot plot.gp | zathura -
