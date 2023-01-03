#!/usr/bin/env python
# coding: utf-8

# # 8x8 Primer Screen
# **Updated 2022-12-12** <br>
# **Author: OP13 LL**
# 
# **Purpose:** Test 64 different forward-reverse primer pairs for sensitivity (ability to amplify target template) and specificity (inability to amplify NTC). <br>
# **Duration:** 55 min
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
#  - **STEP 3: Master mix (20 min)**
#      - Rows A-H: master mix with target template
#      - Rows I-P: master mix with NTC
#      
# **Reaction (total 20uL per well):**
#  - 1.5µL 13X forward primer
#  - 1.5µL 13X reverse primer
#  - 17µL master mix
#  
# **Deck setup:**
#  - **1:** 15-count 5mL screw cap tube rack, with tubes as follows:
#      - tube A5: master mix with target template (3.6mL)
#      - tube C5: negative control master mix (3.6mL)
#  - **2:** Applied Biosystems 384-well MicroAmp plate
#  - **4:** 96-count 300µL tip rack (protocol uses 2 tips)
#  - **5:** 24-count 1.5mL snap cap tube rack, with tubes as follows:
#      - tubes A1-4, B1-4: 13X forward primers (100µL each)
#      - tubes C1-4, D1-4: 13X reverse primers (100µL each)
#  - **6:** 96-count 20µL tip rack (protocol uses 16 tips)
# 
# 
# ![2022-11-22_8x8primerScreen_decksetup.png](attachment:2022-11-22_8x8primerScreen_decksetup.png)


from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': '8x8 Primer Screen (updated 2022-12-05)',
    'author': 'OP13 LL',
    'description': '''LIQUID SETUP:
                        1.5mL tubes: tubes A1-4, B1-4 = forward primers (100µL each); tubes C1-4, D1-4 = reverse primers (100µL each).
                        5mL tubes: tube A5 = master mix with target template (3.6mL), tube C5 = negative control master mix (3.6mL).
                        '''
}

def run(protocol: protocol_api.ProtocolContext):

    # In[ ]:

    # 0. INITIALIZATION

    # user-defined variables - edit as necessary
    # volume of primers and master mix to pipette (uL)
    primerVolume = 1.5
    mastermixVolume = 17
    # height of tip above bottom of well when dispensing (mm)
    reversePrimerTipHeight = 4.5
    mastermixTipHeight = 8

    '''
    import opentrons.execute
    from opentrons import types
    from opentrons import protocol_api
    import json
    protocol = opentrons.execute.get_protocol_api('2.13')
    '''
    protocol.home()

    # deck setup
    # attribute = protocol.load_labware('name', position)
    p20tips = protocol.load_labware('opentrons_96_tiprack_20uL', 6)
    p300tips = protocol.load_labware('opentrons_96_tiprack_300uL', 4)
    reservoir = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 5)
    plate = protocol.load_labware('appliedbiosystemsmicroamp_384_wellplate_40ul', 2)

    '''
    # because 5mL tubes aren't defined by Opentrons, we have to load a custom definition here
    with open('usascientific_15_tuberack_5000ul.json') as labware_file:
        labware_def = json.load(labware_file)
        mastermixes = protocol.load_labware_from_definition(labware_def, 1)
    '''
    mastermixes = protocol.load_labware('usascientific_15_tuberack_5000ul', 1)

    # pipette initialization/setup
    p20 = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[p20tips])
    p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks=[p300tips])


    # In[ ]:


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

        p20.distribute(
            primerVolume,
            reservoir['A'+str(i+1)],
            plate.rows()[i+8],                      # dispense into row with index i+8 (I-L)
            new_tip = 'never'                      
        )
        p20.drop_tip()

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


    # In[ ]:


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

    # tubes D1-D4: reverse primers 5-8
    for i in range(4):
        p20.distribute(
            primerVolume,
            reservoir['D'+str(i+1)],
            plate.columns()[12+3*i:15+3*i],         # columns 13-24 (indices 12-23)
            touch_tip = True
        )

    # Opentrons says pause() method can take a string argument and display this as a message to the user,
    # but in my experience this does not actually happen (string does not even show up in run log.)
    # Instead, use (deprecated?) comment() method to display text.
    # Comment text will show up in run log portion of app screen; can be somewhat hard to find.
    protocol.pause()
    
    # If pausing between steps 3a and 3b:
    #protocol.comment('Primer plating complete. Tap or spin down plate to mix, then add negative control master mix tube to rack.')
    
    # If no pause between steps 3a and 3b:
    protocol.comment('Primer plating complete. Tap or spin down plate to mix, then add both master mix tubes to rack.')
    
    # In[ ]:


    # 3a. MASTER MIX | 10 min

    p300.well_bottom_clearance.dispense = mastermixTipHeight

    # fill rows I-P with negative control master mix (10 min)

    # because master mix is somewhat viscous and we need additional tip-touching / pipette speed controls,
    # we can't use the API's transfer and distribute functions; instead, use building block controls
    # to gain access to additional parameters
    # example: aspirate and dispense can take rate multiplier argument (0.7 = 70% of default speed)

    p300.pick_up_tip()
    for column in range(12):                                                                  # cycle through columns (master loop)
        p300.aspirate((mastermixVolume*17 + 10), mastermixes['C5'], 0.7)                      # enough for 16 rxns + 1 extra
        p300.dispense(mastermixVolume, mastermixes['C5'], 0.7)                                # redispense extra rxn's worth
        for i in range(3):                                                                    # repeat touch tip 3 times on source
            p300.touch_tip(v_offset = -15)                                                    # specify height of touch tip
        for well in range(8):
            p300.dispense(mastermixVolume, plate.wells()[well+(column*16 + 8)], 0.7)          # cycle through wells in a column
            p300.touch_tip()                                                                  # +8 offset = bottom half of plate
        for well in range(8):                                                                 # cycle: 2 columns per master loop
            p300.dispense(mastermixVolume, plate.wells()[well+((column+12)*16 + 8)], 0.7)
            p300.touch_tip()
        p300.blow_out(mastermixes['C5'])                                                      # blow out into source well
    p300.drop_tip()

    # to re-add pause step, un-comment the next two lines,
    # and use protocol.comment() on line 181 instead of 184
    #protocol.pause()
    #protocol.comment('NTC master mix plating complete. Add tube of master mix with template to rack.')
    
    # In[ ]:


    # 3b. MASTER MIX | 10 min

    # fill rows A-H with positive control master mix (10 min)

    p300.pick_up_tip()
    for column in range(12):
        p300.aspirate((mastermixVolume*17 + 10), mastermixes['A5'], 0.7)
        p300.dispense(mastermixVolume, mastermixes['A5'], 0.7)
        for i in range(3):
            p300.touch_tip(v_offset = -15)
        for well in range(8):
            p300.dispense(mastermixVolume, plate.wells()[well+(column*16)], 0.7)
            p300.touch_tip()
        for well in range(8):
            p300.dispense(mastermixVolume, plate.wells()[well+((column+12)*16)], 0.7)
            p300.touch_tip()
        p300.blow_out(mastermixes['A5'])
    p300.drop_tip()

    protocol.home()

