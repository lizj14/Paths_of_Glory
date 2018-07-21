from common import *

crt_table_army = {
    '1':[0,1,1,1,2,2],
    '2':[1,1,2,2,3,3],
    '3':[1,2,2,3,3,4],
    '4':[2,2,3,3,4,4],
    '5':[2,3,3,4,4,5],
    '6-8':[3,3,4,4,5,5],
    '9-11':[3,4,4,5,5,7],
    '12-14':[4,4,5,5,7,7],
    '15':[4,5,5,7,7,7],
    '16+':[5,5,7,7,7,7],
}

crt_table_army_name = list(crt_table_army.keys())
crt_table_army_name = ['A'+e for e in crt_table_army_name]
crt_table_army_value = list(crt_table_army.values())

crt_table_corp = {
    '0':[0,0,0,0,1,1],
    '1':[0,0,0,1,1,1],
    '2':[0,1,1,1,1,1],
    '3':[1,1,1,1,2,2],
    '4':[1,1,1,2,2,2],
    '5':[1,1,2,2,2,3],
    '6':[1,1,2,2,3,3],
    '7':[1,2,2,3,3,4],
    '8+':[2,2,3,3,4,4],
}

crt_table_corp_name = list(crt_table_corp.keys())
crt_table_corp_name = ['C'+e for e in crt_table_corp_name]
crt_table_corp_value = list(crt_table_corp.values())

crt_th_army = [2,3,4,5,6,9,12,15,16,10086]
crt_th_corp = [1,2,3,4,5,6,7,8,10086]

# get loss factor.
# shift: column shift
# drm: dice roll modifier
def LF(fire, is_army=True, shift=0, drm=0):
    # determine army or corp
    if is_army:
        crt_th = crt_th_army
        crt_name = crt_table_army_name
        crt_value = crt_table_army_value
    else:
        crt_th = crt_th_corp
        crt_name = crt_table_corp_name
        crt_value = crt_table_corp_value

    # decide the column used
    for column in range(10086):
        if fire<crt_th[column]:
            break
    column = column+shift
    column = max(column, 0)
    column = min(column, len(crt_th)-1)
    column_name = crt_name[column]

    # decide the dice
    origin_dice = d6()
    dice = origin_dice+drm
    dice = max(dice, 1)
    dice = min(dice, 6)
    dice_name = str(origin_dice)
    if drm != 0:
        dice_name += '+({})'.format(drm)

    print ('Attack with {}, rolled {}'.format(column_name, dice_name))
    # get result
    loss = crt_value[column][dice-1]
    print ('LF={}'.format(loss))

    return loss

def test_LF():
    for i in range(20):
        LF(np.random.randint(0,20), True, shift=np.random.randint(-2,2), drm=np.random.randint(-2,2))
    for i in range(20):
        LF(np.random.randint(0,10), False, shift=np.random.randint(-2,2), drm=np.random.randint(-2,2))

# take loss.
# avaliable params:
# isAttacker : about mdzz
# ifWithdrawal : about whether a corp step loss is taken
mdzz_priority = ['BEF', 'BEFc', 'CAU', 'MEF', 'AUSc']
def take_loss(units, loss, **params):



# flank=-1 for no flank
def battle(attacker_units, defender_units, flank_drm=-1):
    if flank_drm>=0:
        if flank_drm+d6()>=4: # success when 4-6
            flank_success = True
        else:
            flank_success = Falses
    else:
        flank_success = None
