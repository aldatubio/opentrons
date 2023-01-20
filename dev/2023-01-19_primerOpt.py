# Primer Optimization
# Updated 2023-01-19
# Author: OP13 LL
#
# Purpose: Prepare dilution series of one forward and one reverse primer,
# in order to optimize the pair's sensitivity and specificity.
#
# Duration:
#
# Execution: This script will prepare 4X primer pair dilutions as follows:
#     1. Variable forward primer concentrations
#         - 2A: 1:2 | 1000 nM R + 500 nM F
#         - 3A: 1:3 | 1000 nM R + 333 nM F
#         - 4A: 1:4 | 1000 nM R + 250 nM F
#         - 5A: 1:5 | 1000 nM R + 200 nM F
#     2. Dilution series of tubes from previous step
#         - 100%: neat sample from step 1 tube
#         - 75%: 30 µL sample, 10 µL H2O
#         - 50%: 20 µL sample, 20 µL H2O
#         - 25%: 10 µL sample, 30 µL H2O
# 
# Deck setup:
#     1. 200µL filter tips
#     2. 1.5mL tubes in rack, as follows:
#         A1: forward primer
#         B1: reverse primer
#         C1: water
#         A2-D5: empty tubes, to be filled (matching descriptions/names on Labguru)
#     3. 20µL tips


from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'DEV Primer Optimization',
    'author': 'OP13 LL',
    'description': 'text'
}

def run(protocol: protocol_api.ProtocolContext):

    protocol.home()

    # deck setup
    p20tips = protocol.load_labware('opentrons_96_tiprack_20uL', 3)
    p300tips = protocol.load_labware('opentrons_96_tiprack_300uL', 1)
    tubes = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 2)

    # pipette initialization
    p20 = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[p20tips])
    p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[p300tips])


    #################################################
    ### 1. Variable forward primer concentrations ###
    #################################################

    # complex pipetting commands are capable of handling lists -
    # can pass a list of volumes (in µL) and a corresponding list of tubes

    # add water of appropriate volume to each tube
    # 0, 20, 30, 36 µL to A2-A5, respectively
    p300.distribute(
        [20, 30, 36],
        tubes['C1'],
        [tubes.wells_by_name()[tube_name] for tube_name in ['A3', 'A4', 'A5']]
    )

    # add forward primer of appropriate volume to each tube
    # 60, 40, 30, 24 µL to A2-A5, respectively
    p300.distribute(
        [60, 40, 30, 24],
        tubes['A1'],
        [tubes.wells_by_name()[tube_name] for tube_name in ['A2', 'A3', 'A4', 'A5']]
    )

    # add 60 µL reverse primer to A2-A5 and mix
    for i in range(4):
        p300.transfer(
            60,
            tubes['B1'],
            tubes['A'+str(i+2)],
            mix_after = (4, 80)
        )


    ################################
    ### 2. Primer pair dilutions ###
    ################################

    # add water to tubes such that:
    # row B tubes = 10 µL
    # row C tubes = 20 µL
    # row D tubes = 30 µL

    for i in range(3):              # 3 rows: B, C, D
        list = []                   # for each new loop iteration, make an empty list
        row = chr(i+66)             # convert iteration number to row letter using ASCII
        for j in range(4):          # iterate through columns in row
            list.append(row + str(j+2))     # fill list with correct tube names
        p300.distribute(
            (i*10)+10,              # starting with 10µL, add 10µL for every loop iteration
            tubes['C1'],
            [tubes.wells_by_name()[tube_name] for tube_name in list]
        )


    # add primer mix to tubes such that:
    # row B tubes = 30 µL
    # row C tubes = 20 µL
    # row D tubes = 10 µL
    # where tubes B, C, and D in a column are all dilutions of tube A in the same column

    for i in range(4):              # 4 columns: 2, 3, 4, 5
        list = []
        col = str(i+2)              # save iteration number as column number
        for j in range(3):          # iterate through rows in column
            list.append(chr(j+66) + col)   # fill list with correct tube names
        p300.distribute(
            [30, 20, 10],
            tubes['A'+col],
            [tubes.wells_by_name()[tube_name].top(-5) for tube_name in list]
        )

    protocol.home()

run(protocol)