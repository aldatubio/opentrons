# Various Primers | Variation on Primer Selection Protocol
# Updated 2023-04-21
# Author: OP13 LL
# 
# Purpose: plate primer pairs and probes on a 384-well plate
#          such that each probe is tested with twelve different primer pairs.
# 
# Execution: This script fills the first 12 rows of a 384-well plate [columns 1-18] as follows:
#      
# Reaction [total 6µL per well]:
#  - 2µL 10X forward primer
#  - 2µL 10X reverse primer
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
    'apiLevel': '2.14',
    'protocolName': '434/577 Various Probes',
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
    reverseTipHeight = 4.5

    protocol.home()

    # deck setup
    # attribute = protocol.load_labware('name', position)
    p20tips = protocol.load_labware('opentrons_96_tiprack_20uL', 3)
    reservoir = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 1)
    probes = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 6)
    plate = protocol.load_labware('appliedbiosystemsmicroamp_384_wellplate_40ul', 2)

    # pipette initialization/setup
    p20 = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[p20tips])

   # liquid definitions - to create layout map with labels/colors
    fwd434Orig = protocol.define_liquid('434 Forward - Original PANDAA',display_color = '#0700c4')
    fwd434ADR = protocol.define_liquid('434 Forward - ADRd1',display_color = '#00f')
    fwd434PDR = protocol.define_liquid('434 Forward - Short PDR',display_color = '#0052ff')

    reservoir['A1'].load_liquid(fwd434Orig,100)
    reservoir['A2'].load_liquid(fwd434ADR,100)
    reservoir['A3'].load_liquid(fwd434PDR,100)


    # 1. FORWARD PRIMERS
    # See plate layout for more details;
    # each "block" of 8 wells (ex. A1-B4, C1-D4, etc) gets one forward primer

    for i in range(6):                                  # iterate through six column-sections (cols 1-4, 5-8, 9-12... 21-24)
        for j in range(2):                              # iterate through two forward primers for each column-section
            list = []
            row = chr(j+65)                             # j is 0 or 1; convert this to row A or B (ASCII)
            for k in range(16):                         # 16 sets of 2 wells to be filled with each primer
                list.append((k*4)+(2*j)+(i*64))         # well 0, 4, 8... j multiplier = first two or second two in block (i.e., wells 0&1 or wells 2&3)
                list.append((k*4+1)+(2*j)+(i*64))       # well 1, 5, 9... i multiplier = column-section
            p20.pick_up_tip()                           # one tip per primer
            p20.distribute(
                volume,
                reservoir[row+str(i+1)],
                [plate.wells()[wellIndex] for wellIndex in list],
                new_tip = 'never'
            )
            p20.drop_tip()                              # drop tip after primer has been distributed fully

    # 2. REVERSE PRIMERS
    # See plate layout for more details;
    # reverse primers are added in alternating stripes (ex. A1-A4, C1-C4, etc)

    # first, adjust dispense height (in mm) - don't touch primers in wells
    p20.well_bottom_clearance.dispense = reverseTipHeight

    for i in range(6):                                  # iterate through six column-sections (cols 1-4, 5-8, 9-12... 21-24)
        for j in range(2):                              # iterate through two reverse primers for each column-section
            list = []
            row = chr(j+67)                             # j is 0 or 1; convert this to row C or D (ASCII)
            for k in range(32):                         # 32 wells to be filled with each primer
                list.append((k*2)+j+(i*64))             # well 0, 2, 4... j multiplier = odd or even within column
            p20.pick_up_tip()                           # one tip per primer
            p20.distribute(
                volume,
                reservoir[row+str(i+1)],
                [plate.wells()[wellIndex] for wellIndex in list],
                new_tip = 'never',
                touch_tip = True
            )
            p20.drop_tip()                              # drop tip after primer has been distributed fully


    #3. PROBES

    # loop logic below:
    # k allows us to add the wells in rows A through L to the list for each column
    # j allows us to add those 12 wells for all 3 columns that get the probe
    # (i*48) modifier means that with each increase in i (each new probe), we're moving over by 3 columns
    # so, when i = 0, first probe will go in columns 1-3;
    # when i = 1, second probe will go in columns 4-6

    for i in range(2):                                  # iterate through two column-sections (cols 1-12, 13-24)
        list = []
        for j in range(12):                             # 12 columns to fill per probe
            for k in range(8):                          # 8 wells to fill per column
                list.append(k+(j*16)+96*i)                   
            p20.pick_up_tip()                           # one tip per probe
            p20.distribute(
                volume,
                probes['D'+str((i*2)+1)],
                [plate.wells()[wellIndex] for wellIndex in list],
                new_tip = 'never',
                touch_tip = True
            )
            p20.drop_tip()                              # drop tip after primer has been distributed fully

        list = []
        for j in range(12):                             # 12 columns to fill per probe
            for k in range(8):                          # 8 wells to fill per column
                list.append(k+((j*16)+8)+96*i)                   
            p20.pick_up_tip()                           # one tip per probe
            p20.distribute(
                volume,
                probes['D'+str((i*2)+2)],
                [plate.wells()[wellIndex] for wellIndex in list],
                new_tip = 'never',
                touch_tip = True
            )
            p20.drop_tip()                              # drop tip after primer has been distributed fully