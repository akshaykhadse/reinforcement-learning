rm -rf report
########### Experiment 1 ###########
dir_name="report/ex1"
mkdir -p $dir_name
./startmdp.sh 1 1000000 0 1 1 1 1 1 1 1 > $dir_name"/result.txt"
python3 plot_graph.py 1

########### Experiment 2 ###########
dir_name="report/ex2"
mkdir -p $dir_name
for lamd in 0.0 0.2 0.4 0.6 0.8 1.0
do
    ./startmdp.sh 2 1000000 $lamd 1 1 1 1 1 1 1 > $dir_name"/"$lamd".txt"
done
python3 plot_graph.py 2
