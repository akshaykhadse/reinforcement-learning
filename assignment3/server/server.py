#!/usr/bin/python3

from collections import namedtuple
import argparse
import socket
import sys
from environment import Environment


def str2bool(v):
    # https://stackoverflow.com/a/43357954/2570622
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
parser = argparse.ArgumentParser(description="Implements the Environment.")
parser.add_argument('-ip', '--ip', dest='ip', type=str, default='localhost', help='IP of server')
parser.add_argument('-port', '--port', dest='port', type=int, default=5000, help='Port for connection')
parser.add_argument('-side', '--side', dest='side', type=int, default=32, help='Side length of the square grid')
parser.add_argument('-i', '--instance', dest='instance', type=int, default=0, help='Instance number of the gridworld.')
parser.add_argument('-slip', '--slip', dest='slip', type=float, default=0.02, help='How likely is it for the agent to slip')
parser.add_argument('-ml', '--maxlength', dest='maxLength', type=int, default=1000, help='Maximum number of timesteps in an episode')
parser.add_argument('-rs', '--randomseed', dest='randomseed', type=int, default=0, help='Seed for RNG.')
parser.add_argument('-nobf', '--noobfuscate', dest='obfuscate', type=str2bool, nargs='?', const=False, default=True, help='Whether to obfuscate the states or not')
parser.add_argument('-ne', '--numepisodes', dest='numEpisodes', type=int, default=1600, help='Number of episodes to run')
parser.add_argument('-q', '--quiet', dest='quiet', type=str2bool, nargs='?', const=True, default=False, help='Surpresses detailed output. (Will make the code run a little faster)')
args = parser.parse_args()
print(args, file=sys.stderr)
verbose = not args.quiet


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
Address = namedtuple('Address', ['ip', 'port'])
server_address = Address(ip=args.ip, port=args.port)
print('Server started.', server_address, file=sys.stderr)
sock.bind(server_address)
sock.listen(1)


env = Environment(args.side, args.instance, args.slip, args.obfuscate, args.randomseed, args.maxLength)


print('Waiting for client', file=sys.stderr)
connection, client_address = sock.accept()
try:
    client_address = Address(*client_address)
    print('Connected.', client_address, file=sys.stderr)

    episodeNum = 0
    totReward = 0
    episodeRewards = []
    if not verbose: print('Progress: ', end='', file=sys.stderr)
    while episodeNum < args.numEpisodes:
        action = connection.recv(1024).decode('utf-8')
        if verbose: print('----------\nRecieved:', action, file=sys.stderr)

        if action == 'info':
            numStates = env.getnumStates()
            state = env.getState()
            print('Number of states: {}, Current State: {}'.format(numStates, state), file=sys.stderr)
            if verbose: env.printWorld()
            connection.sendall('{} {}\n'.format(numStates, state).encode('utf-8'))

        elif action in 'up down left right'.split():
            if verbose: print('Taking action', action, file=sys.stderr)
            state, reward, event = env.takeAction(action)
            if verbose: print('New state: {}, Reward: {}, event: {}'.format(state,reward, event), file=sys.stderr)

            totReward += reward
            if event in ['goal', 'terminated']:
                episodeNum += 1
                if not verbose and episodeNum % (args.numEpisodes//50) == 0:
                    print('#', end='', flush=True, file=sys.stderr)
                episodeRewards.append(totReward)
                totReward = 0

            event = ['continue', 'terminated', 'goal'].index(event)
            connection.sendall('{} {} {}\n'.format(state, reward, event).encode('utf-8'))

        else:
            print('\n\nInvalid action! Terminating', file=sys.stderr)
            break
    connection.sendall('TERMINATE\n'.encode('utf-8'))

    print('Reward for each episode:')
    print(episodeRewards)
    print('Completed {} episodes.'.format(episodeNum))

finally:
    connection.close()
