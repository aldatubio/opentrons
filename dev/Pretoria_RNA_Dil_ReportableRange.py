'''
Project Pretoria
RNA Dilutions for Reportable Range
Updated 2023-07-28
Author: OP13 LL

+----------+----------------------+---------------+------------+
|               Stock Concentrations              | # of Wells |
+----------+----------------------+---------------+------------+
| Dilution |   Stock Copy / µL    | Copy Per Well |            |
+----------+----------------------+---------------+------------+
|        1 |             1.00E+05 |      1.00E+06 |          4 |
|        2 |             4.00E+04 |      4.00E+05 |          4 |
|        3 |             1.60E+04 |      1.60E+05 |          4 |
|        4 |             6.40E+03 |      6.40E+04 |          4 |
|        5 |                2,560 |      2.60E+04 |          4 |
|        6 |                1,024 |      1.00E+04 |          4 |
|        7 |                  410 |         4,096 |          8 |
|        8 |                  164 |         1,638 |          8 |
|        9 |                   66 |           655 |         12 |
|       10 |                   26 |           262 |         12 |
|       11 |                   10 |           105 |         12 |
|       12 |                    4 |            42 |         12 |
| Negative |                      |               |          8 |
+----------+----------------------+---------------+------------+

​For the performance evaluations in Project Pretoria, eleven dilutions of 2.5-fold are prepared to generate a reportable range
from 1.0E6 to 42 copies / reaction [adding 10 µL / well]. To mitigate the time burden associated with generating these dilutions,
should we be required to repeat any of the performance evaluations at a later date, then the intention is to generate multiple
single-use aliquots at ~1.0E6 copies / µL for long-term storage. These single-use aliquots can then be loaded onto the Opentrons and diluted.  

​There are ten different synthetic RNA constructs for HIV drug resistance genotyping, all of which are named starting with “POL”.
In the Pretoria assay, there are four separate PANDAA triplexes. Each PANDAA triplex detects two drug resistance mutations
and the VQ. One triplex is added per well of a 96-well plate.  

​The dilution series prepared on the Opentrons would be sufficient volume of RNA to perform a reportable range on four 96-well plates
i.e., one reportable range series per PANDAAA.   

​Opentrons Protocol 

​Add Reagents and Consumables to Opentrons Deck 
1. ​Eleven empty 1.5mL lo-bind Eppendorf tubes arrayed in rack on the Opentrons. 
2. ​One 1.5mL lo-bind Eppendorf tube containing 900 µL RNA master stock added to Opentrons rack [tube #1]. 
3. ​One 25mL Eppendorf tube with ~10mL tRNA.  

​Program 
1. ​Opentrons dispenses 540 µL tRNA from 25mL tube to eleven empty 1.5mL tubes. 
2. ​From tube #1, the RNA master stock, transfer 360 µL to the first 1.5mL tube that contains 540 µL tRNA [tube #2]. 
3. ​After dispensing 360 µL RNA into tube #2, pipette up and down to mix thoroughly.  
4. ​Discard tip. 
5. ​Perform same transfer workflow of 360 µL RNA, this time from tube #2 into tube #3. 
6. ​Repeat until 2.5-fold dilutions have been performed eleven times. ​ 

'''

from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Pretoria | RNA Dilutions for Reportable Range',
    'author': 'OP13 LL',
    'description': '''Performs eleven 2.5-fold dilutions to generate a reportable range from 1.0E6 to 42 cp/rxn [adding 10 µL/well].'''
}

def run(protocol: protocol_api.ProtocolContext):

    protocol.home()

    p1000tips = protocol.load_labware('opentrons_96_filtertiprack_1000ul', 3)
    tubes = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 2)
    # custom 25mL tube definition
    diluent = protocol.load_labware('opentrons_6_tuberack_25ml', 1)

    # pipette initialization
    p1000 = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[p1000tips])