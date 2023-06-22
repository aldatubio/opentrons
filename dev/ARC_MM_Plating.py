# Assay Recipe Checkpoint [ARC] - Mastermix Plating
# Updated 2023-06-22
# Author: OP13 LL

from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'ARC | MM Plating',
    'author': 'OP13 LL',
    'description': '''Plates master mix [8 replicates]  for ARCs. | 
                        Place completed 2x mastermix in slot A1 of a tube rack.'''
}

def run(protocol: protocol_api.ProtocolContext):

    # 0. Initialization
    
    number_of_plates = 1
    volume = 10
    
    protocol.home()

    p300tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3, 'Tip Rack')
    plate = protocol.load_labware('appliedbiosystemsmicroamp_384_wellplate_40ul', 2, 'Plate')
    if number_of_plates > 1:
        rack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 4, 'Plates > 1')
    else:
        rack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 4, 'Plates = 1')

    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300tips])


    # 1. Pipetting master mixes 1-9

    tube_number = 0

    for section_rows in range(3):                       # rows A-E, F-J, or K-O
        for section_columns in range(3):                # columns 1-8, 9-16, or 17-24

            tube_number += 1
            list = []

            for no_of_cols in range(8):                # 12 columns per master mix
                for wells_in_column in range(5):        # 5 wells per column
                
                    list.append(
                        section_rows*5      +
                        section_columns*128 +
                        no_of_cols*16       +
                        wells_in_column
                    )
            
            p300.pick_up_tip()
            
            if tube_number <= 6:
                p300.distribute(
                    volume,
                    rack['A'+str(tube_number)],
                    [plate.wells()[wellIndex] for wellIndex in list],
                    new_tip = 'never',
                    disposal_volume = 10
                )

            else:
                p300.distribute(
                    volume,
                    rack['B'+str(tube_number - 6)],
                    [plate.wells()[wellIndex] for wellIndex in list],
                    new_tip = 'never',
                    disposal_volume = 10
                )

            p300.drop_tip()
