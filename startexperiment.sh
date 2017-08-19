#!/bin/bash
#echo "Started"

PWD=`pwd`

#horizon=500
port=5001
nRuns=200
hostname="localhost"
#banditFile="$PWD/data/instance-5.txt"

#echo "Reached Algo Selection"
#algorithm="Thompson-Sampling"
# Allowed values for algorithm parameter(case-sensitive)
# 1. epsilon-greedy
# 2. UCB
# 3. KL-UCB
# 4. Thompson-Sampling
# 5. rr

epsilon=0.2

#echo "Reached numArm Calculation"
#numArms=$(wc -l $banditFile | cut -d" " -f1 | xargs)

#echo "Filenames"
SERVERDIR=./server
CLIENTDIR=./client

OUTPUTFILE=$PWD/serverlog.txt

#rewardFile=$PWD/$algorithm-$epsilon-$horizon-$nRuns-instance$numArms.csv
#resultFile=$PWD/result-$algorithm-$epsilon-$horizon-$nRuns-instance$numArms.csv

#echo "Entering Bandit File Loop"
for banditFile in $PWD/data/instance*
do
   numArms=$(wc -l $banditFile | cut -d" " -f1 | xargs)
   finalResultFile=$PWD/final$numArms.csv
   echo "algorithm,epsilon,horizon,nRuns,numArms,regret" > $finalResultFile
   for algorithm in epsilon-greedy UCB KL-UCB Thompson-Sampling rr
   do
      for i in $(seq 1 5)
      do
         horizon=$(echo "10^$i" | bc)
         rewardFile=$PWD/$algorithm-$epsilon-$horizon-$nRuns-instance$numArms.csv
         resultFile=$PWD/result-$algorithm-$epsilon-$horizon-$nRuns-instance$numArms.csv
         for i in  $(seq 1 $nRuns)
         do
            echo $i
            randomSeed=`date +"%s"`

            pushd $SERVERDIR
            cmd="./startserver.sh $numArms $horizon $port $banditFile $randomSeed $OUTPUTFILE &"
            $cmd
            popd

            sleep 1

            pushd $CLIENTDIR
            cmd="./startclient.sh $numArms $horizon $hostname $port $randomSeed $algorithm $epsilon"
            $cmd > ../temp1.txt
            regret=$(cat ../serverlog.txt | grep Regret | cut -c 10-)
            echo $regret >> ../temp1.txt
           
            if [ "$i" -eq "1" ]
            then
               cat ../temp1.txt > $rewardFile #../output.csv
            else
               cat ../temp1.txt | paste -d',' $rewardFile - > ../temp2.txt
               cat ../temp2.txt > $rewardFile #../output.csv
            fi
            popd

            sleep 1
         done

         if [ -e "$resultFile" ]
         then
            rm -rf $resultFile
         fi

         cmd="python process.py $horizon $rewardFile $resultFile"
         $cmd
 
         rm -rf temp1.txt temp2.txt $rewardFile
         
         echo $algorithm,$epsilon,$horizon,$nRuns,$numArms,`tail -1 $resultFile` >> $finalResultFile       
      done
   done
done
echo "All Done" > finished.txt
