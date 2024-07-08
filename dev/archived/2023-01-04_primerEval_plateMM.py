# # Primer Evaluation - Plating Master Mix
# **Updated 2023-01-03** <br>
# **Author: OP13 LL**
# 
# **Purpose:** Fill the top half of a 384-well plate with master mix containing viral template, and fill the bottom half with negative control master mix.<br>
# **Duration:** 20 min
# 
# **Execution:** This script fills a 384-well plate, already containing 3µL primers, as follows:
#  - **STEP 3: Master mix (20 min)**
#      - Rows A-H: master mix with target template
#      - Rows I-P: master mix with negative control
#      
# **Reaction (total 20uL per well):**
#  - 1.5µL 13X forward primer
#  - 1.5µL 13X reverse primer
#  - 17µL master mix
#  
# **Deck setup:**
#  - **1:** 15-count 5mL screw cap tube rack, with tubes as follows:
#      - tube A5: master mix with target template (3.4mL)
#      - tube C5: negative control master mix (3.4mL)
#  - **2:** Applied Biosystems 384-well MicroAmp plate
#  - **4:** 96-count 300µL tip rack (protocol uses 2 tips)
#
# ![2022-11-22_8x8primerScreen_decksetup.png](attachment:2022-11-22_8x8primerScreen_decksetup.png)


from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Primer Eval - Mastermix Plating (updated 2023-01-04)',
    'author': 'OP13 LL',
    'description': '''For use in 8B04 robot.
                        LIQUID SETUP:
                        5mL tubes: tube A5 = master mix with target template (3.4mL), tube C5 = negative control master mix (3.4mL).
                        '''
}

def run(protocol: protocol_api.ProtocolContext):

    # 0. INITIALIZATION

    # user-defined variables - edit as necessary
    # volume of master mix to pipette (uL)
    mastermixVolume = 17
    # height of tip above bottom of well when dispensing (mm)
    mastermixTipHeight = 8

    protocol.home()

    # deck setup
    # attribute = protocol.load_labware('name', position)
    p300tips = protocol.load_labware('opentrons_96_tiprack_300uL', 4)
    plate = protocol.load_labware('appliedbiosystemsmicroamp_384_wellplate_40ul', 2)

    # to use 5mL tubes, use our lab's custom definition:
    mastermixes = protocol.load_labware('usascientific_15_tuberack_5000ul', 1)

    # to use 15mL tubes, use the Nest definition:
    # Opentrons doesn't have a labware definition for the Nunc / ThermoFisher 15mL tubes we use;
    # however, NEST tube technical specs are very close to the Nunc tubes, so we'll use this definition
    # mastermixes = protocol.load_labware('opentrons_15_tuberack_nest_15ml_conical', 1)

    # pipette initialization/setup
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300tips])



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
    #protocol.comment('Negative control master mix plating complete. Add tube of master mix with template to rack.')
    


    # 3b. MASTER MIX | 10 min

    # fill rows A-H with master mix + template (10 min)

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

