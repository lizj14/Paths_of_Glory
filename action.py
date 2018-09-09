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
        # here need to add a dict to transfer.
        self.side = player_code[side]
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
                        if order = 'operation':
                            self.run_ops(card)  
                elif order in set_order_without_card:
                    #TODO: add the action function
                elif order in set_order_info:
                    self.show_info(order)
                else:
                    print_system('the order cannot be found.')

    def run_ops(self, card):
        self.ops = card.op_points
        activation_places = []
        NE_activated = False
        while True:
            print_system('%d points left. Input the location you want to activate.' % self.ops)
            location = input()
            if location in self.data._map.hexes.keys():
                if location in activation_places:
                    print_system('%s has been activation this turn.' % location)
                    continue
                elif self.data._map.hexes[location].isNE and self.side = player_code['ap']:
                    if not NE_activated:
                        NE_activated = True
                    else:
                        print_system('ap can only activate in NE once per turn')
                        continue
                self.ops -= self.activate_location(location)
                activation_places.append(location)
            elif location == 'cancel':
                self.cancel_actions()
            else:
                print_system('cannot find %s' % location) 
      
    def cancel_actions(self):
        self.ops = 0
        for action_now in self.order_list:
            action_now.cancel()
        self.order_list = []

    # the return value is the reduction of the op points. return 0 means activation fail 
    def activate_location(self, location): 
        loc = self.data._map.hexes[location]
        all_OOS = True
        # sort(loc.units)
        # if the units are the same side
        if len(loc.units) == 0:
            print_system('there is no unit in %s' % location)
            return 0 
        elif loc.units[0].controller != self.side:
            print_system('you cannot order the units of the opposite side')
            return 0
        #@TODO: OOS. only unable to activate when all OOS
        #elif loc.units[0].OOS:
        else:
            for unit_now in loc.units:
                if not unit_now.OOS:
                    all_OOS = False
            if all_OOS:
                print_system('all the units are OOS. So sorry.')
                return 0

        sort(loc.units)
        print(loc.units)
        op_cost = self.calculate_ops(loc)
        if self.ops < op_cost:
            print_system('no enough ops. %d need' % op_cost)
            return 0

        op_mode = self.op_mode()
        return op_cost

    def op_mode(self):
        while True:
            mode = di_op_mode.get(input('move or attack?'), None)
            if mode is None:
                print('please input move or attack')
            else:
                return mode

    def calculate_ops(self, loc):
        exist_country = []
        GE11 = False
        for unit_now in loc.units:
            if self.data.has_condition('11th_Army') and unit_now.name in ['GE11', 'GE11-']:
                # in the sort, 'GE11' is always the first
                exist_country.append('GE')
                GE11 = True
            elif unit_now.opCountry in exist_country:
                pass
                #@TODO: I found that I make a mistake with the rule of Russia.
                #if self.data.parameters['Ru_status'] >= di_Russia_status['Fall_of_the_Tsar'] and unit_now.opCountry == 'RU':
                #    op_sum += 1 
                #else:
                #    pass
            elif unit_now.opCountry == 'BE' and loc.name in ['Antwerp', 'Ostend', 'Calais', 'Amiens']:
                if not 'BR' in exist_country:
                    exist_country.append('BR')
            elif unit_now.opCountry == 'US' and loc.name : #@TODO: France and German? 
                if not 'FR' in exist_country:
                    exist_country.append('FR')
            elif GE11 and not unit_now.isArmy:
                pass
            elif self.data.has_condition('Sud_Army') and \
                unit_now.opCountry == 'GE' and not unit_now.isArmy and \
                'AH' in exist_country:
                pass
            elif GE11 and not unit_now.isArmy:
                pass
            else:
                exist_country.append(unit_now.opCountry)
                
        if loc.fort != 0 and not loc.fort_country in exist_country:
            exist_country.append(loc.fort_country)
        return len(exist_country)

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
