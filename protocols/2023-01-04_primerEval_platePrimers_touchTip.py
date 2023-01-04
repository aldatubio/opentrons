# # Primer Evaluation - Plating Primers
# **Updated 2023-01-03** <br>
# **Author: OP13 LL**
# 
# **Purpose:** Plate 64 primer pairs in triplicate on a 384-well plate. <br>
# **Duration:** 35 min
# 
# **Execution:** This script fills a 384-well plate as follows:
#  - **STEP 1: Forward primers (15 min)**
#      - Rows A & I: forward primer 1
#      - Rows B & J: forward primer 2
#      - ...
#      - Rows H & P: forward primer 8
#  - **STEP 2: Reverse primers (20 min)**
#      - Columns 1-3: reverse primer 1
#      - Columns 4-6: reverse primer 2
#      - ...
#      - Columns 22-24: reverse primer 8
#      
# **Reaction (total 3uL per well):**
#  - 1.5µL 13X forward primer
#  - 1.5µL 13X reverse primer
#  
# **Deck setup:**
#  - **2:** Applied Biosystems 384-well MicroAmp plate
#  - **5:** 24-count 1.5mL snap cap tube rack, with tubes as follows:
#      - tubes A1-4, B1-4: 13X forward primers (100µL each)
#      - tubes C1-4, D1-4: 13X reverse primers (100µL each)
#  - **6:** 96-count 20µL tip rack (protocol uses 16 tips)
#
# ![2022-11-22_8x8primerScreen_decksetup.png](attachment:2022-11-22_8x8primerScreen_decksetup.png)


from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Primer Eval - Primer Plating with Extra Tip Touch (updated 2023-01-04)',
    'author': 'OP13 LL',
    'description': '''For use in 7B10 robot.
                        LIQUID SETUP:
                        1.5mL tubes: tubes A1-4, B1-4 = forward primers (100µL each); tubes C1-4, D1-4 = reverse primers (100µL each).
                        '''
}

def run(protocol: protocol_api.ProtocolContext):

    # 0. INITIALIZATION

    # user-defined variables - edit as necessary
    # volume of primers to pipette (uL)
    primerVolume = 1.5
    # height of tip above bottom of well when dispensing (mm)
    reversePrimerTipHeight = 4.5

    protocol.home()

    # deck setup
    # attribute = protocol.load_labware('name', position)
    p20tips = protocol.load_labware('opentrons_96_tiprack_20uL', 6)
    reservoir = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 5)
    plate = protocol.load_labware('appliedbiosystemsmicroamp_384_wellplate_40ul', 2)

    # pipette initialization/setup
    p20 = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[p20tips])


    # 1. FORWARD PRIMERS | 15 min
    # fill pairs of rows with the correct forward primers
    # rows A and I get forward primer 1, rows B and J get forward primer 2, etc.
    # use 1 tip per primer

    # tubes A1-A4: forward primers 1-4
    for i in range(4):
        p20.pick_up_tip()                           # by specifying exactly when to get a new tip (and disabling
        p20.distribute(                             # auto-new tip), robot only uses one tip per loop iteration
            primerVolume,
            reservoir['A'+str(i+1)],
            plate.rows()[i],                        # dispense into row with index i (A-D)
            new_tip = 'never'
        )
        p20.touch_tip(reservoir['A'+str(i+1)])      # touch tip within source tube
        p20.distribute(
            primerVolume,
            reservoir['A'+str(i+1)],
            plate.rows()[i+8],                      # dispense into row with index i+8 (I-L)
            new_tip = 'never'                      
        )
        p20.drop_tip()

    protocol.pause()
    protocol.comment('Primer F1-F4 plating complete. Add forward primers 5-8 in slots B1-4.')

'''
    # tubes B1-B4: forward primers 5-8
    for i in range(4):
        p20.pick_up_tip()
        p20.distribute(
            primerVolume,
            reservoir['B'+str(i+1)],
            plate.rows()[i+4],                      # dispense into row with index i+4 (E-H)
            new_tip = 'never'
        )
        p20.distribute(
            primerVolume,
            reservoir['B'+str(i+1)],
            plate.rows()[i+12],                     # dispense into row with index i+12 (M-P)
            new_tip = 'never'
        )
        p20.drop_tip()

    protocol.pause()
    protocol.comment('Forward primer plating complete. Add reverse primers 1-4 in slots C1-4.')
'''
    # 2. REVERSE PRIMERS | 20 min
    # fill trios of columns with the correct reverse primers
    # columns 1-3 get reverse primer 1, columns 4-6 get reverse primer 2, etc.
    # use 1 tip per primer

    # first, adjust dispense height (in mm) - don't touch forward primers in wells
    p20.well_bottom_clearance.dispense = reversePrimerTipHeight

    # tubes C1-C4: reverse primers 1-4
    for i in range(4):
        p20.distribute(
            primerVolume,
            reservoir['C'+str(i+1)],
            plate.columns()[3*i:3+3*i],             # columns 1-12 (indices 0-11)
            touch_tip = True
        )

    protocol.pause()
    protocol.comment('Primer R1-R4 plating complete. Add reverse primers 5-8 in slots D1-4.')
'''
    # tubes D1-D4: reverse primers 5-8
    for i in range(4):
        p20.distribute(
            primerVolume,
            reservoir['D'+str(i+1)],
            plate.columns()[12+3*i:15+3*i],         # columns 13-24 (indices 12-23)
            touch_tip = True
        )
'''
    protocol.home()

