import numpy as np


class RandomAgent:
    def __init__(self):
        self.step = 0

    def getAction(self):
        '''samples actions in a round-robin manner'''
        self.step = (self.step + 1) % 4
        return 'up down left right'.split()[self.step]

    def observe(self, newState, reward, event):
        pass


class SarsaAgent:
    def __init__(self, numStates, state, gamma, lamb, trace, alpha, epsilon):
        self.numStates = numStates
        self.actions = 'up down left right'.split()
        self.numActions = len(self.actions)
        self.state = state
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.lamb = lamb
        self.trace = trace
        self.Q = np.zeros((self.numStates, self.numActions))
        self.e = np.zeros((self.numStates, self.numActions))
        self.ecr = 0.0
        self.action = 0
        self.step = 0

    def getAction(self):
        '''samples actions according to SARSA'''
        self.step = (self.step + 1)
        return self.actions[self.action]

    def observe(self, newState, reward, event):
        self.ecr += self.gamma * reward
        if event == 'continue':
            # if np.random.uniform(low=0.0, high=1.0) < self.epsilon/self.step: # Annealing
            if np.random.uniform(low=0.0, high=1.0) < self.epsilon:
                newAction = np.random.randint(low=0, high=4)
            else:
                newAction = np.argmax(self.Q[newState])
            delta = reward + self.gamma * self.Q[newState, newAction] - self.Q[self.state, self.action]
            if self.trace == 'accum':
                self.e[self.state, self.action] = self.e[self.state, self.action] + 1.0
            elif self.trace == 'replace':
                self.e[self.state, self.action] = 1.0
            '''
            for s in range(self.numStates):
                for a in range(self.numActions):
                    self.Q[s, a] = self.Q[s, a] + self.alpha * delta * self.e[s, a]
                    self.e[s, a] = self.gamma * self.lamb * self.e[s, a]
            '''
            # Matrix multiplication form of above nested for loop
            self.Q = self.Q + self.alpha * delta * self.e
            self.e = self.gamma * self.lamb * self.e
            self.state = newState
            self.action = newAction
        elif event == 'terminated':
            # print(str(self.ecr) + '\tterminated')
            self.state = newState
            self.e = np.zeros((self.numStates, self.numActions))
            self.ecr = 0.0
            self.action = 0
            self.step = 0
        elif event == 'goal':
            # print(str(self.ecr) + '\tGoal Reached')
            self.state = newState
            self.e = np.zeros((self.numStates, self.numActions))
            self.ecr = 0.0
            self.action = 0
            self.step = 0



class QAgent:
    def __init__(self, numStates, state, gamma, alpha, epsilon):
        self.numStates = numStates
        self.actions = 'up down left right'.split()
        self.numActions = len(self.actions)
        self.state = state
        self.epsilon = epsilon
        self.gamma = gamma
        self.alpha = alpha
        self.Q = np.zeros((self.numStates, self.numActions))
        self.ecr = 0.0
        self.action = 0
        self.step = 0

    def getAction(self):
        '''samples actions according to SARSA'''
        self.step = (self.step + 1)
        # if np.random.uniform(low=0.0, high=1.0) < self.epsilon/self.step: # Annealing
        if np.random.uniform(low=0.0, high=1.0) < self.epsilon:
            self.action = np.random.randint(low=0, high=4)
        else:
            self.action = np.argmax(self.Q[self.state])
        return self.actions[self.action]

    def observe(self, newState, reward, event):
        self.ecr += self.gamma * reward
        if event == 'continue':
            delta = reward + self.gamma * np.amax(self.Q[newState]) - self.Q[self.state, self.action]
            self.Q[self.state, self.action] = self.Q[self.state, self.action] + self.alpha * delta
            self.state = newState
        elif event == 'terminated':
            # print(str(self.ecr) + '\tterminated')
            self.state = newState
            self.ecr = 0.0
            self.action = 0
            self.step = 0
        elif event == 'goal':
            # print(str(self.ecr) + '\tGoal Reached')
            self.state = newState
            self.ecr = 0.0
            self.action = 0
            self.step = 0


class Agent:
    def __init__(self, numStates, state, gamma, lamb, algorithm, randomseed, trace, alpha, epsilon):
        '''
        numStates: Number of states in the MDP
        state: The current state
        gamma: Discount factor
        lamb: Lambda for SARSA agent
        '''
        np.random.seed(randomseed)
        if algorithm == 'random':
            self.agent = RandomAgent()
        elif algorithm == 'qlearning':
            self.agent = QAgent(numStates, state, gamma, alpha, epsilon)
        elif algorithm == 'sarsa':
            self.agent = SarsaAgent(numStates, state, gamma, lamb, trace, alpha, epsilon)

    def getAction(self):
        '''returns the action to perform'''
        return self.agent.getAction()

    def observe(self, newState, reward, event):
        '''
        event:
            'continue'   -> The episode continues
            'terminated' -> The episode was terminated prematurely
            'goal'       -> The agent successfully reached the goal state
        '''
        self.agent.observe(newState, reward, event)
