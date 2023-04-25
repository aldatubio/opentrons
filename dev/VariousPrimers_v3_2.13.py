# Various Primers | Variation on Primer Selection Protocol
# Updated 2023-04-25
# Author: OP13 LL
# 
# Purpose: plate primer pairs and probes on a 384-well plate
#          such that each of 14 probes is tested with 3 primer pairs.
# 
# Execution: THIS SCRIPT IS NOT COMPLETE. SEE SECTION WITH FOUR #### LINES FOR END OF COMPLETE CODE.
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
    'apiLevel': '2.13',
    'protocolName': '434/577 Various Probes v3',
    'author': 'OP13 LL',
    'description': 'For use in 7B10 robot. See plate map; order of primers in each column is the order they should be loaded into tube rack rows.'
}

def run(protocol: protocol_api.ProtocolContext):

    ########################################################################################
    ########################################################################################
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
    fwdprimers = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 4, 'Forward Primers')
    revprimers = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 5, 'Reverse Primers')
    probes = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 6, 'Probes')
    plate = protocol.load_labware('appliedbiosystemsmicroamp_384_wellplate_40ul', 2)

    # pipette initialization/setup
    p20 = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[p20tips])


    ########################################################################################
    ########################################################################################
    # 1A. FORWARD PRIMERS - 422/586
    # See plate layout for more details
    # 422 and 586 foward primers - 3 primers for each, same plate layout

    for i in range(2):
        if i == 0:
            row = 'A'                             # first time through loop: 422 region
        else:
            row = 'D'                             # second time through loop: 586 region

        list = []                                           # 385.F.1 - first primer
        for j in range(6):                                  # columns 1-6 [for 422 region]; columns 19-24 [586 region]
            for k in range(2):                              # top vs bottom half of plate
                list.append( (j*16)    + (k*8) + (i*288))   # row A/I. i multiplier: move to column 19 (16*18) for 586 region
                list.append(((j*16)+1) + (k*8) + (i*288))   # row B/J. k multiplier: when k=1, move to bottom half of plate
        p20.pick_up_tip()
        p20.distribute(
            volume,
            fwdprimers[row+'1'],                  # first primer is in first slot of the row
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never'
        )
        p20.drop_tip()

        list = []                                 # 385.F.1.Ad2 - second primer
        for j in range(6):
            for k in range(2):
                list.append(((j*16)+2) + (k*8) + (i*288))   # row C/K
                list.append(((j*16)+4) + (k*8) + (i*288))   # row E/M
                list.append(((j*16)+5) + (k*8) + (i*288))   # row F/N
        p20.pick_up_tip()
        p20.distribute(
            volume,
            fwdprimers[row+'2'],                  
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never'
        )
        p20.drop_tip()

        list = []                                 # 385.F.1.Ad1 - third primer
        for j in range(6):
            for k in range(2):
                list.append(((j*16)+3) + (k*8) + (i*288))   # row D/L
        p20.pick_up_tip()
        p20.distribute(
            volume,
            fwdprimers[row+'3'],                  
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never'
        )
        p20.drop_tip()
   
    ########################################################################################
    ########################################################################################
    # 1B. FORWARD PRIMERS - 434/577
    # 4 primers for each, same plate layout

    for i in range(2):
        if i == 0:
            row = 'B'                             # first time through loop: 434 region
        else:
            row = 'C'                             # second time through loop: 577 region

        list = []                                           # 398.F.1 - first primer
        for j in range(6):                                  # j+96 = start at column 7 instead of column 1
            for k in range(2):                              
                list.append( 96+(j*16)    + (k*8) + (i*96))    # row A/I. i multiplier: move to column 13 (16*6) for 577 region
                list.append((96+(j*16)+2) + (k*8) + (i*96))   # row C/K
        p20.pick_up_tip()
        p20.distribute(
            volume,
            fwdprimers[row+'1'],                  # first primer is in first slot of the row
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never'
        )
        p20.drop_tip()

        list = []                                 # 403.F.1 - second primer
        for j in range(6):
            for k in range(2):
                list.append((96+(j*16)+1) + (k*8) + (i*96))   # row B/J
        p20.pick_up_tip()
        p20.distribute(
            volume,
            fwdprimers[row+'2'],                  
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never'
        )
        p20.drop_tip()

        list = []                                 # 398.F.1.Ad2 - third primer
        for j in range(6):
            for k in range(2):
                list.append((96+(j*16)+3) + (k*8) + (i*96))   # row D/L
                list.append((96+(j*16)+5) + (k*8) + (i*96))   # row F/N
                list.append((96+(j*16)+6) + (k*8) + (i*96))   # row G/O
        p20.pick_up_tip()
        p20.distribute(
            volume,
            fwdprimers[row+'3'],                  
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never'
        )
        p20.drop_tip()

        list = []                                 # 398.F.1.Ad1 - fourth primer
        for j in range(6):
            for k in range(2):
                list.append((96+(j*16)+4) + (k*8) + (i*96))   # row E/M
        p20.pick_up_tip()
        p20.distribute(
            volume,
            fwdprimers[row+'4'],                  
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never'
        )
        p20.drop_tip()


    ########################################################################################
    ########################################################################################
    # 2A. REVERSE PRIMERS - 422/586
    # See plate layout for more details.

    # first, adjust dispense height (in mm) - don't touch forward primers in wells
    p20.well_bottom_clearance.dispense = reverseTipHeight

    ########
    # 422 and 586 foward primers - 3 primers for each, same plate layout
    for i in range(2):
        if i == 0:
            row = 'A'                             # first time through loop: 422 region
        else:
            row = 'D'                             # second time through loop: 586 region

        list = []                                           # 458.R.1 - first primer
        for j in range(6):                                  # columns 1-6 [for 422 region]; columns 19-24 [586 region]
            for k in range(2):                              # top vs bottom half of plate
                list.append( (j*16)    + (k*8) + (i*288))   # row A/I. i multiplier: move to column 19 (16*18) for 586 region
                list.append(((j*16)+2) + (k*8) + (i*288))   # row C/K. k multiplier: when k=1, move to bottom half of plate
        p20.pick_up_tip()
        p20.distribute(
            volume,
            revprimers[row+'1'],                  # first primer is in first slot of the row
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never',
            touch_tip = True
        )
        p20.drop_tip()

        list = []                                 # 458.R.1.Ad2 - second primer
        for j in range(6):
            for k in range(2):
                list.append(((j*16)+1) + (k*8) + (i*288))   # row B/J
                list.append(((j*16)+3) + (k*8) + (i*288))   # row D/L
                list.append(((j*16)+5) + (k*8) + (i*288))   # row F/N
        p20.pick_up_tip()
        p20.distribute(
            volume,
            revprimers[row+'2'],                  
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never',
            touch_tip = True
        )
        p20.drop_tip()

        list = []                                 # 458.R.1.Ad1 - third primer
        for j in range(6):
            for k in range(2):
                list.append(((j*16)+4) + (k*8) + (i*288))   # row E/M
        p20.pick_up_tip()
        p20.distribute(
            volume,
            revprimers[row+'3'],                  
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never',
            touch_tip = True
        )
        p20.drop_tip()

    ########################################################################################
    ########################################################################################
    # 2B. REVERSE PRIMERS - 434/577
    # 4 primers for each, same plate layout

    for i in range(2):
        if i == 0:
            row = 'B'                             # first time through loop: 434 region
        else:
            row = 'C'                             # second time through loop: 577 region

        list = []                                           # 469.R.1 - first primer
        for j in range(6):                                  # j+96 = start at column 7 instead of column 1
            for k in range(2):                              
                list.append( 96+(j*16)    + (k*8) + (i*96))   # row A/I. i multiplier: move to column 13 (16*6) for 577 region
                list.append((96+(j*16)+3) + (k*8) + (i*96))   # row D/L
        p20.pick_up_tip()
        p20.distribute(
            volume,
            revprimers[row+'1'],                  # first primer is in first slot of the row
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never',
            touch_tip = True
        )
        p20.drop_tip()

        list = []                                 # 460.R.2 - second primer
        for j in range(6):
            for k in range(2):
                list.append((96+(j*16)+1) + (k*8) + (i*96))   # row B/J
        p20.pick_up_tip()
        p20.distribute(
            volume,
            revprimers[row+'2'],                  
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never',
            touch_tip = True
        )
        p20.drop_tip()

        list = []                                 # 469.R.1.Ad2 - third primer
        for j in range(6):
            for k in range(2):
                list.append((96+(j*16)+2) + (k*8) + (i*96))   # row C/K
                list.append((96+(j*16)+4) + (k*8) + (i*96))   # row E/M
                list.append((96+(j*16)+6) + (k*8) + (i*96))   # row G/O
        p20.pick_up_tip()
        p20.distribute(
            volume,
            revprimers[row+'3'],                  
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never',
            touch_tip = True
        )
        p20.drop_tip()

        list = []                                 # 469.R.1.Ad1 - fourth primer
        for j in range(6):
            for k in range(2):
                list.append((96+(j*16)+5) + (k*8) + (i*96))   # row F/N
        p20.pick_up_tip()
        p20.distribute(
            volume,
            revprimers[row+'4'],                  
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never',
            touch_tip = True
        )
        p20.drop_tip()
   
    ########################################################################################
    ########################################################################################
    # 3A. PROBES - 422/586
    # 6 primer conditions

    for i in range(2):                                  # 422 or 586
        if i == 0:
            row = 'A'
        else:
            row = 'D'
        for h in range(2):                              # short or long probe within each region
            list = []
            for k in range(3):
                j = 0
                while j < 14:                                    # wells 0-13 - equivalent to rows A-N
                    list.append(j + (k*16) + (h*48) + (i*288))   # j = row, k*16 = column, h*48 = which probe, i*288 = 422 or 586 section of plate
                    j += 1
                    if j == 6:  
                        j = 8                           # skip rows G and H
            list.sort()
            p20.pick_up_tip()
            p20.distribute(
                volume,
                probes[row+str(h+1)],
                [plate.wells()[wellIndex] for wellIndex in list],
                new_tip = 'never',
                touch_tip = True
            )

    ########################################################################################
    ########################################################################################
    # 3B. PROBES - 434/577
    # 7 primer conditions

    for i in range(2):                                  # 434 or 577
        if i == 0:
            row = 'B'
        else:
            row = 'C'
        for h in range(2):                              # short or long probe within each region
            list = []
            for k in range(3):
                j = 0
                while j < 15:                                         # wells 0-14 - equivalent to rows A-N
                    list.append((j+96) + (k*16) + (h*48) + (i*288))   # j+96 = row [start in col 7], k*16 = column, h*48 = which probe, i*96 = 434 or 577 section of plate
                    j += 1
                    if j == 7:  
                        j = 8                           # skip row H
            list.sort()
            p20.pick_up_tip()
            p20.distribute(
                volume,
                probes[row+str(h+1)],
                [plate.wells()[wellIndex] for wellIndex in list],
                new_tip = 'never',
                touch_tip = True
            )
    
    protocol.home()