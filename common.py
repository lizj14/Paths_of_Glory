import numpy as np
from enum import Enum

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

player_code = {
    'cp':1,
    'ap':-1,
    'neutral':0
}
player_name = {
    1:'cp',
    -1:'ap',
    0:'neutral'
}
cp = player_code['cp']
ap = player_code['ap']

