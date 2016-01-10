set terminal pdf;
set logscale y;
#set xrange [0:300];
#set yrange [0:10];
plot 'result.txt' using 1 with lines linestyle 1 lt rgb '#FA076C' title "Best", \
    'result.txt' using 3 with lines linestyle 1 lt rgb '#6007FA' title "Avg", \
    'result.txt' using 2 with lines linestyle 1 lt rgb '#07FA95' title "Worst" \
