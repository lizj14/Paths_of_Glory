from common import *

set_order = set([
    'operation',
    'strategic_redeployment',
    'replacement_points',
    'event',  
])

set_order_without_card = set([
    'peace',
    'use_1_op',
])

set_order_info = set([
    'hands',
    'location',
    'orders',
])

# This class is an action turn of one side.
class ActionTurn:
    def __init__(self, side, game_parameters):
        self.side = side
        self.data = game_parameters
        self.ops = -1
        self.order_list = []
 
    def cancel_orders(self):
        for order in self.order_list:
        #TODO: add the cancel effect
            pass
        self.order_list = []
        # this means that the operation turn has not been used
        self.ops = -1
    
    def show_hands(self):
        print(self.data._cards['%s_hand' % self.side])

    def run(self):
        while True:
            # This means that the op is used up, when ops= -1, this means the card has not been used.
            if self.ops = 0:
                return
            else:
                order = input('system >>> input the order')
                if order in set_order:
                    card = input('system >>> input the card to use')
                    if card in self.data._cards:
                        #TODO: add the action function
                elif order in set_order_without_card:
                    #TODO: add the action function
                elif order in set_order_info:
                    self.show_info(order)
                else:
                    print_system('the order cannot be found.')

    def show_info(order):
        if order == 'hands':
            print(self.data._cards['%s_hand'%self.side]
        elif order == 'location':
            loc = input('system >>> input the name of location')
            if loc in self.data._map.hexes:
                print_system(self.data._map.hexes[loc])
            else:
                print_system('no_such_location')

# The model class for op, sr, rp, for they have more than one op to use. And maybe you want to cancel the effect before final decision
class Order:
    def __init__(self):
        pass

    # execute the order. 
    def execute(self):
        pass

    # cancel the effect of the order.
    def cancel(self):
        pass
