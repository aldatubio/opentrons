# # Primer Evaluation | Plating Primers
# **Updated 2024-10-28**
# **Author: OP13 LL**
# 
# **Purpose:** Plate n^2 primer pairs in triplicate on a 384-well plate.
# **Duration:** 35 min
# 
# **Execution:** This script fills a 384-well plate as follows:
#  - **STEP 1: Forward primers (15 min)**
#      - Rows A & n+1: forward primer 1
#      - Rows B & n+2: forward primer 2
#      - ...
#      - Rows n & n*2: forward primer n
#  - **STEP 2: Reverse primers (20 min)**
#      - Columns 1-3: reverse primer 1
#      - Columns 4-6: reverse primer 2
#      - ...
#      - Columns n*3 - (n+1)*3: reverse primer n
#      
# **Reaction (total 3uL per well):**
#  - 1.5µL 13X forward primer
#  - 1.5µL 13X reverse primer
#  
# **Deck setup:**
#  - **2:** Applied Biosystems 384-well MicroAmp plate
#  - **5:** 24-count 1.5mL snap cap tube rack, with tubes as follows:
#      - tubes A1-(n/2), B1-(n/2): 13X forward primers (100µL each)
#      - tubes C1-(n/2), D1-(n/2): 13X reverse primers (100µL each)
#  - **6:** 96-count 20µL tip rack (protocol uses 16 tips)


from opentrons import protocol_api

metadata = {
    'apiLevel': '2.20',
    'protocolName': 'Primer Evaluation | Primer Plating',
    'author': 'OP13 LL',
    'description': 'Plates custom number of primer pairs on 384-well plate in triplicate.'
}

requirements = {
    'robotType': 'OT-2'
}

def add_parameters(parameters: protocol_api.Parameters):

    parameters.add_int(
        variable_name = 'num_primers',
        display_name = 'Number of primers',
        description = 'Number of forward / reverse primers. For example, for an 8x8 grid, type "8".',
        default = 8,
        minimum = 1,
        maximum = 8
    )
    
    parameters.add_float(
        variable_name = 'primer_volume',
        display_name = 'Primer Volume',
        default = 1.5,
        minimum = 1.0,
        maximum = 20.0,
        unit = 'µL'
    )

def run(protocol: protocol_api.ProtocolContext):

    # 0. INITIALIZATION

    # user-defined variables - edit as necessary
    # volume of primers to pipette (uL)
    primer_volume = protocol.params.primer_volume
    # height of tip above bottom of well when dispensing (mm)
    reverse_primer_tip_height = 4.5
    # number of forward / reverse primers being tested
    num_primers = protocol.params.num_primers

    protocol.home()

    # deck setup
    # attribute = protocol.load_labware('name', position)
    p20tips = protocol.load_labware('opentrons_96_tiprack_20uL', 3)
    primers = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 5)
    plate = protocol.load_labware('appliedbiosystemsmicroamp_384_wellplate_40ul', 2)

    # pipette initialization/setup
    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[p20tips])


    ### Visualization of deck layout - API 2.14 and above only!
    ### To use protocol simulator, downgrade this protocol to 2.13 and comment out this section
    
    # ************************************
    f_primer_viz = protocol.define_liquid(
        'Forward primers',
        '#44f'
    )

    r_primer_viz = protocol.define_liquid(
        'Reverse primers',
        '#f44'
    )

    empty_viz = protocol.define_liquid(
        'Wells to be plated',
        '#777'
    )

    for i in range(num_primers):
        primers.wells()[i].load_liquid(
            f_primer_viz,
            (6 * num_primers * primer_volume) * 1.1 + 10 #10% excess + 10 µL
        )

    for i in range(num_primers):
        primers.wells()[i+8].load_liquid(
            r_primer_viz,
            (6 * num_primers * primer_volume) * 1.1 + 10 #10% excess + 10 µL
        )


    wells_to_plate_viz = []
    for i in range(num_primers):
        wells_to_plate_viz += list(range(i, num_primers*48, 16))                 
        wells_to_plate_viz += list(range(num_primers + i, num_primers*49, 16))
    
    for well in wells_to_plate_viz:
        plate.wells()[well].load_liquid(
            empty_viz,
            0
        )
    

    ### **********************************


    # 1. FORWARD PRIMERS | 15 min
    # fill pairs of rows with the correct forward primers

    for i in range(num_primers):
        
        wells_to_plate = []
        wells_to_plate = list(range(i, num_primers*48, 16))                 # first row: primer 1 --> row A, for columns up to 3*num_primers
        wells_to_plate += list(range(num_primers + i, num_primers*49, 16))  # second row: primer 1 --> row num_primers, for columns up to 3*num_primers

        p20.distribute(
            primer_volume,
            primers.wells()[i],
            [plate.wells()[well] for well in wells_to_plate]
        )


    # 2. REVERSE PRIMERS | 20 min
    # fill trios of columns with the correct reverse primers
    # columns 1-3 get reverse primer 1, columns 4-6 get reverse primer 2, etc.

    # first, adjust dispense height (in mm) - don't touch forward primers in wells
    p20.well_bottom_clearance.dispense = reverse_primer_tip_height

    for i in range(num_primers):

        wells_to_plate = []
        wells_to_plate = list(range(i*48, i*48 + 2*num_primers))                # first column: primer 1 --> column 1, for rows up to 2*num_primers
        wells_to_plate += list(range(i*48 + 16, i*48 + 2*num_primers + 16))     # second column: primer 1 --> column 2, for rows up to 2*num_primers
        wells_to_plate += list(range(i*48 + 32, i*48 + 2*num_primers + 32))     # third column: primer 1 --> column 3, for rows up to 2*num_primers

        p20.distribute(
            primer_volume,
            primers.wells()[i + 8],
            [plate.wells()[well] for well in wells_to_plate],
            touch_tip = True
        )

    protocol.home()

