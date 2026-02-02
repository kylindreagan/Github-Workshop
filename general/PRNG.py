import time

class PRNG:
    def __init__(self, seed=None):
        if seed is None:
            seed = int(time.time() * 1000)
        self.state = seed
        self.a = 1103515245
        self.c = 12345
        self.m = 2**32

    def next_int(self, low, high):
        self.state = (self.a * self.state + self.c) % self.m
        return low + (self.state % (high - low + 1))

    def next_float(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state / self.m