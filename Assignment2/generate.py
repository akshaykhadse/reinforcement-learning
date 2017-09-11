import time
import os
import numpy as np


S = 50                  # Number of states
A = 2                   # Number of actions
outputFileNumber = 100  # Number of files to generate


def write_mdp(filename, S, A, R, T, gamma):

    """Function to write MDP file based on S, A, R, T and gamma"""

    mdpfile = open(filename, 'w')

    # Write S and A
    mdpfile.write(str(S) + '\n')
    mdpfile.write(str(A) + '\n')

    # Write Reward function
    for s in range(S):
        for a in range(A):
            for sPrime in range(S):
                mdpfile.write(str.format("{0:.6f}",R[s][a][sPrime]) + "\t".rstrip('\n'))

            mdpfile.write("\n")

    # Write Transition function
    for s in range(S):
        for a in range(A):
            for sPrime in range(S):
                mdpfile.write(str.format("{0:.6f}",T[s][a][sPrime]) + "\t".rstrip('\n'))

            mdpfile.write("\n")

    # Write gamma
    mdpfile.write(str.format("{0:.2f}",gamma))
    mdpfile.write("\n")

    mdpfile.close()

    return


# Make specified directory if it does not exist
if not os.path.exists('generated'):
    os.makedirs('generated')

seeds = []

# For each file to be generated
for i in range(outputFileNumber):
    # Find a unique random seed
    while 1:
        seed = np.random.randint(10000)
        if seed not in seeds:
            seeds.append(seed)
            np.random.seed(seed)
            break

    # Construct the filename
    fn = './generated/newMDP'+ str.format("{0:02d}", i) + '.txt'

    # Initialize transition and reward arrays
    T = np.zeros((S,A,S))
    R = np.zeros((S,A,S))

    # For each initial state and each action
    for s in range(S):
        for a in range(A):
            # Generate a random vector of 0s and 1s coreesponding to each sPrime
            while 1:
                k = np.sum([np.random.choice([0, 1]) for i in range(S)])
                # Making sure that there is atleat one transition exists
                if np.sum(k) != 0:
                    break

            # Find transition probabilities s.t. their sum is 1
            T[s][a][:] = k * np.random.random(S)
            T[s][a][:] = T[s][a][:] / np.sum(T[s][a][:])

            # Find rewards between -1 and 1
            R[s][a] = (k * (2 * np.random.random(S) - np.ones(S)))

    # Generate a random gamma
    g = np.random.uniform(0,1)

    # Write S, A, R, T and gamma to file
    write_mdp(fn, S, A, R, T, g)
