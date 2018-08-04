from common import *
import random

di_sr_point_function = {
    2: 2,
    3: 4,
    4: 4,
    5: 5,
}

di_time = {
    0: 'mobilization',
    1: 'limited war',
    2: 'total war',
}

class Card:
    def __init__(no, name, fraction, time, points, remove, cc, war_state):
        self.no = no
        self._name = name
        self.fraction = fraction
        self._time = time
        self._points = points
        self.remove = remove
        self.cc = cc
        self.war_state = war_state
    
    @property
    def name(self):
        return '%s%s%s%s' % (self._name, '*' if self.remove else '', 'c' if self.cc else '', '(%d)' if self.war_state != 0 else '' )

    @property
    def time(self):
        return di_time(self._time)

    @property
    def op_points(self):
        return self._points

    @property
    def sr_points(self):
        return di_sr_point_function(self._points)

    def execute(self, game_data):
        pass

    def describe(self):
        pass

    def if_prepared(self, game_data):
        return False

    def __str__(self):
        return self.name

class BritishReinforcements(Card):
    def __init__(self):
        Card.__init__(no = 0, name='BritishReinforcement', fraction='ap', time=0, points=4, remove=True, cc=False, war_state=1)

    def describe(self):
        return '2nd Army, 1 Corps'


class CardList:
    def __init__(self, card_list):
        self.card_list = card_list if isinstance(card_list, list) else []

    def shuffle(self):
        random.shuffle(self.card_list)

    def __str__(self):
        return [card.name for card in self.card_list]

    def add_card(self, card):
        self.card_list.append(card)

    def add_cards(self, cards):
        for card in cards:
            self.add_card(card)
    
    def remove_card(self, card_no):
        for card in self.card_list:
            if card.no == card_no:
                 self.card_list.remove(card)
                 break

    def get_all_cards(self):
        to_get = self.card_list
        self.card = []
        return to_get

# This class, printing only the number of cards.
class CardStore(CardList):
    def __str__(self):
        return '%d cards remains' % len(self.card_list)

    def get_cards(self, number):
        if number > 0:
            to_get =  [self.card_list[i] for i in range(0, number)]
            self.card_list = self.card_list[number:]
            return to_get
        return []      
 
def merge_cards(card_store, cards_to_add):
    card_list = cards_to_add.card_list
    card_store.add_cards(card_list)
    card_store.shuffle()

#@TODO: to add the list of the cards in the __init__.
class ApMobilization(CardStore):
    def __init__(self):
        pass

class ApLimitedWar(CardStore):
    def __init__(self):
        pass

class ApTotalWar(CardStore):
    def __init__(self):
        pass

class CpMobilization(CardStore):
    def __init__(self):
        pass

class CpLimitedWar(CardStore):
    def __init__(self):
        pass

class CpTotalWar(CardStore):
    def __init__(self):
        pass

def _initialize_cards(get_Eight_gun=False, card_number):
    ap_hand = CardList()
    cp_hand = CardList()
    ap_mobilization = ApMobilization()
    ap_mobilization.shuffle()
    cp_mobilization = CpMobilization()
    cp_mobilization.shuffle()
    ap_limited_war = ApLimitedWar()
    ap_limited_war.shuffle()
    cp_limited_war = CpLimitedWar()
    cp_limited_war.shuffle()
    ap_total_war = ApTotalWar()
    ap_total_war.shuffle()
    cp_total_war = CpTotalWar()
    cp_total_war.shuffle()
    ap_discard = CardList()
    cp_discard = CardList()   

    #@TODO: the no of eight gun has not been decided 
    if get_Eight_gun:
        cp_hand.add_card(EightGun())
        initial_cards = cp_mobilization.get_cards(number=card_number-1)
        cp_hand.add_cards(initial_cards)
        ap_hand.add_cards(ap_mobilization.get_cards(number=card_number))
    else:
        cp_mobilization.add_card(card=@TODOEightGuns())
        cp_mobilization.shuffle()
        cp_hand.add_cards(cp_mobilization.get_cards(number=card_number))
        ap_hand.add_cards(ap_mobilization.get_cards(number=card_number))
    
    return cp_hand, ap_hand, cp_mobilization, ap_mobilization, cp_limited_war, ap_limited_war, cp_total_war, ap_total_war, cp_discard, ap_discard
