# Lineage-Specific Primer Pools
# Updated 2023-05-17
# Author: OP13 LL
#
# Master mix tube rack layout:
# 

from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Lineage-Specific Primer Pools | MM Plating',
    'author': 'OP13 LL',
    'description': 'Plates master mix for lineage-specific primer pool evaluations.'
}

def run(protocol: protocol_api.ProtocolContext):

    # 0. Initialization
    
    volume = 10
    
    protocol.home()

    p300tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 4, 'Tip Rack')
    plate = protocol.load_labware('appliedbiosystemsmicroamp_384_wellplate_40ul', 2, 'Plate')
    rack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 3, 'Master Mixes')

    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300tips])


    # 1. Pipetting master mixes 1-4

    tube_number = 0

    for section_rows in range(2):                       # rows A-F or G-L
        for section_columns in range(2):                # columns 1-12 or 13-24

            tube_number += 1
            list = []

            for no_of_cols in range(12):                # 12 columns per master mix
                for wells_in_column in range(6):        # 6 wells per column
                
                    list.append(
                        section_rows*6      +
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


    # 2. Pipetting master mix 5

    tube_number = 5
    p300.pick_up_tip()

    for section_columns in range(2):                # columns 1-12 or 13-24

        list = []

        for no_of_cols in range(12):                # 12 columns per section

            if section_columns == 0:        
                for wells_in_column in range(2):    # 2 wells per column
                    list.append(
                        section_columns*192 +
                        no_of_cols*16       +
                        wells_in_column     +
                        12                          # plating begins with row M
                    )

            else:      
                for wells_in_column in range(4):    # 4 wells per column
                    list.append(
                        section_columns*192 +
                        no_of_cols*16       +
                        wells_in_column     +
                        12  
                    )     
        
        p300.distribute(
                volume,
                rack['A'+str(tube_number)],
                [plate.wells()[wellIndex] for wellIndex in list],
                new_tip = 'never'
            )

    p300.drop_tip()
