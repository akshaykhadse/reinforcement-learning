# Reinforcement Learning

Repository for CS747 Intelligent and Learning Agents Course

This repo contains implementations of basic concepts dealt under the Rienforcement Learning Umbrella

#### [Multi Armed Bandits](Multi-Armed-Bandits#multi-armed-bandits)

In this repo, you will find the implemention and comparison of different algorithms for sampling the arms of a stochastic multi-armed bandit. Each arm provides i.i.d. rewards from a fixed Bernoulli distribution. The objective is to minimise regret. The algorithms implemented are epsilon-greedy exploration, UCB, KL-UCB, and Thompson Sampling.

*[Link to implementation](https://github.com/akshaykhadse/ReinforcementLearning/tree/master/Multi-Armed-Bandits)*

#### [Markovian Decision Processes](Markovian-Decision-Processes#markovian-decision-processes)

Markovian decision processes find application in problems wher a decision is to be made on basis of previous outcomes.

Here, algorithms for finding an optimal policy for a given MDP are implemented. The first part is to apply Linear Programming (LP) formulation and the second part is to implement three different variants of Policy Iteration (PI) viz. Howard's PI, Mansour and Singh's Randomised PI, and Batch-switching PI. Thereafter, the efficiency of these variants of PI are compared by running a set of experiments.

*[Link to implementation](https://github.com/akshaykhadse/ReinforcementLearning/tree/master/Markovian-Decision-Processes)*

## Upcomming

- Q Learning
- Multi Agent Systems