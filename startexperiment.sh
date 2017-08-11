#!/bin/bash

PWD=`pwd`

horizon=500
port=5001
nRuns=2000;
hostname="localhost"
banditFile="$PWD/data/instance-5.txt"

algorithm="Thompson-Sampling"
# Allowed values for algorithm parameter(case-sensitive)
# 1. epsilon-greedy
# 2. UCB
# 3. KL-UCB
# 4. Thompson-Sampling
# 5. rr

epsilon=0.2

numArms=$(wc -l $banditFile | cut -d" " -f1 | xargs)

SERVERDIR=./server
CLIENTDIR=./client

OUTPUTFILE=$PWD/serverlog.txt

for i in  $(seq 1 $nRuns)
do
   echo $i
   randomSeed=`date +"%s"`

   pushd $SERVERDIR
   cmd="./startserver.sh $numArms $horizon $port $banditFile $randomSeed $OUTPUTFILE &"
   #echo $cmd
   $cmd
   popd

   sleep 1

   pushd $CLIENTDIR
   cmd="./startclient.sh $numArms $horizon $hostname $port $randomSeed $algorithm $epsilon"
   #echo $cmd
   $cmd > ../temp1
   if [ "$i" -eq "1" ]
   then
      cat ../temp1 > ../output.csv
   else
      cat ../temp1 | paste -d',' ../output.csv - > ../temp
      cat ../temp > ../output.csv
   fi
   popd

   sleep 1
done

rm -rf temp temp1


####

#for i in  $(seq 1 $nRuns)
#do
   #echo $i
#   randomSeed=`date +"%s"`

#   pushd $SERVERDIR
#   cmd="./startserver.sh $numArms $horizon $port $banditFile $randomSeed $OUTPUTFILE &"
   #echo $cmd
#   $cmd
#   popd

#   sleep 1

#   pushd $CLIENTDIR
#   cmd="./startclient.sh $numArms $horizon $hostname $port $randomSeed $algorithm $epsilon"
   #echo $cmd
#   $cmd
#   popd

#   sleep 1
#done
