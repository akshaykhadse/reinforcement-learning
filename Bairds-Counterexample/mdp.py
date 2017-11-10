import sys
import numpy as np

expt = int(sys.argv[1])
steps = int(sys.argv[2])
lamd = float(sys.argv[3])
w = np.array(sys.argv[4:], dtype=float)
gamma = 0.99
alpha = 0.001


class MDP(object):
    """
    Class for MDP
    Initialized based on state value at start
    """
    def __init__(self, state):
        self.next_state = state

    def advance(self):
        '''
        This method returns present state and next state values
        for each advancement
        '''
        self.state = self.next_state
        if self.state < 5:
            self.next_state = 5
        else:
            rnum = np.random.randint(100)
            if rnum == 0:
                self.next_state = 6
            else:
                self.next_state = 5
        return self.state, self.next_state


step = 0
ep = 0
dv_dw = np.array([[2, 0, 0, 0, 0, 0, 1],
                  [0, 2, 0, 0, 0, 0, 1],
                  [0, 0, 2, 0, 0, 0, 1],
                  [0, 0, 0, 2, 0, 0, 1],
                  [0, 0, 0, 0, 2, 0, 1],
                  [0, 0, 0, 0, 0, 1, 2]], dtype=float)

if expt == 1:
    while ep < steps:
        mdpObject = MDP(ep % 6)
        state, next_state = mdpObject.advance()
        V = np.array([2.0 * w[0] + w[6],
                      2.0 * w[1] + w[6],
                      2.0 * w[2] + w[6],
                      2.0 * w[3] + w[6],
                      2.0 * w[4] + w[6],
                      2.0 * w[6] + w[5],
                      0.0])
        print('{:.8f} {:.8f} {:.8f} {:.8f} {:.8f} {:.8f}'.format(*V))

        delta = gamma * V[next_state] - V[state]
        w += alpha * delta * dv_dw[state]
        ep += 1
else:
    while step < steps:
        e = np.zeros_like(w)
        mdpObject = MDP(np.random.randint(5))

        while step < steps:
            state, next_state = mdpObject.advance()
            if next_state == 6:
                break
            else:
                V = np.array([2.0 * w[0] + w[6],
                              2.0 * w[1] + w[6],
                              2.0 * w[2] + w[6],
                              2.0 * w[3] + w[6],
                              2.0 * w[4] + w[6],
                              2.0 * w[6] + w[5],
                              0.0])
                print('{:.8f} {:.8f} {:.8f} {:.8f} {:.8f} {:.8f}'.format(*V))

                delta = gamma * V[next_state] - V[state]
                e = gamma * lamd * e + dv_dw[state]
                w = w + alpha * delta * e
            step += 1
        ep += 1
