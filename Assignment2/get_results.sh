#!/bin/bash

rm -rf *.csv temp temp2 2> /dev/null

FILES=generated/*

# Comaparison of algorithms
for ALGORITHM in hpi rpi bspi
do
  BATCHSIZE=50
  RANDOMSEED=`date +%s%N | cut -c 11-`
  rm -rf $ALGORITHM.txt 2> /dev/null
  for MDP in $FILES
  do
    python planner.py $MDP $ALGORITHM $BATCHSIZE $RANDOMSEED gen | head -1 | cut -d " " -f1 >> $ALGORITHM.csv
  done
done


# Effect of batchsize
touch batchsize.csv
for BATCHSIZE in {1..50}
do
  for MDP in  $FILES
  do
    python planner.py $MDP bspi $BATCHSIZE 0 gen | head -1 | cut -d " " -f1 >> temp
  done
  paste -d"," batchsize.csv temp > temp2
  rm -rf temp batchsize.csv
  mv temp2 batchsize.csv
done
