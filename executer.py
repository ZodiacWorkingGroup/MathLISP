from data import *
from execpack import expck
from parse import *


if __name__ == '__main__':
    i = 0
    ep = expck()

    env = {}

    while True:
        inp = input('In ['+str(i)+']> ')

        if inp[0] != ':':
            eved, env = ep.evalml(parser.parse(inp)[0], env)
            print(eved)

        else:
            com = inp[1:].split(' ')[0].upper()
            if com == 'EXIT':
                break
            elif com == 'ENV':
                print(env)


        i += 1
