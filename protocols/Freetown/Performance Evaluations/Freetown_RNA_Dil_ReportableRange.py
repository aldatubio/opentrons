'''
Project Freetown
RNA Dilutions for Reportable Range
Updated 2024-05-21
Author: OP13 LL

Adapted from Project Pretoria's RNA Dilutions for Reportable Range protocol

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

from opentrons import protocol_api

metadata = {
    'apiLevel': '2.14',
    'protocolName': 'Freetown | RNA Dilutions for Reportable Range',
    'author': 'OP13 LL',
    'description': '''Performs fourteen-point dilution series. 
                    DURATION: 20 min.'''
}

def run(protocol: protocol_api.ProtocolContext):

    protocol.home()

    ###
    ### User-defined variables
    ###

    '''
    # Original Cairo setup:

    diluent_vol = [200, 300, 300]
    diluent_location = 'B1'

    RNA_vol = [50, 75, 300]
    num_tubes = [7, 1, 6] # number of tubes to contain RNA; arranged in columns (A1, B1, C1, D1, A2...)
    '''

    diluent_vol = [68, 144, 130]
    diluent_location = 'B1'
    
    RNA_vol = [17, 36, 130]
    num_tubes = [7, 1, 6] # number of tubes to contain RNA; arranged in columns (A1, B1, C1, D1, A2...)
    
    
    ###
    ### Initialization
    ###

    p300tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
    p20tips = protocol.load_labware('opentrons_96_filtertiprack_20ul', 6)
    tubes = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 2)
    # custom 25mL tube definition - Eppendorf screw-top
    diluent = protocol.load_labware('opentrons_6_tuberack_25ml', 5)

    # pipette initialization
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300tips])
    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[p20tips])


    ###
    ### Visualization of deck layout - API 2.14 and above only!
    ### To use protocol simulator, downgrade this protocol to 2.13 and comment out this section
    ###
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


    ###
    ### 1. Transfer diluent
    ###

    p300.pick_up_tip()
    tube_counter = 1

    for j in num_tubes:

        for i in range(tube_counter, j + tube_counter):
            if tube_counter >= sum(num_tubes):
                break
            p300.transfer(
                diluent_vol[j], ###need to check whether this will work - I am doubtful
                diluent[diluent_location],
                [tubes.wells()[i]],
                new_tip = 'never'
            )
            tube_counter += 1

    p300.drop_tip()

## Below content still needs amendment

    ###
    ### 2. Transfer RNA
    ###

    for i in range(1, num_tubes):

        p1000.transfer(
            RNA_vol,
            [tubes.wells()[i - 1]],
            [tubes.wells()[i]],
            mix_after = (
                5,
                (diluent_vol + RNA_vol)*0.8
            )
        )


    protocol.home()