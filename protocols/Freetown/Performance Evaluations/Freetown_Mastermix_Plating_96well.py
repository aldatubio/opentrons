# Project Freetown
# Reportable Range - Mastermix Plating
# Updated 2024-05-24
# Author: OP13 LL

from opentrons import protocol_api

metadata = {
    'apiLevel': '2.18',
    'protocolName': 'Freetown | Mastermix Plating for Reportable Range',
    'author': 'OP13 LL',
    'description': '''Plates master mix for reportable range experiments [all wells of a 96-well plate]. | 
                        Place completed 2x mastermix in slot A1 of a tube rack [1.5mL tube for 1 plate, 5mL tube for 2+ plates].'''
}

requirements = {
    'robotType': 'OT-2'
}

def add_parameters(parameters: protocol_api.Parameters):
    
    parameters.add_int(
        variable_name = 'number_of_plates',
        display_name = 'Number of plates',
        description = 'Number of 96-well plates to prepare; all wells of each plate will be filled.',
        default = 1,
        minimum = 1,
        maximum = 4,
    )

    parameters.add_float(
        variable_name = 'volume',
        display_name = 'Volume per well',
        description = 'Volume of liquid added to each well.',
        default = 10.0,
        minimum = 10.0,
        maximum = 20.0,
        unit = 'µL'
    )

def run(protocol: protocol_api.ProtocolContext):

    # 0. Initialization
    
    number_of_plates = protocol.params.number_of_plates
    volume = protocol.params.volume
    
    protocol.home()

    p300tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 6, 'p300 Tips')
    
    plateDict = {}
    for i in range(number_of_plates):
        plateDict[str(i+1)] = protocol.load_labware('thermo_96_well_endura_0.1ml', i+1, 'Plate '+str(i+1))

    if number_of_plates > 1:
        rack = protocol.load_labware('usascientific_15_tuberack_5000ul', 5, 'MM: Plates > 1')
    else:
        rack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 5, 'MM: Plates = 1')

    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300tips])



    # 1. Adding mastermix to all wells

    list = []

    for i in range(96):
        list.append(i)

    #ARC_wells = [num for num in list if (num % 8 != 2) or (num < 64)]  # remove wells C9-C12 from list: #66, 74, 82, and 90

    for i in range(number_of_plates):

        p300.distribute(
            volume,
            rack['A1'],
            [plateDict[str(i+1)].wells()[wellIndex] for wellIndex in list],
            disposal_volume = 10,
            blow_out = True,
            blowout_location = "source well"
        )

    protocol.home()
