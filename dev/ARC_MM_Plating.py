# Assay Recipe Checkpoint [ARC] - Mastermix Plating
# Updated 2023-06-22
# Author: OP13 LL

from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'ARC | MM Plating',
    'author': 'OP13 LL',
    'description': '''Plates master mix for ARCs [all wells except C9-C12] | 
                        Place completed 2x mastermix in slot A1 of a tube rack.'''
}

def run(protocol: protocol_api.ProtocolContext):

    # 0. Initialization
    
    number_of_plates = 2
    volume = 10
    
    protocol.home()

    p300tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 6, 'p300 Tips')
    
    plateDict = {}
    for i in range(1, number_of_plates):
        plateDict[str(i)] = protocol.load_labware('thermo_96_well_endura_0.1ml', i, 'Plate '+str(i))

    if number_of_plates > 1:
        rack = protocol.load_labware('usascientific_15_tuberack_5000ul', 4, 'MM: Plates > 1')
    else:
        rack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 4, 'MM: Plates = 1')

    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300tips])



    # 1. Adding mastermix to all wells

    list = []

    for i in range(96):
        list.append(i)

    ARC_wells = [num for num in list if (num % 8 != 2) or (num < 64)]  # remove wells C9-C12 from list: #66, 74, 82, and 90

    for i in range(1, number_of_plates):

        p300.distribute(
            volume,
            rack['A1'],
            [plateDict[str(i)].wells()[wellIndex] for wellIndex in ARC_wells],
            disposal_volume = 10
        )

