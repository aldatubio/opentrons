# Probe Selection | 6x6 Matrix for YFV
# Updated 2023-03-15
# Author: OP13 LL
# 
# Purpose: plate primer pairs and probes on a 384-well plate
#          such that each probe is tested with four different primer pairs
#          and three different templates [vaccine strain, wild type strain, and hgDNA].
# 
# Execution: This script fills the first 12 rows of a 384-well plate [columns 1-18] as follows:
#  - STEP 1: Primer pairs
#      - Rows A, E, I: F1R1
#      - Rows B, F, J: F2R1
#      - Rows C, G, K: F1R2
#      - Rows H, H, L: F2R2
#  - STEP 2: Probes
#      - Columns 1-3: probe 1
#      - Columns 4-6: probe 2
#      - ...
#      - Columns 15-18: probe 6
#      
# Reaction [total 4µL per well]:
#  - 2µL 10X forward-reverse primer mix
#  - 2µL 10X probe
#  
# Deck setup:
#  - 1: 24-count 1.5mL snap cap tube rack, with tubes as follows:
#       - tubes A1-4: 10X forward-reverse primer mixes
#       - tubes D1-6: 10X probes
#  - 2: Applied Biosystems 384-well MicroAmp plate
#  - 3: 96-count 20µL tip rack (protocol uses 10 tips)


from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Probe Selection | 6x6 Matrix for YFV',
    'author': 'OP13 LL',
    'description': '''For use in 7B10 robot. | 
                   LIQUID SETUP [1.5mL tubes]:
                   A1-4 = 10X forward-reverse primer mixes,
                   D1-6 = 10X probes.'''
}

def run(protocol: protocol_api.ProtocolContext):

    # 0. INITIALIZATION

    # user-defined variables - edit as necessary
    # volume of primer mix and probe to pipette (in µL)
    volume = 2
    # height of tip above bottom of well when dispensing (in mm)
    probeTipHeight = 4.5

    protocol.home()

    # deck setup
    # attribute = protocol.load_labware('name', position)
    p20tips = protocol.load_labware('opentrons_96_tiprack_20uL', 3)
    reservoir = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 1)
    plate = protocol.load_labware('appliedbiosystemsmicroamp_384_wellplate_40ul', 2)

    # pipette initialization/setup
    p20 = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[p20tips])


    # 1. PRIMER PAIRS
    # fill rows [x, x+4, x+8] with primer mix (for rows A-L, wells 1-18)
    # ex. F1R1 --> A, E, I
    # use 1 tip per primer pair

    # How the construction of loops works below:
    # Opentrons' list of wells (when using labware.wells() method)
    # goes by column. So, well A1 is well 0, but well A2 is well 16 (initializing at zero).
    # Because of this, we have to create the following list to access A1-A18:
    # [0, 16, 32, 48... 272]
    # Therefore, to access A1-A18, we can use a loop:
    # for k in range(18): list.append(k*16)
    # For E1-E18, we want the following list:
    # [4, 20, 36, 52... 276]
    # We can modify the loop to achieve this:
    # for k in range(18): list.append((k*16) + 4)
    # By using "i + 4" where i = 0, we can set ourselves up to iterate with i
    # such that an increase in i corresponds with a new primer mix
    # and a new set of rows (ex. i = 1 results in lists for rows B and F).

    for i in range(4):                     # iterate through primer mixes 1-4
        list = []
        for k in range(18):                # only use first 18 wells in row
            list.append((k*16)+i)          # make list: wells A1-A18 when i = 0
        p20.pick_up_tip()                  # one tip per primer mix
        p20.distribute(
            volume,
            reservoir['A'+str(i+1)],       # primer mix 1 when i = 0
            plate.wells(list),
            new_tip = 'never'
        )
        list = []
        for k in range(18):
            list.append((k*16)+(i+4))      # make list: wells E1-E18 when i = 0
        p20.distribute(
            volume,
            reservoir['A'+str(i+1)],
            plate.wells(list),
            new_tip = 'never'
        )
        list = []
        for k in range(18):
            list.append((k*16)+(i+8))      # make list: wells I1-I18 when i = 0
        p20.distribute(
            volume,
            reservoir['A'+str(i+1)],
            plate.wells(list),
            new_tip = 'never'
        )
        p20.drop_tip()                     # drop tip after all 3 rows filled with primer mix

    # 2. PROBES
    # fill groups of three columns with probe (for rows A-L, wells 1-18)
    # ex. probe 1 --> 1, 2, 3
    # use 1 tip per probe

    # first, adjust dispense height (in mm) - don't touch primers in wells
    p20.well_bottom_clearance.dispense = probeTipHeight

    # loop logic below:
    # k allows us to add the wells in rows A through L to the list for each column
    # j allows us to add those 12 wells for all 3 columns that get the probe
    # (i*48) modifier means that with each increase in i (each new probe), we're moving over by 3 columns
    # so, when i = 0, first probe will go in columns 1-3;
    # when i = 1, second probe will go in columns 4-6

    for i in range(6):                            # 6 probes
        list = []
        for j in range(3):                        # 3 columns to fill (0-3 when i = 0)
            for k in range(12):
                list.append(k+(16*j)+(i*48))      # create list of first 12 wells in all 3 columns
        p20.distribute(
            volume,
            reservoir['D'+str(i+1)],
            plate.wells(list),
            touch_tip = True
        )

    protocol.home()