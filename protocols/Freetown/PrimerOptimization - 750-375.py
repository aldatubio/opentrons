# Primer Optimization
# Updated 2023-07-27
# Author: OP13 LL
#
# Purpose: Prepare dilution series of one forward and one reverse primer,
# in order to optimize the pair's sensitivity and specificity.
#
# Duration: 7.5 min
#
# Execution: This script will prepare 4X primer pair dilutions as follows:
#     1. Variable forward primer concentrations
#         - 2A: 1:2 | 750 nM R + 375 nM F
#         - 3A: 1:3 | 750 nM R + 250 nM F
#         - 4A: 1:4 | 750 nM R + 188 nM F
#         - 5A: 1:5 | 750 nM R + 150 nM F
#     2. Dilution series of tubes from previous step
#         - 100%: neat sample from step 1 tube
#         - 83%: 33 µL sample, 7 µL H2O
#         - 67%: 27 µL sample, 13 µL H2O
#         - 50%: 20 µL sample, 20 µL H2O
# 
# Deck setup:
#     1. 5mL screw-cap tube of water in rack (located in slot A5)
#     2. 1.5mL snap-cap tubes in rack, as follows:
#         A1: forward primer (250 µL)
#         B1: reverse primer (250 µL)
#         A2-D5: empty tubes, to be filled (matching descriptions/names on Labguru)
#     3. 200µL filter tips (uses 12 tips)



from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Primer Optimization [750R to 375R] | prepares 1 plate',
    'author': 'OP13 LL',
    'description': '''Performs dilutions for primer optimization [reverse ranges from 750nM to 375nM]. || 
                    TUBE SETUP: 5mL screw-cap tube of water in slot A5 of large tube rack;
                    in small tube rack,
                    1.5mL snap-cap tubes with 250µL of primers (A1: 375nM, B1: 750nM);
                    and 16 empty 1.5mL snap-cap tubes in slots A2-D5.'''
}

def run(protocol: protocol_api.ProtocolContext):

    protocol.home()

    # multiplier
    # increase by 1 = increase number of plates prepped by 1
    # NOTE: multiplier >2 may result in cross-contamination
    # (if entire volume to be added is greater than 200uL,
    #  Opentrons will double-dip - for example:
    #  add 200uL, mix, then go back to source well with same tip
    #  and transfer an additional 40uL, then mix again).
    # Use multiplier >2 at your own risk.
    p = 1

    ### 2023-07-27: Overage when preparing only one plate was not sufficient in A tubes.
    ### To prepare additional overage [25% more], include the following line:
    p = p*1.25

    # deck setup
    p300tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
    tubes = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 2)
    # custom 5mL tube definition
    water = protocol.load_labware('usascientific_15_tuberack_5000ul', 1)

    # pipette initialization
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300tips])


    #################################################
    ### 1. Variable forward primer concentrations ###
    #################################################

    # complex pipetting commands are capable of handling lists -
    # can pass a list of volumes (in µL) and a corresponding list of tubes

    # add water of appropriate volume to each tube
    # 0, 20, 30, 36 µL to A2-A5, respectively

    p300.distribute(
        [20*p, 30*p, 36*p],
        water['A5'],
        [tubes.wells_by_name()[tube_name] for tube_name in ['A3', 'A4', 'A5']],
        disposal_volume = 10    # default excess is 20 µL (10% of pipette max) which seems wasteful
    )

    # add forward primer of appropriate volume to each tube
    # 60, 40, 30, 24 µL to A2-A5, respectively
    p300.distribute(
        [60*p, 40*p, 30*p, 24*p],
        tubes['A1'],
        [tubes.wells_by_name()[tube_name].bottom(10) for tube_name in ['A2', 'A3', 'A4', 'A5']],
        disposal_volume = 10,
	    touch_tip = True
    )

    # add 60 µL reverse primer to A2-A5 and mix
    for i in range(4):
        p300.transfer(
            60*p,
            tubes['B1'],
            tubes['A'+str(i+2)],
            mix_after = (4, 80*p)
        )

    # Set p back to original value if it has been adjusted by 25%
    if not (p).is_integer():
        p = p*0.8

    ################################
    ### 2. Primer pair dilutions ###
    ################################

    # add water to tubes such that:
    # row B tubes = 6.7 µL
    # row C tubes = 13.3 µL
    # row D tubes = 20 µL

    p300.pick_up_tip()              # allows use of new_tip = 'never'
    for i in range(3):              # 3 rows: B, C, D
        list = []                   # for each new loop iteration, make an empty list
        row = chr(i+66)             # convert iteration number to row letter using ASCII
        for j in range(4):          # iterate through columns in row
            list.append(row + str(j+2))     # fill list with correct tube names
        p300.distribute(
            ((i*6.6)+6.7)*p,              # starting with 6.7µL, add 6.6µL for every loop iteration
            water['A5'],
            [tubes.wells_by_name()[tube_name] for tube_name in list],
            disposal_volume = 10,
            new_tip = 'never'       # one tip for all water dispenses
        )
    p300.drop_tip()


    # add primer mix to tubes such that:
    # row B tubes = 33.3 µL
    # row C tubes = 26.7 µL
    # row D tubes = 20 µL
    # where tubes B, C, and D in a column are all dilutions of tube A in the same column

    for i in range(4):              # 4 columns: 2, 3, 4, 5
        list = []
        col = str(i+2)              # save iteration number as column number
        for j in range(3):          # iterate through rows in column
            list.append(chr(j+66) + col)   # fill list with correct tube names
        p300.distribute(
            [33.3*p, 26.7*p, 20*p],
            tubes['A'+col],
            [tubes.wells_by_name()[tube_name].top(-15) for tube_name in list],
            disposal_volume = 10,
            touch_tip = True
        )

    protocol.home()