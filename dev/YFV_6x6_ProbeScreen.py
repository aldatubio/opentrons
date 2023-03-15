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
#  - 3: 96-count 20µL tip rack (protocol uses XX tips)


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

    for i in range(4):
        p20.pick_up_tip()
        p20.distribute(
            volume,
            reservoir['A'+str(i+1)],
            plate.wells()
        )