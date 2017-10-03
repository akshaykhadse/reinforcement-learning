class RandomAgent:
    def __init__(self):
        self.step = 0

    def getAction(self):
        '''samples actions in a round-robin manner'''
        self.step = (self.step + 1) % 4
        return 'up down left right'.split()[self.step]

    def observe(self, newState, reward, event):
        pass


class Agent:
    def __init__(self, numStates, state, gamma, lamb, algorithm, randomseed):
        '''
        numStates: Number of states in the MDP
        state: The current state
        gamma: Discount factor
        lamb: Lambda for SARSA agent
        '''
        if algorithm == 'random':
            self.agent = RandomAgent()
        elif algorithm == 'qlearning':
            raise NotImplementedError('Q Learning needs to be implemented')
        elif algorithm == 'sarsa':
            raise NotImplementedError('SARSA lambda needs to be implemented')

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

