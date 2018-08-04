import numpy as np


class Config:
    _version = 1.0

config = Config()

def d6():
    return np.random.randint(1,7)

def print_system(to_print):
    print('system >>> %s' % to_print)

def print_side(side, to_print):
    print('%s -> %s' % (side, to_print))

def cp_action(to_print):
    print_side(side = 'cp', to_print = to_print)

def ap_action(to_print):
    print_side(side = 'ap', to_print = to_print)
