import sys
from math import *
from parse import func
from lex import SpecialNum
from data import *
from copy import deepcopy

class expck:
    def __init__(self):
        self.subs = {
            '+': self.add,
            '-': self.sub,
            '*': self.mul,
            '/': self.div,
            '%': self.mod,
            '**': self.exp,
            '&': self._and,
            '|': self._or,
            '^': self.xor,
            '~': self.bwnot,
            '!': self._not,
            '=': self.eq,
            '!=': self.neq,
            '?': self.neq,
            '>': self.gt,
            '<': self.lt,
            '>=': self.gte,
            '?': self.gte,
            '=<': self.lte,
            '?': self.lte,
            'class': self.cls,
        }

    def err(self, error):
        print(error)
        sys.exit()

    def evalall(self, things, env=None):
        if env is None:
            env = {}

        ret = []

        for thing in things:
            out = self.evalml(thing, env)
            ret.append(out[0])
            env = out[1]

        return ret, env

    def evalml(self, script, env=None):
        if env is None:
            env = {}

        ret = None

        if type(script) == list:
            com = script[0]
            if type(com) == func:
                com = com.name

            else:
                self.err('SyntaxError: %s is not a function' % repr(com))
                sys.exit()

            if len(script) > 1:
                args = script[1:]

            else:
                args = []

            if com.isidentifier() and com.lower() in dir(self):
                try:
                    ret, env = getattr(self, com.lower())(env, *args)
                except AttributeError:
                    if com in env:
                        return self.evalml(env[com], env)
                    self.err('CommandError: %s is not a command' % repr(com))
                    sys.exit()

            elif com.lower() in self.subs:
                ret, env = self.subs[com.lower()](env, *args)

            elif com.lower() in env:
                f = env[com.lower()]
                if type(f) == Func:
                    fe = deepcopy(env)
                    fe.update({x: y for (x, y) in zip(f.accepts, self.evalall(args, env)[0])})
                    return self.evalml(f.code, fe)[0], env
                else:
                    return f, env

            return ret, env

        elif type(script) == SpecialNum:
            ret = None
            if script.const == 'i':
                ret = complex(0, script.val)
            else:
                self.err()
            return ret, env
        else:
            return script, env

    def s(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        if len(args) > 0:
            if len(args) < 2:
                if type(args[0]) == int:
                    return args[0]+1, env

                else:
                    self.err('ValueError: Non-integer value %i used in successor' % args[0])

            else:
                self.err('ValueError: Too many values given to successor function')

        else:
            return 0, env

    def p(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        if len(args) > 0:
            if len(args) < 2:
                if type(args[0]) == int:
                    return args[0]-1, env

                else:
                    self.err('ValueError: Non-integer value %i used in successor' % args[0])

            else:
                self.err('ValueError: Too many values given to successor function')

        else:
            return 0, env

    def add(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        if len(args) > 0:
            out = args[0]

            if len(args) > 1:
                if all([type(a) in [int, float, complex] for a in args]):
                    tail = args[1:]

                    for i in tail:
                        out += i

                else:
                    self.err('ValueError: Non-numerical value used in + operation')

            return out, env

        else:
            return 0, env

    def sub(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        if len(args) > 0:
            out = args[0]

            if len(args) > 1:
                if all([type(a) in [int, float, complex] for a in args]):
                    tail = args[1:]

                    for i in tail:
                        out -= i

                else:
                    self.err('ValueError: Non-numerical value used in - operation')

            return out, env

        else:
            return 0, env

    def mul(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        if len(args) > 0:
            out = args[0]

            if len(args) > 1:
                if all([type(a) in [int, float, complex] for a in args]):
                    tail = args[1:]

                    for i in tail:
                        out *= i

                else:
                    self.err('ValueError: Non-numerical value used in * operation')

            return out, env

        else:
            return 1, env

    def div(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        if len(args) > 0:
            out = args[0]

            if len(args) > 1:
                if all([type(a) in [int, float, complex] for a in args]):
                    tail = args[1:]

                    for i in tail:
                        out /= i

                else:
                    self.err('ValueError: Non-numerical value used in / operation')

            return out, env

        else:
            return 1, env

    def mod(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        if len(args) > 0:
            out = args[0]

            if len(args) > 1:
                if all([type(a) in [int, float] for a in args]):
                    tail = args[1:]

                    for i in tail:
                        out %= i

                else:
                    self.err('ValueError: Non-numerical value used in % operation')

            return out, env

        else:
            return 1, env

    def exp(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        if len(args) > 0:
            out = args[0]

            if len(args) > 1:
                if all([type(a) in [int, float, complex] for a in args]):
                    tail = args[1:]

                    for i in tail:
                        out **= i

                else:
                    self.err('ValueError: Non-numerical value used in ** operation')

            return out, env

        else:
            return 1, env

    def _and(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        if len(args) > 0:
            out = args[0]

            if len(args) > 1:
                if all([type(a) in [int, bool] for a in args]):
                    tail = args[1:]

                    for i in tail:
                        out &= i

                else:
                    self.err('ValueError: Non-bitwise value used in & operation')
            return out, env

        else:
            return -1, env

    def _or(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        if len(args) > 0:
            out = args[0]

            if len(args) > 1:
                if all([type(a) in [int, bool] for a in args]):
                    tail = args[1:]

                    for i in tail:
                        out |= i

                else:
                    self.err('ValueError: Non-bitwise value used in | operation')

            return out, env

        else:
            return 0, env

    def xor(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        if len(args) > 0:
            out = args[0]

            if len(args) > 1:
                if all([type(a) in [int, bool] for a in args]):
                    tail = args[1:]

                    for i in tail:
                        out ^= i

                else:
                    self.err('ValueError: Non-bitwise value used in ^ operation')

            return out, env

        else:
            return 0, env

    def bwnot(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        if len(args) > 0:
            if len(args) < 2:
                return ~args[0], env

            else:
                self.err('ValueError: Too many values given to ~ function')

        else:
            return 1, env

    def _not(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        if len(args) > 0:
            if len(args) < 2:
                return not args[0], env

            else:
                self.err('ValueError: Too many values given to ~ function')

        else:
            return 1, env

    def eq(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        return all([a == args[0] for a in args[1:]]), env

    def neq(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        return len(set(args)) == len(args), env

    def gt(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        return all(x < y for (x, y) in zip(args, args[1:])), env

    def lt(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        return all(x > y for (x, y) in zip(args, args[1:])), env

    def gte(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        return all(x <= y for (x, y) in zip(args, args[1:])), env

    def lte(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        return all(x >= y for (x, y) in zip(args, args[1:])), env

    def print(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        print(''.join(args), end='')
        return None, env

    def input(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        return input(), env

    def c(self, env, *args):
        return self.evalall(args, env)

    def t(self, env, *args):
        eved = self.evalall(args, env)
        return tuple(eved[0]), eved[1]

    def assgn(self, env, *args):
        args = self.evalall(args, env)
        env = args[1]
        args = args[0]

        env[args[0].lower()] = args[1]

        return args[1], env

    def func(self, env, *args):
        accepts = [x.name for x in args[0]]
        returns = args[1]
        return Func(accepts, returns), env

    def cls(self, env, *args):
        pass