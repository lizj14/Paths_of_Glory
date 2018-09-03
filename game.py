from common import *
import cards
import units
import maps
import action

CARD_NUM = 8

di_mandated_offensive = {
    'cp': {
    0: 'accomplish',
    1: 'AH',
    2: 'AH vs IT',
    3: 'TU',
    4: 'GE',
    5: 'no',
    6: 'no', 
},
    'ap': {
    0: 'accomplish',
    1: 'FR',
    2: 'FR',
    3: 'BR',
    4: 'IT',
    5: 'RU',
    6: 'no',
}
}

di_country_state = {
    'peace': 0,
    'at_war': 1,
    'capital_occupied': 2,
#    'surrunder': 3,
}

# need to add the situation of Rus.
di_Russia_status = {
    'Gold_Save_the_Tsar': 0,
    'Tsar_Takes_Command_Allowed': 1,
    'Fall_of_the_Tsar_Allowed': 2,
    'Fall_of_the_Tsar': 3,
    'Bolshevik_Revolution': 4,
    'Treaty_of_Brest-Litovsk': 5,
}

di_US_status = {
    'no': 0,
    'Zimmermann_Telegram_Allowed': 1,
    'Zimmermann_Telegram': 2,
    'Over_There': 3,
}

class GameParameter:
    def __init__(end_vp, get_Eight_gun):
        self.vp = 10
        self.turn = 0
        self._cards = dict()
        self._condition = set()
        self.initialize_cards(get_Eight_gun=get_Eight_gun, card_number=CARD_NUM)
        #self._units = _initialize_units()
        self._units = POG_units() 

        #@TODO: there is a conflict to resolve: units in map or outside?
        self._map = maps.test_map(self._units) 
        self.end_vp = end_vp
        self.parameters = {
            'cp_war_state': 0,
            'ap_war_state': 0,
            'cp_man_offensive': 0,
            'ap_man_offensive': 0,
            'cp_last_operation': '',
            'ap_last_operation': '',
            'Ru_status': 0,
            'US_status': 0,
        }

        #@TODO: need to check whether it is enough.
        self.country_state = {}
        for country_name in ['FR','BR','BE','GE','AH','RU','SB','MN']:
            self.country_state[country_name] = di_country_state['at_war']
        for country_name in ['TU','IT','RO','US','GR','BU']:
            self.country_state[country_name] = di_country_state['peace']

    def initialize_cards(self, get_Eight_gun, card_number):
        card_lists = card._initialize_cards(get_Eight_gun=get_Eight_gun, card_number=card_number)
        self._cards['cp_hand'] = card_lists[0]
        self._cards['ap_hand'] = card_lists[1]
        self._cards['cp_mobilization'] = card_lists[2]
        self._cards['ap_mobilization'] = card_lists[3]
        self._cards['cp_limited_war'] = card_lists[4]
        self._cards['ap_limited_war'] = card_lists[5]
        self._cards['cp_total_war'] = card_lists[6]
        self._cards['ap_total_war'] = card_lists[7]
        self._cards['cp_discard'] = card_lists[8]
        self._cards['ap_discard'] = card_lists[9]

    def win_judge(self):
        pass  

    def add_condition(self, new_condition):
        self._condition.add(new_condition)

    def has_condition(self, condition):
        return condition in self._condition

    #@property
    #def cp_war_state(self):
    #    return self.parameters['cp_war_state']

    #@property
    #def ap_war_state(self):
    #    return self.parameters['ap_war_state']

    def Zimmermann_Allowed(self):
        if self.parameters['cp_war_state'] + self.parameters['ap_war_state'] >= 30:
            self.parameters['US_status'] = di_US_status['Zimmermann_Telegram_Allowed']

    #@cp_war_state.setter
    #def cp_war_state(self, value):
    #    self.parameters['cp_war_state'] = value
    #    self.Zimmermann_Allowed()

    #@ap_war_state.setter
    #def ap_war_state(self, value):
    #    self.parameters['ap_war_state'] = value
    #    self.Zimmermann_Allowed()

# This class is the main logic of the game
def Game:
    def __init__(self):
        pass
        # self.game_data = GameParameter()

    def run(self):
        end_vp_change = decide_side()
        get_Eight_gun = get_Eight_Gun()
        self.game_data = GameParameter(end_vp = 10+end_vp_change, get_Eight_gun=get_Eight_gun)
        while self.game_data.turn < 20:
            self.run_turn()
 

    def run_turn(self):
        self.mandated_offensive_phase()
        self.action_phase()
        self.supply_phase()
        self.siege_phase()
        if self.game_data.turn != 0:
            self.war_state_phase()
        self.replacement_phase()
        self.card_phase()
        self.game_data.turn += 1

    def mandated_offensive_phase(self):
        self.mandated_offensive_side(side = 'cp')
        self.mandated_offensive_side(side = 'ap') 
    
    def mandated_offensive_side(self, side):
        number = d6()
        print_side(side=side, to_print='mandated offensive roll: %s' % di_mandated_offensive[side][number])
        self.game_data.parameters['%s_man_offensive'%side] = number

    def action_phase(self):
        for i in range(0, 6):
            self.action_side(side='cp')
            self.action_side(side='ap')
 
    def action_side(self, side):
        print_side(side=side, to_print='wait for act')
        act_turn = action.ActionTurn(side=side, game_parameter=self.game_data)
        act_turn.run()
 
    def supply_phase(self):
        to_destroy = []
        for hex_now in self.game_data._map.hexes.keys():
            if self.game_data._map.hexes[hex_now].xxx: #@TODO: here need a method to judge if in supply. Later we shall add a method in maps.py
                to_destroy.add(hex_now)
        for hex_now in to_destroy:
            #@TODO: here need to add the destroy of the units in the hex. 

    def siege_phase(self):
        hexes = self.game_data._map.hexes
        for hex_name in hexes.keys():
            hex_now = hexes[hex_name]
            if hex_now.fort != 0 and len(hex_now.units) != 0 and hex_now.controller != hex_now.units[0] #@TODO: here need a new method to define the side of the unit.
                d_result = d6() if self.game_data.turn >= 2 else d6()-2:
                if d_result > hex_now.fort:
                    self.game_data.vp += hex_now.transfer_controller()
                    print_system('%s surrunderres under siege.' % hex_name)
                else:
                    print_system('%s does not surrunder under siege.' % hex_name)

    def war_state_phase(self):
        #@TODO: check for the effect of card, for example, Blockade.
      
        self.check_for_mandated_offensive()
        
        #@TODO: need to add the check for auto win or truce.

        self.check_war_state('cp')
        self.check_war_state('ap')   

    def check_war_state(self, side):
        for stage_new, war_state_need in [['limited_war', 4], ['total_war', 11]]:
            if not self.game_data.has_condition('%s_%s' % (side, stage_new):
                if self.game_data.parameters['%s_war_state'%side] >= war_state_need:
                    self.game_data._cards['%s_mobilization'%side].add_cards(self.game_data._cards['%s_%s'% (side, stage_new)].get_all_cards())
                    self.game_data._cards['%s_mobilization'%side].add_cards(self.game_data._cards['%s_discard'].get_all_cards())
                    self.game_data._cards['%s_mobilization'%side].shuffle()
                    print_side(side=side, to_print='enters %s' % (stage_new))

    def check_for_mandated_offensive(self):
        cp_state = self.game_data.parameters['cp_man_offensive']
        if cp_state != di_mandated_offensive['cp']['accomplish'] and cp_state != di_mandated_offensive['cp']['no']:
            if cp_state == di_mandated_offensive['cp']['AH vs IT'] and self.game_data.country_state['IT'] == di_country_state['peace']:
                pass
            elif cp_state == di_mandated_offensive['cp']['TU'] and self.game_data.country_state['TU'] == di_country_state['peace']:
                pass
            else:
                self.game_data.vp -= 1
        ap_state = self.game_data.parameters['ap_man_offensive']
        if ap_state != di_mandated_offensive['ap']['accomplish']:
            if ap_state == di_mandated_offensive['ap']['IT'] and self.game_data.country_state['IT'] == di_country_state['peace']:
                pass
            #@TODO: need to check after make the card
            elif ap_state == di_mandated_offensive['ap']['FR'] and self.game_data.has_condition('FR_bingbian'):
                pass
            else:
                self.game_data.vp += 1


    def replacement_phase(self):
        pass
           
    def card_phase(self):
        self.card_reinforce_side(side='cp')
        self.card_reinforce_side(side='ap')

    def card_reinforce_side(self,side):
        print(self.game_data._cards['%s_hand'%side])
        #@TODO: I have forgotten whether remove can be used in list like this. Need verification. has revised, need to debug
        to_discard = []
        for card in self.game_data._cards['%s_hand'%side]:
            if card.cc:
                print_system('discard %s? print yes to discard, other not to' % card.name)
                ok = input()
                if ok == 'yes':
                    to_discard.append(card)
                    #self.game_data._cards.remove_card(card_no=card.no)
        for card in to_discard:
            self.game_data._cards.remove_card(card_no=card.no)

        number_now = self.game_data._cards['%s_hand'%side].card_number()
        card_remain = self.game_data._cards['%s_mobilization'%side].card_number()
        if number_now + card_remain <= CARD_NUM:
            self.game_data._cards['%s_hand'%side].add_cards(self.game_data._cards['%s_mobilization'%side].get_all_cards())
            cards.merge_cards(self.game_data._cards['%s_mobilization'%side], self.game_data._cards['%s_discard'%side])
        else:
            self.game_data._cards['%s_hand'%side].add_cards(self.game_data._cards['%s_mobilization'%side].get_cards(number=CARD_NUM-number_now)
 
#@TODO: the process of side decision is not implemented here. If necessary, it is easy to add later.
def decide_side():
    print_system('input the vp decided: ')
    num = None
    while not(num is not None and isinstance(num, int) and num < 10 and num > -10):
        print_system('please input an int among (-10, 10)')
        num = input()
    return num

def get_Eight_Gun():
    print_system('the cp decide: if you want to get the Eight Gun:')
    print_system('print y / n. Anything except n will be seemed as y')
    y_n = input()
    if y_n == 'n':
        return False
    return True

if __name__ == '__main__':
    game = Game()
    game.run()
