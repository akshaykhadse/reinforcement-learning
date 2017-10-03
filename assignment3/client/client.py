#!/usr/bin/python3

from collections import namedtuple
import argparse
import socket
import sys
from agent import Agent

parser = argparse.ArgumentParser(description="Implements the Learning Agent.")
parser.add_argument('-ip', '--ip', dest='ip', type=str, default='localhost', help='IP of server')
parser.add_argument('-port', '--port', dest='port', type=int, default=5000, help='Port for connection')
parser.add_argument('-algo', '--algorithm', dest='algorithm', type=str, default='sarsa', help='The learning algorithm to be used. {random, sarsa, qlearning, model}')
parser.add_argument('-gamma', '--gamma', dest='gamma', type=float, default=1, help='Discount Factor')
parser.add_argument('-lambda', '--lambda', dest='lamb', type=float, default=0, help='Value of lambda')
parser.add_argument('-trace', '--trace', dest='trace', type=str, default='accum', help='Value of trace {accum, replace}')
parser.add_argument('-rs', '--randomseed', dest='randomseed', type=int, default=0, help='Seed for RNG.')
args = parser.parse_args()


def getResponse(message):
    global sock
    sock.sendall(message.encode())
    data = ''
    while True:
        data += sock.recv(1024).decode()
        if data[-1] == '\n':
            break
    if 'TERMINATE' in data:
        sys.exit()
    return data[:-1]


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
Address = namedtuple('Address', ['ip', 'port'])

server_address = Address(ip=args.ip, port=args.port)
print('Connecting to:', server_address, file=sys.stderr)
sock.connect(server_address)

try:
    print('Requesting environment info')
    numStates, state = map(int, getResponse('info').strip().split())
    print('Number of States: {}, Current State: {}\n=========='.format(numStates, state))

    agent = Agent(numStates, state, args.gamma, args.lamb, args.algorithm.lower(), args.randomseed)

    while True:
        action = agent.getAction() # Take action
        state, reward, event = map(int, getResponse(action).strip().split())
        event = 'continue terminated goal'.split()[event]
        agent.observe(state, reward, event) # Observe Reward
finally:
    print('Closing Socket')
    sock.close()