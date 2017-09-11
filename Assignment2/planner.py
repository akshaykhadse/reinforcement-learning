import numpy as np
from pulp import *
import sys

# Get command line arguments
mdp = sys.argv[1]               # MDP File
algorithm = sys.argv[2]         # Algorithm
batchsize = int(sys.argv[3])    # Batchsize
randomseed = int(sys.argv[4])   # Randomseed
# Check if invoked from get_results
if len(sys.argv) == 6:
    mode = sys.argv[5]
else:
    mode = "na"

# Set the randomseed to specified value, only matters for RPI
np.random.seed(randomseed)


def read_mdp(mdp):

    """Function to read MDP file"""

    f = open(mdp)

    S = int(f.readline())
    A = int(f.readline())

    # Initialize Transition and Reward arrays
    R = np.zeros((S, A, S))
    T = np.zeros((S, A, S))

    # Update the Reward Function
    for s in range(S):
        for a in range(A):
            line = f.readline().split()
            for sPrime in range(S):
                R[s][a][sPrime] = line[sPrime]

    # Update the Transition Function
    for s in range(S):
        for a in range(A):
            line = f.readline().split()
            for sPrime in range(S):
                T[s][a][sPrime] = line[sPrime]

    # Read the value of gamma
    gamma = float(f.readline().rstrip())

    f.close()

    return S, A, R, T, gamma


def print_mdp(S, A, R, T, gamma):

    """Function to print the data read from MDP file"""

    print "States: " + str(S)
    print "Actions: " + str(A)

    print "Reward Function:"
    for s in range(S):
        for a in range(A):
            for sPrime in range(S):
                print str(R[s][a][sPrime]) + "\t",

            print "\n",

    print "Transition Function:"
    for s in range(S):
        for a in range(A):
            for sPrime in range(S):
                print str(T[s][a][sPrime]) + "\t",

            print "\n",

    print "Gamma: " + str(gamma)

    return


def find_v(T, R, gamma, policy):

    """Function to find value function V"""

    # Initialize arrays of zeros for Value function after and before update
    V1 = np.zeros(T.shape[0])
    V0 = np.zeros(T.shape[0])

    while(1):
    # Until the V1 and V0 are close enough element wise
        for s in range(T.shape[0]):
            # Find the V1
            V1[s] = np.sum(T[s, policy[s], :] * R[s, policy[s], :] + gamma * T[s, policy[s], :] * V0)
        # If V1 and V0 are close enough
        if np.allclose(V1, V0, rtol=1e-13, atol=1e-15):
            break
        else:
            # Update V0 with V1
            np.copyto(V0, V1)
    return V1


def find_q(V, T, R, gamma):

    """Function to find action value function Q"""

    # Initialize arrays of zeros for Value function after and before update
    Q = np.zeros((T.shape[0], T.shape[1]))

    for s in range(T.shape[0]):
        # Find action value for each state action pair
        Q[s] = np.sum(T[s] * R[s] + gamma * T[s] * V, axis=1)

    return Q


def hpi(T, R, gamma):

    """Implementation of Howard's PI"""

    # Initialise policy to all zeros
    policy = [0 for i in range(T.shape[0])]

    # Set the flag
    changed = 1

    iterations = 0
    while changed == 1:
        # While flag is set
        iterations += 1

        # Find V and Q
        V = find_v(T, R, gamma, policy)
        Q = find_q(V, T, R, gamma)

        # Find improvable states
        improvable_states = []
        for s in range(T.shape[0]):
            # Check for improvablity and add to improvable states
            if (Q[s][policy[s]] < np.amax(Q[s][:])):
                improvable_states.append(s)

        # If there are improvable states, switch the action for each improvable state
        if len(improvable_states) > 0:
                for k in improvable_states:
                    policy[k] = 1 - policy[k]
        else:
            # If no improvable states, reset the flag
            changed = 0

    # Print iterations if invoked from get_results.sh
    if mode == "gen":
        print iterations, policy

    return V, policy


def rpi(T, R, gamma):

    """Implementation of Randomised PI"""

    # Initialise policy to all zeros
    policy = [0 for i in range(T.shape[0])]

    # Set the flag
    changed = 1

    iterations = 0
    while changed == 1:
        # While flag is set
        iterations += 1

        # Find V and Q
        V = find_v(T, R, gamma, policy)
        Q = find_q(V, T, R, gamma)

        # Find improvable states
        improvable_states = []
        for s in range(T.shape[0]):
            # Check for improvablity and add to improvable states
            if Q[s][policy[s]] < np.amax(Q[s][:]):
                improvable_states.append(s)

        if len(improvable_states) > 0:
            # From the set of improving states, pick random subset and switch its states
            # Subset should be non empty and its elements must to be repeated
            for i in range(np.random.choice(range(len(improvable_states)))+1):
                j = np.random.choice(improvable_states)
                policy[j] = 1 - policy[j]
                improvable_states.remove(j)
        else:
            # If no improvable states, reset the flag
            changed = 0

    # Print iterations if invoked from get_results.sh
    if mode == "gen":
        print iterations, policy

    return V, policy


def bspi(T, R, gamma, batch_size):

    """Implementation of Howard's PI"""

    # Initialise policy to all zeros
    policy = [0 for i in range(T.shape[0])]
    iterations = 0

    # Partition the states into batches; and improve rightmost batch first
    # then the one on left to it and so on
    for i in reversed(range(0, T.shape[0], batch_size)):

        if i+batch_size-1 < T.shape[0]:
            batch = range(i, i+batch_size)
        else:
            batch = range(i, T.shape[0])

        # Set the flag
        changed = 1
        while changed == 1:
            # While flag is set
            iterations += 1

            # Find V and Q
            V = find_v(T, R, gamma, policy)
            Q = find_q(V, T, R, gamma)

            # Find improvable states
            improvable_states = []
            for s in batch:
                # Check for improvablity and add to improvable states
                if (Q[s][policy[s]] < np.amax(Q[s][:])):
                    improvable_states.append(s)

            # If there are improvable states, switch the action for each improvable state
            if len(improvable_states) > 0:
                    for k in improvable_states:  # For each improvable state
                        policy[k] = 1 - policy[k] # Switch the action
            else:
                # If no improvable states, reset the flag
                changed = 0

    # Print iterations if invoked from get_results.sh
    if mode == "gen":
        print iterations, policy

    # Find final Vstar
    V = find_v(T, R, gamma, policy)

    return V, policy


def solve_lp(T, R, gamma):

    """Function to solve Linear Programming using PuLP"""

    # Setting up problem and decision variables
    prob = pulp.LpProblem('mdp_lp', pulp.LpMinimize)
    decision_variables = pulp.LpVariable.dicts('v', range(T.shape[0]))

    # Objective function
    prob += np.sum(decision_variables.values())

    for s in range(T.shape[0]):
        for a in range(T.shape[1]):
            # Add constraint to LP for each state and action
            formula = 0.0
            for sPrime in range(T.shape[2]):
                formula += T[s, a, sPrime] * (R[s, a, sPrime] + gamma * decision_variables[sPrime])
            prob += decision_variables[s] >= formula

    # Solve the LP Problem and get results in V
    prob.solve()  # solvers.PULP_CBC_CMD(fracGap=0.000000001)
    V = np.array([v.varValue for v in prob.variables()])

    return V


def lp(T, R, gamma):

    """Implementation of LP"""

    # Initialise policy to all zeros
    policy = [0 for i in range(T.shape[0])]

    # Find V and Q
    V = solve_lp(T, R, gamma)
    Q = find_q(V, T, R, gamma)

    # For each state, if action_0 value is less than action_1 value,
    # change its action to action_1
    for s in range(T.shape[0]):
        if (Q[s][0] < Q[s][1]) and (policy[s] != 1):
            policy[s] = 1

    return V, policy


def print_output(V, pi):

    """Function to print results of any PI Method"""

    for i in range(V.shape[0]):
        print str.format("{0:.15f}", V[i]) + "\t" + str(pi[i])

    return


# Read the MDP file
S1, A1, R1, T1, gamma1 = read_mdp(mdp)

# Invoke appropriate Algorithm according to Command Line Parameter
if algorithm == "hpi":
    V_star, pi_star = hpi(T1, R1, gamma1)
elif algorithm == "rpi":
    V_star, pi_star = rpi(T1, R1, gamma1)
elif algorithm == "bspi":
    V_star, pi_star = bspi(T1, R1, gamma1, batchsize)
elif algorithm == "lp":
    V_star, pi_star = lp(T1, R1, gamma1)

# Print the results to STDOUT
print_output(V_star, pi_star)
