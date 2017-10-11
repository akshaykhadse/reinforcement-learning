############################# General template for experimentation #############################
# For tuning epsilon and alpha
: '
mdp=0
algo=qlearning
trials=50
ne=1600
tune=epsilon

for ep in $(seq 0.1 0.1 0.9) # Epsilon Values
do
    dir_name="mdp"$mdp"/"$algo"/"$tune"/"$ep # Result dir name
    mkdir -p $dir_name
    for((n=0;n<$trials;n++))
    do
        echo "----------------    Q Learning $n    ------------------"
        python3 ./server/server.py -port $((3000+$n)) -i $mdp -rs $n -ne $ne -q | tee $dir_name"/rs"$n".txt" &
        sleep 1
        python3 ./client/client.py -port $((3000+$n)) -rs $n -gamma 1 -algo $algo -ep $ep
    done
done
python3 results.py "mdp"$mdp"/"$algo"/"$tune"/"
'
############################# General template for experimentation #############################
# For tuning lambda
: '
mdp=0
algo=sarsa
trials=50
ne=500
tune=lambda
ep=0.2
al=0.8

for lm in $(seq 0.0 0.1 0.9) # Lambda Values
do
    dir_name="mdp"$mdp"/"$algo"/"$tune"/"$lm # Result dir name
    mkdir -p $dir_name
    for((n=0;n<$trials;n++))
    do
        echo "----------------    SARSA $n    ------------------"
        python3 ./server/server.py -port $((4000+$n)) -i $mdp -rs $n -ne $ne -q | tee $dir_name"/rs"$n".txt" &
        sleep 1
        python3 ./client/client.py -port $((4000+$n)) -rs $n -gamma 1 -algo $algo -ep $ep -al $al -lambda $lm
    done
done
python3 results-lambda.py "mdp"$mdp"/"$algo"/"$tune"/"
'
############################# Templeate for Generating Final Output #############################

mdp=0
algo=sarsa
trials=50
trace=replace
ne=2000
ep=0.2
al=0.8
lm=0.8 # 0.8 for mdp0 and 0.85 for mdp1

dir_name="results/mdp"$mdp"/"$algo
mkdir -p $dir_name
for((n=0;n<$trials;n++))
do
    echo "----------------    SARSA \0 $n    ------------------"
    python3 ./server/server.py -port $((5000+$n)) -i $mdp -rs $n -ne $ne -q | tee $dir_name"/rs"$n".txt" &
    sleep 1
    python3 ./client/client.py -port $((5000+$n)) -rs $n -gamma 1 -algo $algo -ep $ep -al $al -lambda $lm -trace $trace
done
python3 results-output.py "results/mdp"$mdp"/"

############################# Original Code #############################

: '
for((n=0;n<10;n++))
do
    echo "----------------    Q Learning $n    ------------------"
    python3 ./server/server.py -port $((4000+$n)) -i 0 -rs $n -ne 1600 -q | tee "results/random_rs$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((4000+$n)) -rs $n -gamma 1 -algo random
done
for((n=0;n<10;n++))
do
    echo "----------------    SARSA \0 $n    ------------------"
    python3 ./server/server.py -port $((5000+$n)) -i 0 -rs $n -ne 1600 -q | tee "results/sarsa_accum_lambda0_rs$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((5000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0
done
for((n=0;n<1;n++))
do
    echo "----------------    SARSA \0.2 $n    ------------------"
    python3 ./server/server.py -port $((6000+$n)) -i 5 -rs $n -ne 1600 -q | tee "results/sarsa_accum_lambda0.2_rs$n.txt" &
    sleep 1
    python3 ./client/client.py -port $((6000+$n)) -rs $n -gamma 1 -algo sarsa -lambda 0.2
done
'
