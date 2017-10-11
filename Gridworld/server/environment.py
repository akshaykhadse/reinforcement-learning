import random


class Environment:
    def __init__(self, side, instance, slipperiness, randomizeNames, seed, maxLength):
        self.side = side
        self.numStates = self.side ** 2
        self.slipperiness = slipperiness
        self.randomizeNames = randomizeNames
        self.maxLength = maxLength
        self.episodeLen = 0
        random.seed(instance)

        self.start = random.randint(0, self.numStates - 2)  # Anything but the goal
        corners = [0, side-1, side*(side-1), side*side-1]
        self.goal = random.choice(corners)

        # Make some obstacles
        numObstacles = self.numStates // 10
        self.obstacles = []
        for i in range(numObstacles):
            obs = random.randint(0, self.numStates - 1)
            while obs == self.start or obs == self.goal:
                obs = random.randint(0, self.numStates - 1)
            self.obstacles.append(obs)

        random.seed(seed)
        # Make a mapping for randomizing state names
        oldnames = list(range(self.numStates))
        newnames = oldnames[:]
        random.shuffle(newnames)
        self.oldToNew = {old: new for old, new in zip(oldnames, newnames)}
        self.newToOld = {new: old for old, new in zip(oldnames, newnames)}

        # Start the environemt
        self.state = self.start

    def printWorld(self):
        for y in range(self.side):
            print('  |', end='')
            for x in range(self.side):
                state = y * self.side + x
                obs = self.obfuscate(state)
                stateType = ' '
                if state == self.state: stateType = 'A' # This is where the agent is at!
                if state == self.start: stateType = 'S' # Start state
                if state == self.goal: stateType = 'G' # Goal
                if state in self.obstacles: stateType = 'O' # Obstacle
                print('  {:03} {:03} {}  |'.format(state, obs, stateType), end='')
            print()

    def obfuscate(self, state):
        if self.randomizeNames:
            state = self.oldToNew[state]
        return state

    def deobfuscate(self, state):
        if self.randomizeNames:
            state = self.newToOld[state]
        return state

    def getnumStates(self):
        return self.numStates

    def getState(self):
        return self.obfuscate(self.state)

    def takeAction(self, action):
        '''Takes the given action in the current environment
        Returns: (new state, reward, event)'''

        self.episodeLen += 1

        # Simulate slipping
        if random.random() < self.slipperiness:
            action = random.choice('up down left right'.split())

        y, x = self.state // self.side, self.state % self.side

        x_, y_ = x, y
        if action == 'up':
            y_ -= 1
        elif action == 'down':
            y_ += 1
        elif action == 'left':
            x_ -= 1
        elif action == 'right':
            x_ += 1

        state_ = y_ * self.side + x_

        # If we fall out of boundary, or in an obstacle, undo action.
        if (x_ < 0 or x_ >= self.side or y_ < 0 or y_ >= self.side) or state_ in self.obstacles:
            state_ = self.state

        # If we reach the goal, end the episode
        if state_ == self.goal:
            self.episodeLen = 0
            self.state = self.start
            return self.obfuscate(state_), 100, 'goal'
        elif self.episodeLen == self.maxLength:
            self.episodeLen = 0
            self.state = self.start
            return self.obfuscate(state_), -1, 'terminated'
        else:
            self.state = state_
            return self.obfuscate(self.state), -1, 'continue'
