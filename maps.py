from common import *


class Terrain:
    def __init__(self, name):
        self.name = name
        self.allow_flank = True # allow flank
        self.can_cancel_retreat = False # can negate 1 step to cancel retreat
        self.must_stop_advance = False # must stop advance into
        self.can_combat_summer = True # can attack or be attacked in summer
        self.offensive_left = 0

    def __str__(self):
        return self.name

def _get_terrain():
    clear = Terrain('clear')
    forest = Terrain('forest')
    mountain = Terrain('mountain')
    swamp = Terrain('swamp')
    desert = Terrain('desert')

    for t in [forest, mountain, swamp, desert]:
        t.must_stop_advance = True
        t.can_cancel_retreat = True

    for t in [swamp, desert]:
        t.allow_flank = False

    for t in [mountain, swamp]:
        t.offensive_left = 1

    desert.can_combat_summer = False
    return clear, forest, mountain, swamp, desert

clear, forest, mountain, swamp, desert = _get_terrain()

#@TODO: notice: ap and cp has been moved into common.py

class MapHex:
    def __init__(self, name, terrain, **kwargs):
        self.name = name
        self.terrain = terrain

        self.isNE = kwargs['isNE'] if 'isNE' in kwargs else False
        self.isVPHex = kwargs['isVPHex'] if 'isVPHex' in kwargs else False
        self.supplyCenter = kwargs['supplyCenter'] if 'supplyCenter' in kwargs else ''
        self.supplyFrom = kwargs['supplyFrom'] if 'supplyFrom' in kwargs else 'OOS'
        self.controller = kwargs['controller'] if 'controller' in kwargs else 0
        self.fort = kwargs['fort'] if 'fort' in kwargs else 0 # 0 to 3
        self.trench = kwargs['trench'] if 'trench' in kwargs else 0 # 0 to 2
        self.fort_country = kwargs['fort_country'] if 'fort_country' in kwargs else ''

        self.units = kwargs['units'] if 'units' in kwargs else []
        self.neighbours = []


    @property
    def canNegateRetreat(self):
        return self.trench or self.terrain.can_cancel_retreat

    @property
    def canFlank(self):
        return (not self.trench) and self.terrain.allow_flank

    @property
    def canAdvance(self):
        return self.terrain.must_stop_advance

    @property
    def canCombatSummer(self):
        return self.terrain.can_combat_summer

    @property
    def shiftAtk(self):
        return -(self.trench+self.terrain.offensive_left)

    @property
    def shiftDef(self):
        return self.trench>0

    def __repr__(self):
        earthwork_status = ''
        if self.trench:
            earthwork_status += ', Trench {}'.format(self.trench)
        if self.fort:
            earthwork_status += ', Fort {}'.format(self.fort)

        main_status = '{} {}({}{}), {} Control\n{}'.format(
            '#' if not self.isVPHex else '*',
            self.name, self.terrain.name, earthwork_status,
            player_name[self.controller],
            ','.join([unit.__repr__() for unit in self.units]) if self.units else 'No unit'
        )

        return main_status

    def surrunder_under_siege(self):
        self.fort = 0
        return self.transfer_controller()

    def transfer_controller(self):
        self.controller *= -1
        print_system('%s has controlled %s' % (player_name[self.controller], self.name))
        if self.isVPHex:
            return self.controller
        return 0

    def __str__(self):
        main_status = self.__repr__()
        neighbour_status = 'neighbours:'+','.join([n[0] for n in self.neighbours])
        #####这里是补给状况，梓劼你实现一下
        supply_status = 'Supply from: {}'.format(self.supplyFrom) # TBD
        if self.supplyCenter:
            supply_status = 'A valid supply source as {}. '.format(self.supplyCenter)\
                +supply_status
        return main_status+'\n'+neighbour_status+'\n'+supply_status


# the map/saved game
def _link_always_true(unit):
    return True

class Map:
    def __init__(self):
        self.hexes = {}
        self.game_params = {}

    def add_connection(self, name1, name2, cond=_link_always_true):
        self.hexes[name1].neighbours.append((name2,cond))
        self.hexes[name2].neighbours.append((name1,cond))


#from units import POG_units

#def test_map():
#    units = POG_units()

def test_map(unit):
    
    map = Map()
    map.game_params['mapName'] = 'France 1916'

    map.hexes['Paris'] = MapHex('Paris',clear,isVPHex=True,fort=1,trench=1,
        units=[units['FRcs'][0]],controller=ap,fort_country='FR',
        supplyFrom='London'
    )
    map.hexes['C-T'] = MapHex('C-T',clear,isVPHex=False,trench=1,
        units=[units['FR1'].flip(),units['FR2'],units['FR3']],controller=ap,
        supplyFrom='London'
    )
    map.hexes['Verdun'] = MapHex('Verdun',clear,isVPHex=True,fort=3,trench=1,
        units=[units['FR4'],units['FR5'],units['FR6']],controller=ap,
        supplyFrom='London', fort_country='FR',
    )
    map.hexes['Cambrai'] = MapHex('Cambrai',clear,isVPHex=True,trench=1,
        units=[units['BR1'],units['BR2']],controller=ap,
        supplyFrom='London'
    )
    map.hexes['Calais'] = MapHex('Calais',clear,isVPHex=True,
        units=[],controller=ap,
        supplyCenter='AP port',
        supplyFrom='London'
    )
    map.hexes['Amiens'] = MapHex('Amiens',clear,isVPHex=True,
        units=[],controller=ap,
        supplyFrom='London'
    )
    map.hexes['Ostend'] = MapHex('Ostend',clear,isVPHex=True,trench=1,
        units=[units['BE1'],units['BEF'],units['BR3']],controller=ap,
        supplyCenter='AP port',
        supplyFrom='London'
    )
    map.hexes['London'] = MapHex('London',clear,
        units=[],controller=ap,
        supplyCenter='London',
        supplyFrom='London'
    )
    map.hexes['Sedan'] = MapHex('Sedan',clear,isVPHex=True,trench=2,
        units=[units['GE1'],units['GE2'],units['GE3']],controller=cp,
        supplyFrom='Essen'
    )
    map.hexes['Brussels'] = MapHex('Brussels',clear,isVPHex=True,trench=2,
        units=[units['GE4'],units['GE5'],units['GE6']],controller=cp,
        supplyFrom='Essen'
    )
    map.hexes['Metz'] = MapHex('Metz',clear,isVPHex=True,trench=2,fort=3,
        units=[units['GE7'],units['GE8'],units['GEcs'][0]],controller=cp,
        supplyFrom='Essen',fort_country='GE',
    )
    map.hexes['Essen'] = MapHex('Essen',clear,isVPHex=True,
        units=[],controller=cp,
        supplyCenter='Essen',
        supplyFrom='Essen'
    )

    map.hexes['CPRB'] = MapHex('CP RB',clear,
        units=units['GEcs'][1:10],controller=cp,
    )
    map.hexes['APRB'] = MapHex('AP RB',clear,
        units=units['FRcs'][4:8]+units['BRcs'][:4]+units['BEFcs']+units['BEcs'],controller=ap,
    )
    map.hexes['CPElim'] = MapHex('CP Elim',clear,
        units=[],controller=cp,
    )
    map.hexes['APElim'] = MapHex('AP Elim',clear,
        units=[units['FR9'],units['FRcs'][1],units['FRcs'][2],units['FRcs'][3]],controller=ap,
    )

    map.add_connection('Paris','C-T')
    map.add_connection('Verdun','C-T')
    map.add_connection('Sedan','C-T')
    map.add_connection('Cambrai','C-T')
    map.add_connection('Paris','Amiens')
    map.add_connection('Calais','Amiens')
    map.add_connection('Cambrai','Amiens')
    map.add_connection('Calais','Ostend')
    map.add_connection('Calais','London',lambda unit:unit.isBR)
    map.add_connection('Calais','Cambrai')
    map.add_connection('Brussels','Ostend')
    map.add_connection('Brussels','Cambrai')
    map.add_connection('Verdun','Sedan')
    map.add_connection('Cambrai','Sedan')
    map.add_connection('Metz','Sedan')
    map.add_connection('Verdun','Metz')
    map.add_connection('Verdun','Essen')
    map.add_connection('Metz','Essen')
    map.add_connection('Brussels','Essen')

    return map
