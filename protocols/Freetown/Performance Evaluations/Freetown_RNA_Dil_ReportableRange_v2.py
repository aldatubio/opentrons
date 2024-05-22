'''
Project Freetown
RNA Dilutions for Reportable Range
Updated 2024-05-22
Author: OP13 LL

Adapted from Project Pretoria's RNA Dilutions for Reportable Range protocol

Basic design: takes parameters (volumes, number of tubes/dilutions) as a pasted csv table

----------------------------
  Stock Conc.    2.5E+6 µL  
----------------------------
  Dil. Factor    Variable   
  Vol Per Well   10         
  tRNA Needed    3500 µL    
----------------------------

------------------------------------------------------------
  #    Stock Conc.   Copies / Well   Dil Factor   # Wells  
------------------------------------------------------------
   1   2.5E+6 cp/µL   2.5E+7 cp/rxn            8         4  
   2   5.0E+5 cp/µL   5.0E+6 cp/rxn            5         4  
   3   1.0E+5 cp/µL   1.0E+6 cp/rxn            5         4  
   4   2.0E+4 cp/µL   2.0E+5 cp/rxn            5         4  
   5    4,000 cp/µL   4.0E+4 cp/rxn            5         4  
   6      800 cp/µL   8.0E+3 cp/rxn            5         4  
   7      160 cp/µL    1,600 cp/rxn            5         4  
   8       32 cp/µL      320 cp/rxn            5         4  
   9       16 cp/µL      160 cp/rxn            2         4  
  10        8 cp/µL       80 cp/rxn            2         8  
  11        4 cp/µL       40 cp/rxn            2         8  
  12        2 cp/µL       20 cp/rxn            2        12  
  13        1 cp/µL       10 cp/rxn            2        12  
  14       .5 cp/µL        5 cp/rxn            2        12  
     Negative                                            8  
------------------------------------------------------------

Analytical Inclusivity

Analytical inclusivity is the ability of the assay to detect all geographically and genetically diverse
Ebolavirus and Marburgvirus species. The analytical inclusivity will a reportable range for each of the isolates,
allowing us to capture our dynamic range. This approach 1) allows us to determine the upper limit of detection
without the need for incredibly high concentrations of inactivated virus (which we won’t be able to obtain)
and 2) determine the expected lower limit of detection so that the analytical sensitivity work is designed appropriately
(as it is 4–5 concentrations around the LOD).


Freetown Design 

•	The same reportable range that was used for Project Cairo (run on a single 96-well plate). 
•	Run each of the templates three times, to be done on different days. 
•	The mastermix can be prepared by hand and plated by one Opentrons robot.
•	The templates can be diluted and prepared by a second Opentrons robot. 


Tube Setup

25mL tube: B1 of 6-ct 50mL rack
Single-use RNA aliquot: A1 of 24-ct 1.5mL rack
Empty 1.5mL tubes: B1-D1, A2-D2, A3-D3, and A4-B4 [first 4 columns] of 24-ct 1.5mL rack

'''

import csv
import io
from opentrons import protocol_api


###
### Paste your raw csv data here
###
csv_raw = '''1,17,68
2,17,68
3,17,68
4,17,68
5,17,68
6,17,68
7,36,144
8,130,130
9,130,130
10,130,130
11,130,130
12,130,130
13,130,130
'''
###
###
###


# Parsing csv input - StringIO method treats pasted string as file object
csv_file = io.StringIO(csv_raw)
csv_reader = csv.reader(csv_file, delimiter = ",")
# saving the csv_reader as a list allows us to iterate over the reader more than once -
# using the reader and doing a "for row in csv_reader" loop consumes the reader
dataset = list(csv_reader)

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Freetown | RNA Dilutions for Reportable Range',
    'author': 'OP13 LL',
    'description': '''Performs fourteen-point dilution series. 
                    DURATION: 20 min.'''
}

def run(protocol: protocol_api.ProtocolContext):

    protocol.home()

    ###
    ### Initialization
    ###

    diluent_location = 'B1'

    p300tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
    tubes = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 2)
    # custom 25mL tube definition - Eppendorf screw-top
    diluent = protocol.load_labware('opentrons_6_tuberack_25ml', 5)

    # pipette initialization
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300tips])


    ### needs edits

    ### Visualization of deck layout - API 2.14 and above only!
    ### To use protocol simulator, downgrade this protocol to 2.13 and comment out this section
    ###
    '''
    # ************************************
    diluent_viz = protocol.define_liquid(
        'Diluent',
        '0.05 mg/mL tRNA in dH2O',
        '#44f'
    )

    RNA_viz = protocol.define_liquid(
        'RNA',
        'Single-use RNA aliquot in 1.5mL tube',
        '#f44'
    )

    empty_viz = protocol.define_liquid(
        'Empty Tube',
        '1.5mL tubes. Once filled, tubes are arranged in columns [B1 is dilution 1, C1 is dilution 2, D1 is dilution 3, A2 is dilution 4, etc.].',
        '#777'
    )

    diluent[diluent_location].load_liquid(
        diluent_viz,
        diluent_vol*num_tubes
    )

    tubes['A1'].load_liquid(
        RNA_viz,
        RNA_vol + diluent_vol
    )

    for i in range(1, sum(num_tubes)):
        tubes.wells()[i].load_liquid(
            empty_viz,
            0
        )
    # ************************************
    '''

    ###
    ### 1. Transfer diluent
    ###

    p300.pick_up_tip()

    # ensure that row data is wrapped in int() - needs to be number type, not string
    for row in dataset:
        p300.transfer(
            int(row[2]),
            diluent[diluent_location],
            [tubes.wells()[int(row[0])]],
            new_tip = 'never'
        )

    p300.drop_tip()


    ###
    ### 2. Transfer RNA
    ###

    for row in dataset:

        # set mixing volume - must be less than max pipette volume
        if (int(row[1]) + int(row[2]))*0.8 < 200:
            mix_vol = (int(row[1]) + int(row[2]))*0.8
        else:
            mix_vol = 200
        
        p300.transfer(
            int(row[1]),
            [tubes.wells()[int(row[0]) - 1]],
            [tubes.wells()[int(row[0])]],
            mix_after = (
                5,
                mix_vol
            )
        )

    protocol.home()