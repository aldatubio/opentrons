'''
Primer Optimization
Updated 2023-01-19
Author: OP13 LL

Purpose: Prepare dilution series of one forward and one reverse primer,
in order to optimize the pair's sensitivity and specificity.

Duration:

Execution: This script will prepare 4X primer pair dilutions as follows:
    1. Variable forward primer concentrations
        - 2A: 1:2 | 1000 nM R + 500 nM F
        - 3A: 1:3 | 1000 nM R + 333 nM F
        - 4A: 1:4 | 1000 nM R + 250 nM F
        - 5A: 1:5 | 1000 nM R + 200 nM F
    2. Dilution series of tubes from previous step
        - 100%: neat sample from step 1 tube
        - 75%: 30 µL sample, 10 µL H2O
        - 50%: 20 µL sample, 20 µL H2O
        - 25%: 10 µL sample, 30 µL H2O

Deck setup:


'''

from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'DEV Primer Optimization',
    'author': 'OP13 LL',
    'description': 'text'
}

def run(protocol: protocol_api.ProtocolContext):