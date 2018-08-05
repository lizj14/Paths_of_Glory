from common import *
import cards
import units

CARD_NUM = 8

class GameParameter:
    def __init__(start_vp, get_Eight_gun):
        self.vp = start_vp
        self.turn = 0
        self._cards = dict()
        self._condition = set()
        self.initialize_cards(get_Eight_gun=get_Eight_gun, card_number=CARD_NUM)
        self._units = _initialize_units()        
        #@TODO: here needs a function of map initialize. 

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

# This class is the main logic of the game
def Game:
    def __init__(self):
        pass
        # self.game_data = GameParameter()

    def run(self):
        start_vp_change = decide_side()
        get_Eight_gun = get_Eight_Gun()
        self.game_data = GameParameter(start_vp = 10+start_vp_change, get_Eight_gun=get_Eight_gun)
        while self.game_data.turn < 20:
            self.run_turn
 

    def run_turn(self):
        pass

#@TODO: the process of side decision is not implemented here. If necessary, it is easy to add later.
def decide_side():
    print_system('input the vp decided: ')
    num = None
    while not(num is not None and isinstance(num, int) and num < 10 and num > -10):
        print_system('please input an int among (-10, 10)')
        num = input()
    return num

def get_Eight_Gun():
    print_system('the cp decide: if you want to get hte Eight Gun:')
    print_system('print y / n. Anything except n will be seemed as y')
    y_n = input()
    if y_n == 'n':
        return False
    return True 
