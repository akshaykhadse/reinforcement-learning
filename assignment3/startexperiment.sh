# demonstrates how to call the server and the client
# modify according to your needs

ne=2000 # Number of Episodes (Default 1600)
gamma=0.9 # Discount Factor

# Tuning exploration rate
dir_name=ep_tuning
mkdir $dir_name
for algo in qlearning sarsa
do
    for((n=0;n<100;n++)) # Number of trials
    do
        for ep in $(seq 0 0.1 1) # Epsilon Values
        do
            python3 ./server/server.py -port $((4000+$n)) -i 0 -rs $n -ne $ne -q | tee $dir_name"/"$algo"_rs$n-ep"$ep".txt" &
            sleep 1
            python3 ./client/client.py -port $((4000+$n)) -rs $n -ep $ep -gamma $gamma -algo $algo
            sleep 1
        done
    done
    for ep in $(seq 0 0.1 1) # Epsilon Values
    do
        python3 results.py $dir_name"/"$algo"_rs*-ep"$ep
    done
done

# Tuning learning rate
dir_name=al_tuning
mkdir $dir_name
for algo in qlearning sarsa
do
    for((n=0;n<100;n++)) # Number of trials
    do
        for al in $(seq 0 0.1 1) # Alpha Values
        do
            python3 ./server/server.py -port $((4000+$n)) -i 0 -rs $n -ne $ne -q | tee $dir_name"/"$algo"_rs$n-al"$al".txt" &
            sleep 1
            python3 ./client/client.py -port $((4000+$n)) -rs $n -al $al -gamma $gamma -algo $algo
            sleep 1
        done
    done
    for al in $(seq 0 0.1 1) # Alpha Values
    do
        python3 results.py $dir_name"/"$algo"_rs*-al"$al
    done
done


: '
mkdir results
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