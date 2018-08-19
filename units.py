from common import *


# class Unit
# the basic unit class in pog
# properties: name, attack, defence, movement, isflipped;
# advanced attributes: rp, isArmy, rpCountry, can SR/MV to NE
class Unit:
    def __init__(self, name, atks, defs, movs):
        self._name = name
        self._atks = atks
        self._defs = defs
        self._movs = movs
        self.flipped = 0

        self.isArmy = False
        self.rpCountry = None
        self.canSRNE = False
        self.canMVNE = False

        self.isBR = False
        self.isRU = False
        self.isIT = False

    def flip(self):
        self.flipped = 1-self.flipped
        return self

    @property
    def name(self):
        return self._name+self.flipped*'-'

    @property
    def attack(self):
        return self._atks[self.flipped]

    @property
    def defence(self):
        return self._defs[self.flipped]

    @property
    def movement(self):
        return self._movs[self.flipped]

    @property
    def isFlipped(self):
        return self.flipped==0

    @isFlipped.setter
    def isFlipped(self, value):
        self.flipped = (value==1)

    def __repr__(self):
        main_status = 'unit {}-{}-{} {}'.format(
            self.attack, self.defence, self.movement, self.name)
        if self.rpCountry == None:
            main_status += '*'

        return main_status

    def __str__(self):
        main_status = self.__repr__()

        rp_status = ''
        if self.flipped:
            rp_status += 'Currently at Reduced Strength. '
        else:
            rp_status += 'Currently at Full Strength. '
        if self.rpCountry != None:
            rp_status += 'Use {} RP.'.format(self.rpCountry)
        else:
            rp_status += 'Cannot be replaced.'

        ne_status = 'can SR to NE: {}, can move to NE: {}'.format(
            self.canSRNE, self.canMVNE)

        return main_status+'\n'+rp_status+'\n'+ne_status


def _duplicate_units(n, format_string, empty_no, *unit_params):
    return [Unit(format_string.format(i),*unit_params)
        for i in range(1,n+1) if not i in empty_no]


# generate all units in PoG and their a-d-m value
def _get_all_units():
    all_units = {}
    all_units['GEa'] = _duplicate_units(18, 'GE{}', [13,15,16], [5,3], [3,3], [3,3])

    all_units['AHa'] = _duplicate_units(11, 'AH{}', [8,9], [3,1], [2,2], [3,3])
    tua_params = ([1,1], [2,2], [3,2])
    all_units['AoI'] = [Unit('AoI',*tua_params)]
    all_units['YLD'] = [Unit('YLD',*tua_params)]

    all_units['GEc'] = _duplicate_units(19, 'GEc', [], [2,1], [1,1], [4,4])
    all_units['AHc'] = _duplicate_units(11, 'AHc', [], [1,0], [1,1], [3,3])
    all_units['TUc'] = _duplicate_units(15, 'TUc', [], [1,0], [1,1], [3,3])
    all_units['BUc'] = _duplicate_units(6, 'BUc', [], [2,0], [1,1], [3,3])
    all_units['SNc'] = [Unit('SNc', [1,0], [1,1], [1,1])]

    all_units['BRa'] = _duplicate_units(5, 'BR{}', [], [4,3], [3,3], [3,3])
    all_units['BEF'] = [Unit('BEF', [5,4], [3,3], [3,3])]
    all_units['MEF'] = [Unit('MEF', [1,1], [2,2], [3,3])]
    all_units['Alb'] = [Unit('Alb', [4,3], [3,3], [3,3])]
    all_units['FRa'] = _duplicate_units(10, 'FR{}', [8], [3,2], [3,3], [3,3])
    all_units['AoO'] = [Unit('AoO', [3,2], [3,3], [3,3])]
    all_units['RUa'] = _duplicate_units(12, 'RU{}', [], [3,2], [2,2], [3,3])
    all_units['CAU'] = [Unit('CAU', [3,2], [2,2], [3,3])]
    all_units['USa'] = _duplicate_units(2, 'US{}', [], [5,3], [3,3], [3,3])
    all_units['BEa'] = [Unit('BE1', [2,1], [3,3], [3,3])]
    all_units['SBa'] = _duplicate_units(2, 'SB{}', [], [2,1], [2,2], [3,3])
    all_units['ITa'] = _duplicate_units(5, 'IT{}', [], [2,1], [2,2], [3,3])


    all_units['BRc'] = _duplicate_units(10, 'BRc', [], [2,1], [1,1], [4,4])
    all_units['FRc'] = _duplicate_units(10, 'FRc', [], [1,1], [1,1], [4,4])
    all_units['BEc'] = _duplicate_units(1, 'BEc', [], [1,0], [1,1], [3,3])
    all_units['ITc'] = _duplicate_units(7, 'ITc', [], [1,0], [1,1], [3,3])
    all_units['USc'] = _duplicate_units(6, 'USc', [], [2,1], [1,1], [4,4])

    all_units['RUc'] = _duplicate_units(18, 'RUc', [], [1,1], [1,1], [3,3])
    all_units['ROc'] = _duplicate_units(6, 'ROc', [], [1,0], [1,1], [3,3])
    all_units['GRc'] = _duplicate_units(3, 'GRc', [], [1,0], [1,1], [3,3])
    all_units['SBc'] = _duplicate_units(2, 'SBc', [], [1,0], [1,1], [4,4])
    all_units['MNc'] = _duplicate_units(2, 'MNc', [], [1,0], [1,1], [0,0])


    all_units['BEFc'] = [Unit('BEFc', [2,2], [2,1], [4,4])]
    all_units['AUSc'] = [Unit('AUSc', [2,2], [1,1], [4,4])]
    all_units['CNDc'] = [Unit('CNDc', [2,2], [1,1], [4,4])]
    all_units['ANAc'] = [Unit('ANAc', [1,0], [1,1], [3,3])]
    all_units['PTc'] = [Unit('PTc', [1,0], [1,1], [3,3])]


    return all_units

# set advanced attributes
def _initialize_units():
    all_units = _get_all_units()
    for key, units in all_units.items():
        for unit in units:
            if key[-1] == 'c':
                unit.isArmy = False
            else:
                unit.isArmy = True
                unit.canSRNE = False

            if key[:-1] in ['BR', 'FR', 'IT', 'RU', 'US', 'GE', 'AH', 'TU', 'BU']:
                unit.rpCountry = key[:-1]
            elif key in ['BEa', 'BEc', 'ROc', 'GRc', 'SBa', 'SBc', 'MNc',
                'AUSc', 'CNDc', 'PTc', 'ANAc']:
                unit.rpCountry = 'A'
            elif key in ['BEF', 'BEFc', 'AoO', 'Alb', 'MEF', 'CAU', 'AoI',
                'YLD', 'SNc']:
                unit.rpCountry = None
            else:
                assert(False)

            if key in ['MEF', 'Alb', 'AoO', 'AoI', 'YLD']:
                unit.canMVNE = True
            elif key in ['BRc', 'RUc', 'GEc', 'AHc', 'BUc', 'TUc', 'AUSc']:
                unit.canMVNE = True
                unit.canSRNE = True
            elif key[-1] == 'c':
                unit.canMVNE = True
                unit.canSRNE = False
            else:
                unit.canMVNE = False

            if key[:-1]=='BR':
                unit.isBR = True
            elif key[:-1]=='RU':
                unit.isRU = True
            elif key[:-1]=='IT':
                unit.isIT = True
            elif key in ['BEF', 'BEFc', 'CNDc', 'AUSc', 'PTc', 'Alb', 'MEF']:
                unit.isBR = True
    return all_units

def POG_units():
    all_units = _initialize_units()
    POG_units = {}
    for key, units in all_units.items():
        if key[-1] == 'c':
            POG_units[key+'s'] = units
        else:
            for unit in units:
                POG_units[unit.name] = unit

    return POG_units
