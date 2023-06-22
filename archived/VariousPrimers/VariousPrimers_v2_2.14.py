# Various Primers | Variation on Primer Selection Protocol
# Updated 2023-04-24
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
    'apiLevel': '2.14',
    'protocolName': '434/577 Various Probes v2',
    'author': 'OP13 LL',
    'description': 'For use in 7B10 robot.'
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
    primers = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 1, 'Primers')
    probes = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 6, 'Probes')
    plate = protocol.load_labware('appliedbiosystemsmicroamp_384_wellplate_40ul', 2)

    # pipette initialization/setup
    p20 = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[p20tips])

   # liquid definitions - to create layout map with labels/colors
    fwd434 = protocol.define_liquid(
            '434 Forward Primers',
            'Tubes loaded [left to right] in the order they are used in the protocol: 385.F.2, 385.F.2.Ad1, 403.F.1.',
            '#0700c4'
    )

    rev434 = protocol.define_liquid(
            '434 Reverse Primers',
            'Tubes loaded [left to right] in the order they are used in the protocol: 479.R.1, 460.R.2, 469.R.2.Ad1, 479.R.1.Ad1.',
            '#00a3ff'
    )
    
    probe434 = protocol.define_liquid(
        '434 Probes',
        'Tubes loaded [left to right] in the order they are used in the protocol: 434.12.F.1, 434.12.F.2, 434.12.F.3, 434.13.F.1, 434.13.F.2, 434.14.F.1.',
        '#00ccff'
    )

    fwd577 = protocol.define_liquid(
            '577 Forward Primers',
            'Tubes loaded [left to right] in the order they are used in the protocol: 542.F.1, 542.F.1.ADRd1, 548.F.2.L1, 530.F.1, 530.F.1.ADRd1, 545.F.2.L1.',
            '#c61a09'
    )

    rev577 = protocol.define_liquid(
            '577 Reverse Primers',
            'Tubes loaded [left to right] in the order they are used in the protocol: 626.R.1, 626.R.1.ADRd1, 605.R.1.L1, 602.R.1.L1, 611.R.1, 611.R.1.ADRd1.',
            '#ff6242'
    )
    
    probe577 = protocol.define_liquid(
        '577 Probes',
        'Tubes loaded [top left to bottom right, by row] in the order they are used in the protocol: 577.11.F.1, 577.12.F.1, 577.12.F.2, 577.13.F.1, 577.13.F.2, 577.14.F.1, 577.14.F.2, 577.15.F.1.',
        '#ed3419'
    )

    for i in range(6):
        primers['A'+str(i+1)].load_liquid(fwd577, 120)
        primers['B'+str(i+1)].load_liquid(rev577, 120)
        probes['C'+str(i+1)].load_liquid(probe434, 100)

    for i in range(3):
        primers['C'+str(i+1)].load_liquid(fwd434, 120)

    for i in range(4):
        primers['D'+str(i+1)].load_liquid(rev434, 120)
        probes['A'+str(i+1)].load_liquid(probe577, 100)
        probes['B'+str(i+1)].load_liquid(probe577, 100)

    ########################################################################################
    ########################################################################################
    # 1A. FORWARD PRIMERS - 577
    # See plate layout for more details

    # 542.F.1, 542.F.1.Ad1
    for i in range(2):                                  # 542.F.1 and 542.F.1.Ad1 follow a similar plate pattern, so can be distributed within same loop
        list = []
        for j in range(8):                              # 8 wells per column
            list.append(j+16*i)                         # column 1. i multiplier: moves right by 1 column for 542.F.1.Ad1
            list.append((j+96)+(16*i))                  # column 7
            list.append((j+144)+(16*i))                 # column 10
            list.append((j+240)+(16*i))                 # column 16
            list.append((j+288)+(16*i))                 # column 19
            list.append((j+336)+(16*i))                 # column 22
        list.sort()                                     # put wells in ascending order for simpler pipetting
        p20.pick_up_tip()
        p20.distribute(
            volume,
            primers['A'+str(i+1)],                      # tubes 1 and 2 in row A
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never'
        )
        p20.drop_tip()

    # 548.F.2.L1
    list = []
    for j in range(8):
        list.append(j+32)                               # column 3
        list.append(j+128)                              # column 9
    list.sort()
    p20.pick_up_tip()
    p20.distribute(
        volume,
        primers['A3'],
        [plate.wells()[wellIndex] for wellIndex in list],
         new_tip = 'never'
        )
    p20.drop_tip()

    # 530.F.1, 530.F.1.Ad1
    for i in range(2):                                  # 530.F.1 and 530.F.1.Ad1 follow a similar plate pattern, so can be distributed within same loop
        list = []
        for j in range(8):                              # 8 wells per column
            list.append((j+48)+(16*i))                  # column 4. i multiplier: moves right by 1 column for 530.F.1.Ad1
            list.append((j+192)+(16*i))                 # column 13
        list.sort()                                     
        p20.pick_up_tip()
        p20.distribute(
            volume,
            primers['A'+str(i+3)],                      # tubes 3 and 4 in row A
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never'
        )
        p20.drop_tip()

    # 545.F.2.L1
    list = []
    for j in range(8):
        list.append(j+80)                               # column 6
        list.append(j+176)                              # column 12
        list.append(j+224)                              # column 15
        list.append(j+272)                              # column 18
        list.append(j+320)                              # column 21
        list.append(j+368)                              # column 24
    list.sort()
    p20.pick_up_tip()
    p20.distribute(
        volume,
        primers['A6'],
        [plate.wells()[wellIndex] for wellIndex in list],
         new_tip = 'never'
        )
    p20.drop_tip()

    ########################################################################################
    ########################################################################################
    # 1B. FORWARD PRIMERS - 434
    # See plate layout for more details

    for i in range(3):                                  # all 3 primers follow a similar plate pattern, so can be distributed within same loop
        list = []
        for j in range(8):                              # 8 wells per column
            list.append((j+8)+(16*i))                   # column 1, bottom half of plate. i multiplier: moves right by 1 column for each primer
            list.append((j+56)+(16*i))                  # column 4
            list.append((j+104)+(16*i))                 # column 7
            list.append((j+152)+(16*i))                 # column 10
            list.append((j+200)+(16*i))                 # column 13
            list.append((j+248)+(16*i))                 # column 16
        list.sort()                                     
        p20.pick_up_tip()
        p20.distribute(
            volume,
            primers['C'+str(i+1)],                      # tubes 1-3 in row C
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never'
        )
        p20.drop_tip()

    ########################################################################################
    ########################################################################################
    # 2A. REVERSE PRIMERS - 577
    # See plate layout for more details.

    # first, adjust dispense height (in mm) - don't touch forward primers in wells
    p20.well_bottom_clearance.dispense = reverseTipHeight

    # 626.R.1, 626.R.1.Ad1
    for i in range(2):                                  # 626.R.1 and 626.R.1.Ad1 follow a similar plate pattern, so can be distributed within same loop
        list = []
        for j in range(8):                              # 8 wells per column
            list.append(j+16*i)                         # column 1. i multiplier: moves right by 1 column for 626.R.1.Ad1
            list.append((j+48)+(16*i))                  # column 4
            list.append((j+96)+(16*i))                  # column 7
            list.append((j+144)+(16*i))                 # column 10
        list.sort()                                     
        p20.pick_up_tip()
        p20.distribute(
            volume,
            primers['B'+str(i+1)],                      # tubes 1 and 2 in row B
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never',
            touch_tip = True
        )
        p20.drop_tip()

    # 605.R.1.L1
    list = []
    for j in range(8):
        list.append(j+32)                               # column 3
        list.append(j+128)                              # column 9
        list.append(j+368)                              # column 24
    list.sort()
    p20.pick_up_tip()
    p20.distribute(
        volume,
        primers['B3'],
        [plate.wells()[wellIndex] for wellIndex in list],
         new_tip = 'never',
         touch_tip = True
        )
    p20.drop_tip()

    # 602.R.1.L1
    list = []
    for j in range(8):
        list.append(j+80)                               # column 6
        list.append(j+176)                              # column 12
        list.append(j+224)                              # column 15
        list.append(j+272)                              # column 18
        list.append(j+320)                              # column 21
    list.sort()
    p20.pick_up_tip()
    p20.distribute(
        volume,
        primers['B4'],
        [plate.wells()[wellIndex] for wellIndex in list],
         new_tip = 'never',
         touch_tip = True
        )
    p20.drop_tip()

    # 611.R.1, 611.R.1.Ad1
    for i in range(2):                                  # 611.R.1 and 611.R.1.Ad1 follow a similar plate pattern, so can be distributed within same loop
        list = []
        for j in range(8):                              # 8 wells per column
            list.append((j+192)+(16*i))                 # column 13. i multiplier: moves right by 1 column for 611.R.1.Ad1
            list.append((j+240)+(16*i))                 # column 16
            list.append((j+288)+(16*i))                 # column 19
            list.append((j+336)+(16*i))                 # column 22
        list.sort()                                     
        p20.pick_up_tip()
        p20.distribute(
            volume,
            primers['B'+str(i+4)],                      # tubes 5 and 6 in row B
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never',
            touch_tip = True
        )
        p20.drop_tip()
   
    ########################################################################################
    ########################################################################################
    # 2B. REVERSE PRIMERS - 434
    # See plate layout for more details.
   
    # 479.R.1, 460.R.2
    for i in range(2):                                  # 479.R.1 and 460.R.2 follow a similar plate pattern, so can be distributed within same loop
        list = []
        for j in range(8):                              # 8 wells per column
            list.append((j+8)+(32*i))                   # column 1, bottom half of plate. i multiplier: moves right by 2 columns for 460.R.2
            list.append((j+56)+(32*i))                  # column 4
            list.append((j+104)+(32*i))                 # column 7
            list.append((j+152)+(32*i))                 # column 10
            list.append((j+200)+(32*i))                 # column 13
            list.append((j+248)+(32*i))                 # column 16
        list.sort()                                     
        p20.pick_up_tip()
        p20.distribute(
            volume,
            primers['D'+str(i+1)],                      # tubes 1-2 in row D
            [plate.wells()[wellIndex] for wellIndex in list],
            new_tip = 'never',
            touch_tip = True
        )
        p20.drop_tip()

#######################################
###########################################
###########################################
###########################################
    # 469.R.2.Ad1
    list = []
    for j in range(8):                              # 8 wells per column
        list.append((j+8)+(32*i))                   # column 2, bottom half of plate
        list.append((j+56)+(32*i))                  # column 4
        list.append((j+104)+(32*i))                 # column 7
        list.append((j+152)+(32*i))                 # column 10
        list.append((j+200)+(32*i))                 # column 13
        list.append((j+248)+(32*i))                 # column 16
    list.sort()                                     
    p20.pick_up_tip()
    p20.distribute(
        volume,
        primers['D'+str(i+1)],                      # tubes 1-2 in row D
        [plate.wells()[wellIndex] for wellIndex in list],
        new_tip = 'never',
        touch_tip = True
    )
    p20.drop_tip()


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