import numpy as np


class Config:
    _version = 1.0

config = Config()

def d6():
    return np.random.randint(1,7)
