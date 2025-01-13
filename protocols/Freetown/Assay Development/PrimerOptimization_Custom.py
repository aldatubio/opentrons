# Primer Optimization - Customizable Tube Types
# Updated 2025-01-13
# Author: OP13 LL
#
# Purpose: Prepare dilution series of one forward and one reverse primer,
# in order to optimize the pair's sensitivity and specificity.
#
# Duration: 7.5 min
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
#     1. 5mL screw-cap tube of water in rack (located in slot A5)
#     2. 1.5mL snap-cap tubes in rack, as follows:
#         A1: forward primer (250 µL)
#         B1: reverse primer (250 µL)
#         A2-D5: empty tubes, to be filled (matching descriptions/names on Labguru)
#         (Alternatively, strip tubes on a 96-well plate rack can be used;
#          layout is similar, see Opentrons visualization for details)
#     3. 200µL filter tips (uses 12 tips)



from opentrons import protocol_api

metadata = {
    'apiLevel': '2.20',
    'protocolName': 'Primer Optimization | Customizable',
    'author': 'OP13 LL',
    'description': '''Performs dilutions for primer optimization.
                    Options to customize tube type and number of plates prepared.'''
}


requirements = {
    'robotType': 'OT-2'
}


def add_parameters(parameters: protocol_api.Parameters):

    parameters.add_str(
        variable_name='tube',
        display_name='Tube type',
        choices=[
            {'display_name': '1.5 mL Snap-Cap', 'value': 'opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap'},
            {'display_name': '0.2 mL Flex-Free Strip', 'value': 'abs_usasci_96well_200ul'}
        ],
        default='opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap'
    )

    parameters.add_int(
        variable_name='volume',
        display_name='Volume',
        description='Volume of each 4x primer mix prepared. >80 µL may result in Opentrons cross-contamination.',
        default=1,
        choices=[
            {'display_name': '40 µL (one plate)', 'value': 1},
            {'display_name': '80 µL (two plates)', 'value': 2},
            {'display_name': '120 µL (three plates - 1.5 mL tubes)', 'value': 3},
            {'display_name': '160 µL (four plates - 1.5 mL tubes)', 'value': 4}
        ]
    )


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
    p = 1 #protocol.params.volume
    param_tubes = 'abs_usasci_96well_200ul' #protocol.params.tubes

    # deck setup
    p300tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
    tubes = protocol.load_labware(param_tubes, 2)
    # custom 5mL tube definition
    water = protocol.load_labware('usascientific_15_tuberack_5000ul', 1)

    # pipette initialization
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300tips])

    # tube initialization
    if param_tubes == 'abs_usasci_96well_200ul': #strip tubes
        wells = [
                ['A2', 'B2', 'C2', 'D2'],
                ['A5', 'B5', 'C5', 'D5'],
                ['A8', 'B8', 'C8', 'D8'],
                ['A11', 'B11', 'C11', 'D11']
            ]
        lower_conc_loc = 'F1'
        higher_conc_loc = 'G1'
        
    else: #1.5mL tubes
        wells = [
            ['A2', 'B2', 'C2', 'D2'],
            ['A3', 'B3', 'C3', 'D3'],
            ['A4', 'B4', 'C4', 'D4'],
            ['A5', 'B5', 'C5', 'D5']
        ]
        lower_conc_loc = 'A1'
        higher_conc_loc = 'B1'


    ### Visualization of deck layout - API 2.14 and above only!
    ### To use protocol simulator, downgrade this protocol to 2.13 and comment out this section
    
    # ************************************
    higher_primer_viz = protocol.define_liquid(
        '1000 µM primer',
        '#44f'
    )

    lower_primer_viz = protocol.define_liquid(
        '500 µM primer',
        '#f44'
    )

    empty_viz = protocol.define_liquid(
        'Tubes to be filled',
        '#777'
    )

    tubes.wells[lower_conc_loc].load_liquid(lower_primer_viz, 250*p)
    tubes.wells[higher_conc_loc].load_liquid(higher_primer_viz, 250*p)
    wells_to_plate_viz = sum(wells, []) #flatten list
    
    for well in wells_to_plate_viz:
        tubes.wells()[well].load_liquid(
            empty_viz,
            0
        )
    ### **********************************
    

    #################################################
    ### 0. Adding water to tubes                  ###
    #################################################

    # add water of appropriate volume to each tube
    # 0, 20, 30, 36 µL to A2-A5, respectively
    to_fill = [wells[i][0] for i in range(1,4)]

    p300.pick_up_tip()
    p300.distribute(
        [20*p, 30*p, 36*p],
        water['A5'],
        [tubes.wells_by_name()[tube_name] for tube_name in to_fill],
        disposal_volume = 10,    # default excess is 20 µL (10% of pipette max) which seems wasteful
        new_tip = 'never'
    )

    # also add water to tubes such that:
    # row B tubes = 10 µL
    # row C tubes = 20 µL
    # row D tubes = 30 µL
    to_fill = []
    for i in range(1,4):
        interior_list = []
        interior_list = [wells[j][i] for j in range(1,4)] #get nested list of wells by column
        to_fill.append(interior_list)
    
    for i in range(3):              # 3 rows: B, C, D
        p300.distribute(
            ((i*10)+10)*p,              # starting with 10µL, add 10µL for every loop iteration
            water['A5'],
            [tubes.wells_by_name()[tube_name] for tube_name in to_fill[i]],
            disposal_volume = 10,
            new_tip = 'never'       # one tip for all water dispenses
        )
    p300.drop_tip()


    #################################################
    ### 1. Variable forward primer concentrations ###
    #################################################

    # complex pipetting commands are capable of handling lists -
    # can pass a list of volumes (in µL) and a corresponding list of tubes

    # add forward primer of appropriate volume to each tube
    # 60, 40, 30, 24 µL to A2-A5, respectively
    to_fill = [wells[i][0] for i in range(4)]
    p300.distribute(
        [60*p, 40*p, 30*p, 24*p],
        tubes[lower_conc_loc],
        [tubes.wells_by_name()[tube_name].bottom(10) for tube_name in to_fill],
        disposal_volume = 10
    )

    # add 60 µL reverse primer to A2-A5 and mix
    for i in range(4):
        p300.transfer(
            60*p,
            tubes[higher_conc_loc],
            tubes.wells_by_name()[wells[i][0]],
            mix_after = (4, 80*p)
        )


    ################################
    ### 2. Primer pair dilutions ###
    ################################

    # add primer mix to tubes such that:
    # row B tubes = 30 µL
    # row C tubes = 20 µL
    # row D tubes = 10 µL
    # where tubes B, C, and D in a column are all dilutions of tube A in the same column

    to_fill = []
    wells_temp = wells
    for i in range(4):
        wells_temp[i].pop(0)
        to_fill.append(wells_temp[i]) #to_fill is now a list of lists: [[B2, C2, D2], [B3, C3, D3],...]

    for i in range(4):              # 4 columns: 2, 3, 4, 5
        p300.distribute(
            [30*p, 20*p, 10*p],
            tubes[wells[i][0]],     #A2, A3, A4, or A5
            [tubes.wells_by_name()[tube_name].top(-15) for tube_name in to_fill[i]], #B2/C2/D2, B3/C3/D3...
            disposal_volume = 10,
            touch_tip = True
        )

    protocol.home()