from collections import deque
from collections import OrderedDict


class Func:
    def __init__(self, accepts, code):
        self.accepts = accepts
        self.code = code


class Cls:
    def __init__(self, env):
        self.env = env