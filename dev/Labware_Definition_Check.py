'''
This protocol can be used to check whether a new labware definition is suitable. 
'''

new_labware_name = 'abs_96well_100ul'

###########################################################################################

from opentrons import protocol_api

metadata = {
    'apiLevel': '2.22',
    'protocolName': 'Labware Definition Check',
    'author': 'OP13 LL',
    'description': 'Check whether a newly generated labware definition is suitable.'
}

requirements = {
    'robotType': 'OT-2'
}


def run(protocol: protocol_api.ProtocolContext):

    liquid = protocol.load_labware('usascientific_15_tuberack_5000ul', 1)
    new_labware = protocol.load_labware(new_labware_name, 2)
    p300_tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300_tips])

    def visualize_deck():
        liquid_viz = protocol.define_liquid(
            'Water',
            '#44f'
        )

        liquid['A1'].load_liquid(
            liquid_viz,
            4000
        )
    
    if float(metadata['apiLevel']) >= 2.14:
        visualize_deck()


    p300.distribute(
        30,
        liquid['A1'],
        new_labware.wells()
    )

    protocol.home()

