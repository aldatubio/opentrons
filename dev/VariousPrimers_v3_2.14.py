# Various Primers | Variation on Primer Selection Protocol
# Updated 2023-04-25
# Author: OP13 LL
# 
# Purpose: plate primer pairs and probes on a 384-well plate
#          such that each of 6 probes is tested with 6-7 different primer pairs.
#      
# Reaction [total 6µL per well]:
#  - 2µL 10X forward primer
#  - 2µL 10X reverse primer
#  - 2µL 10X probe
#  
# Deck setup:
#  - 4, 5, 6: 24-count 1.5mL snap-cap tube rack with forward primers, reverse primers, and probes, respectively
#  - 2: Applied Biosystems 384-well MicroAmp plate
#  - 3: 96-count 20µL tip rack
#
# Note: this version of the protocol no longer includes the 586 region in columns 19-24 of the plate.


from opentrons import protocol_api

metadata = {
    'apiLevel': '2.14',
    'protocolName': '422/434/577 Various Primers v3',
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

   # liquid definitions - to create layout map with labels/colors
    fwdliquids = protocol.define_liquid(
            'Forward Primers [10x]',
            '''Each row represents a different SNP
                [row A = 422, row B = 434, row C = 577].
                Tubes loaded left to right within rows in the order they are used in the protocol.''',
            '#00f'
    )

    revliquids = protocol.define_liquid(
            'Reverse Primers [10x]',
            '''Each row represents a different SNP
                [row A = 422, row B = 434, row C = 577].
                Tubes loaded left to right within rows in the order they are used in the protocol.''',
            '#f00'
    )

    probeliquids = protocol.define_liquid(
            'Probes [10x]',
            '''Each row represents a different SNP
                [row A = 422, row B = 434, row C = 577].
                Tubes loaded left to right within rows in the order they are used in the protocol.''',
            '#0f0'
    )

    for i in range(3):
        fwdprimers['A'+str(i+1)].load_liquid(fwdliquids, 100)
        revprimers['A'+str(i+1)].load_liquid(revliquids, 100)
        for j in range(2):
            probes[str(chr(i+65))+str(j+1)].load_liquid(probeliquids, 100)

    
    for i in range(4):
        fwdprimers['B'+str(i+1)].load_liquid(fwdliquids, 100)
        fwdprimers['C'+str(i+1)].load_liquid(fwdliquids, 100)
        revprimers['B'+str(i+1)].load_liquid(revliquids, 100)
        revprimers['C'+str(i+1)].load_liquid(revliquids, 100)



    ########################################################################################
    ########################################################################################
    # 1A. FORWARD PRIMERS - 422
    # See plate layout for more details
    # 422 foward primers - 3 primers

    list = []                                           # 385.F.1 - first primer
    for j in range(6):                                  # columns 1-6 [for 422 region]
        for k in range(2):                              # top vs bottom half of plate
            list.append( (j*16)    + (k*8))   # row A/I
            list.append(((j*16)+1) + (k*8))   # row B/J. k multiplier: when k=1, move to bottom half of plate
    p20.pick_up_tip()
    p20.distribute(
        volume,
        fwdprimers['A1'],                  # first primer is in first slot of the row
        [plate.wells()[wellIndex] for wellIndex in list],
        new_tip = 'never'
    )
    p20.drop_tip()

    list = []                                 # 385.F.1.Ad2 - second primer
    for j in range(6):
        for k in range(2):
            list.append(((j*16)+2) + (k*8))   # row C/K
            list.append(((j*16)+4) + (k*8))   # row E/M
            list.append(((j*16)+5) + (k*8))   # row F/N
    p20.pick_up_tip()
    p20.distribute(
        volume,
        fwdprimers['A2'],                  
        [plate.wells()[wellIndex] for wellIndex in list],
        new_tip = 'never'
    )
    p20.drop_tip()

    list = []                                 # 385.F.1.Ad1 - third primer
    for j in range(6):
        for k in range(2):
            list.append(((j*16)+3) + (k*8))   # row D/L
    p20.pick_up_tip()
    p20.distribute(
        volume,
        fwdprimers['A3'],                  
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
    # 2A. REVERSE PRIMERS - 422
    # See plate layout for more details.

    # first, adjust dispense height (in mm) - don't touch forward primers in wells
    p20.well_bottom_clearance.dispense = reverseTipHeight

    ########
    # 422 - 3 primers
    list = []                                           # 458.R.1 - first primer
    for j in range(6):                                  # columns 1-6
        for k in range(2):                              # top vs bottom half of plate
            list.append( (j*16)    + (k*8))             # row A/I
            list.append(((j*16)+2) + (k*8))             # row C/K. k multiplier: when k=1, move to bottom half of plate
    p20.pick_up_tip()
    p20.distribute(
        volume,
        revprimers['A1'],                  # first primer is in first slot of the row
        [plate.wells()[wellIndex] for wellIndex in list],
        new_tip = 'never',
        touch_tip = True
    )
    p20.drop_tip()

    list = []                                 # 458.R.1.Ad2 - second primer
    for j in range(6):
        for k in range(2):
            list.append(((j*16)+1) + (k*8))   # row B/J
            list.append(((j*16)+3) + (k*8))   # row D/L
            list.append(((j*16)+5) + (k*8))   # row F/N
    p20.pick_up_tip()
    p20.distribute(
        volume,
        revprimers['A2'],                  
        [plate.wells()[wellIndex] for wellIndex in list],
        new_tip = 'never',
        touch_tip = True
    )
    p20.drop_tip()

    list = []                                 # 458.R.1.Ad1 - third primer
    for j in range(6):
        for k in range(2):
            list.append(((j*16)+4) + (k*8))   # row E/M
    p20.pick_up_tip()
    p20.distribute(
        volume,
        revprimers['A3'],                  
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
    # 3A. PROBES - 422
    # 6 primer conditions

    for h in range(2):                              # short or long probe
        list = []
        for k in range(3):
            j = 0
            while j < 14:                          # wells 0-13 - equivalent to rows A-N
                list.append(j + (k*16) + (h*48))   # j = row, k*16 = column, h*48 = which probe
                j += 1
                if j == 6:  
                    j = 8                           # skip rows G and H
        list.sort()
        p20.pick_up_tip()
        p20.distribute(
            volume,
            probes['A'+str(h+1)],
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never',
            touch_tip = True
        )
        p20.drop_tip()

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
                    list.append((j+96) + (k*16) + (h*48) + (i*96))   # j+96 = row [start in col 7], k*16 = column, h*48 = which probe, i*96 = 434 or 577 section of plate
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
            p20.drop_tip()
    
    protocol.home()