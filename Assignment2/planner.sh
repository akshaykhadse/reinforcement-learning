#!/bin/bash

# Read the long options
TEMP=`getopt -o m:a:b:r: --long mdp:,algorithm:,batchsize:,randomseed: -n 'planner.sh' -- "$@"`
eval set -- "$TEMP"

# Set default randomseed and batchsize
RANDOMSEED=0
BATCHSIZE=1

# Extract options and their arguments into variables
while true ; do
    case "$1" in
        -m | --mdp ) MDP="$2" ; shift 2 ;;
        -a | --algorithm ) ALGORITHM="$2" ; shift 2 ;;
        -b | --batchsize ) BATCHSIZE="$2" ; shift 2 ;;
        -r | --randomseed ) RANDOMSEED="$2" ; shift 2 ;;
        -- ) shift ; break ;;
        * ) echo "Internal error!" ; exit 1 ;;
    esac
done

#echo "mdp = $MDP"
#echo "algorithm = $ALGORITHM"
#echo "batchsize = $BATCHSIZE"
#echo "randomseed = $RANDOMSEED"

python planner.py $MDP $ALGORITHM $BATCHSIZE $RANDOMSEED
