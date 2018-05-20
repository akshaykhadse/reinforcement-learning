# Reinforcement Learning
This repo contains implementations of basic concepts dealt under the Reinforcement Learning umbrella

### [Multi Armed Bandits](Multi-Armed-Bandits#multi-armed-bandits)

Here, you will find the implemention and comparison of different algorithms for sampling the arms of a stochastic multi-armed bandit. Each arm provides i.i.d. rewards from a fixed Bernoulli distribution. The objective is to minimise regret. The algorithms implemented are epsilon-greedy exploration, UCB, KL-UCB, and Thompson Sampling.
*[Link to implementation](https://github.com/akshaykhadse/reinforcement-learning/tree/master/Multi-Armed-Bandits)*

### [Markovian Decision Processes](Markovian-Decision-Processes#markovian-decision-processes)

Markovian decision processes find application in problems where a decision is to be made on basis of previous outcomes.

Here, algorithms for finding an optimal policy for a given MDP are implemented. The first part is to apply Linear Programming (LP) formulation and the second part is to implement three different variants of Policy Iteration (PI) viz. Howard's PI, Mansour and Singh's Randomised PI, and Batch-switching PI. Thereafter, the efficiency of these variants of PI are compared by running a set of experiments.
*[Link to implementation](https://github.com/akshaykhadse/reinforcement-learning/tree/master/Markovian-Decision-Processes)*

### [Gridworld](Gridworld#gridworld)

This repo contains implementions and comparison of Sarsa(&lambda;) and Q-learning.

The learning and exploration rates are tuned to achieve the best performance. The systematic procedure for tuning the hyperparameters is discussed in the report.

For Sarsa, the replacing-trace method as well as the accumulating-trace method is implemented.
*[Link to implementation](https://github.com/akshaykhadse/reinforcement-learning/tree/master/Gridworld)*

## Upcomming

- Baird's Counterexample
