# Lineage-Specific Primer Pools
# Updated 2023-05-30
# Author: OP13 LL
#
# Master mix tube rack layout:
# 

from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'LSP Pools | MM Plating | 12 replicates',
    'author': 'OP13 LL',
    'description': '''Plates master mix [12 replicates]  for lineage-specific primer pool evaluations. | 
                        Place completed 2x mastermixes [1-6] in slots A1-A6 of tube rack.
                        Mastermixes are added to plate: top left, top right, center left, center right, bottom left, bottom right.'''
}

def run(protocol: protocol_api.ProtocolContext):

    # 0. Initialization
    
    volume = 10
    
    protocol.home()

    p300tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3, 'Tip Rack')
    plate = protocol.load_labware('appliedbiosystemsmicroamp_384_wellplate_40ul', 2, 'Plate')
    rack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 4, 'Master Mixes')

    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300tips])


    # 1. Pipetting master mixes 1-6

    tube_number = 0

    for section_rows in range(3):                       # rows A-E, F-J, or K-O
        for section_columns in range(2):                # columns 1-12 or 13-24

            tube_number += 1
            list = []

            for no_of_cols in range(12):                # 12 columns per master mix
                for wells_in_column in range(5):        # 5 wells per column
                
                    list.append(
                        section_rows*5      +
                        section_columns*192 +
                        no_of_cols*16       +
                        wells_in_column
                    )
            
            p300.pick_up_tip()

            p300.distribute(
                volume,
                rack['A'+str(tube_number)],
                [plate.wells()[wellIndex] for wellIndex in list],
                new_tip = 'never'
            )

            p300.drop_tip()
