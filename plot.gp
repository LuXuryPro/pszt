set terminal pdf;
set logscale y
plot  'result.txt' using 1 with lines linestyle 1 lt rgb 'green' title "Rulette Best", \
      'result.txt' using 2 with lines linestyle 1 lt rgb 'blue' title "Rulette Worst",\
      'result.txt' using 3 with lines linestyle 1 title "Rulette Avg", \
      'result.txt' using 4 with lines linestyle 1 lt rgb 'green' title "Microbe Best", \
      'result.txt' using 5 with lines linestyle 1 lt rgb 'blue' title "Microbe Worst",\
      'result.txt' using 6 with lines linestyle 1 title "Microbe Avg", \
      'result.txt' using 7 with lines linestyle 1 lt rgb 'green' title "Best", \
      'result.txt' using 8 with lines linestyle 1 lt rgb 'blue' title "Worst",\
      'result.txt' using 9 with lines linestyle 1 title "Avg", \
