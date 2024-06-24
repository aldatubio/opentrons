'''
Troubleshooting
Home Gantry
Updated 2024-06-24
Author: OP13 LL


INSTRUCTIONS FOR USE

This protocol homes the gantry as a troubleshooting measure for homing fail errors. This protocol can also be used to ensure that hard limit errors have been resolved.

'''

from opentrons import protocol_api

metadata = {
    'apiLevel': '2.18',
    'protocolName': 'Troubleshooting | Home Gantry',
    'author': 'OP13 LL',
    'description': '''This protocol homes the gantry as a troubleshooting measure for homing fail errors. This protocol can also be used to ensure that hard limit errors have been resolved. 
                    '''
}

requirements = {
    'robotType': 'OT-2'
}

def add_parameters(parameters: protocol_api.Parameters):
    parameters.add_str(
        variable_name = "left_pipettor",
        display_name = "Left Pipette",
        description = "Pipette installed on left mount.",
        choices = [
            {"display_name": "1-Channel 20 µL", "value": "p20_single_gen2"},
            {"display_name": "1-Channel 300 µL", "value": "p300_single_gen2"},
            {"display_name": "1-Channel 1000 µL", "value": "p1000_single_gen2"}
        ],
        default = "p1000_single_gen2"
    )
    parameters.add_str(
        variable_name = "right_pipettor",
        display_name = "Right Pipette",
        description = "Pipette installed on right mount.",
        choices = [
            {"display_name": "1-Channel 20 µL", "value": "p20_single_gen2"},
            {"display_name": "1-Channel 300 µL", "value": "p300_single_gen2"},
            {"display_name": "1-Channel 1000 µL", "value": "p1000_single_gen2"}
        ],
        default = "p300_single_gen2"
    )
    parameters.add_bool(
        variable_name = "pipetting_simulate",
        display_name = "Simulate Pipetting",
        # description can only be 100 characters
        description = "Mock aspirate / dispense for each pipettor.",
        default = False
    )



def run(protocol: protocol_api.ProtocolContext):

    protocol.home()

    ###
    ### Initialization - choose protocol type, pipettes installed
    ###

    if protocol.params.pipetting_simulate is True:
        diluent = protocol.load_labware('usascientific_15_tuberack_5000ul', 1)
        diluent_location = 'A5'

    if protocol.params.left_pipettor == "p20_single_gen2":
        left_tips = protocol.load_labware('opentrons_96_filtertiprack_20ul', 2)
    elif protocol.params.left_pipettor == "p300_single_gen2":
        left_tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 2)
    elif protocol.params.left_pipettor == "p1000_single_gen2":
        left_tips = protocol.load_labware('opentrons_96_filtertiprack_1000ul', 2)
    
    left_pipette = protocol.load_instrument(protocol.params.left_pipettor, 'left', tip_racks=[left_tips])

    if protocol.params.right_pipettor == "p20_single_gen2":
        right_tips = protocol.load_labware('opentrons_96_filtertiprack_20ul', 3)
    elif protocol.params.right_pipettor == "p300_single_gen2":
        right_tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
    elif protocol.params.right_pipettor == "p1000_single_gen2":
        right_tips = protocol.load_labware('opentrons_96_filtertiprack_1000ul', 3)
    
    right_pipette = protocol.load_instrument(protocol.params.left_pipettor, 'right', tip_racks=[right_tips])

    ###
    ### 1. Fake transfer diluent
    ###

    if protocol.params.pipetting_simulate is True:
        left_pipette.transfer(
            20,
            diluent[diluent_location],
            diluent[diluent_location],
            trash = False
        )
        right_pipette.transfer(
            20,
            diluent[diluent_location],
            diluent[diluent_location],
            trash = False
        )

    protocol.home()