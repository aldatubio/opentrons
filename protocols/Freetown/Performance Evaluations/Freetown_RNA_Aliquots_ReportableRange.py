'''
Project Freetown
RNA Aliquoting for Reportable Range - 96-well Plate
Updated 2024-05-10
Author: OP13 LL

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


The previous Python protocol prepares a set of 14 RNA dilutions, with concentrations as outlined in the table above.
​This dilution series is sufficient volume of RNA to perform a reportable range on four 96-well plates.

This protocol aliquots RNA dilutions into a 96-well plate, matching the plate layout used for reportable range experiments.
RNA from these aliquots can then be "stamped" into each qPCR plate [i.e., 10µL from column 1 of the aliquot plate can be added
to column 1 of the qPCR plate, and so on]. This minimizes user time/effort, especially if a multichannel multipipette is not available.

Plate Map

     1    2    3    4    5    6    7    8    9    10   11   12 
   ┌───────────────────┬───────────────────┬───────────────────┐
 A │         1         │         2         │         3         │
   ├───────────────────┼───────────────────┼───────────────────┤
 B │         4         │         5         │         6         │
   ├───────────────────┼───────────────────┼───────────────────┤
 C │         7         │         8         │         9         │
   ├───────────────────┴───────────────────┼───────────────────┤
 D │                  10                   │                   │
   ├───────────────────────────────────────┤      Negative     │
 E │                  11                   │                   │
   ├───────────────────────────────────────┴───────────────────┤
 F │                            12                             │
   ├───────────────────────────────────────────────────────────┤
 G │                            13                             │
   ├───────────────────────────────────────────────────────────┤
 H │                            14                             │
   └───────────────────────────────────────────────────────────┘

Tube Setup

Empty 96-well plate
RNA dilutions [14]: columns 1-3, plus A4-B4, of 24-ct 1.5mL rack [arranged in columns]

'''

from opentrons import protocol_api

metadata = {
    'apiLevel': '2.13',
    'protocolName': 'Freetown | Aliquoting for Reportable Range',
    'author': 'OP13 LL',
    'description': '''Distributes RNA dilutions into a 96-well plate for stamping. 
                    '''
}

def run(protocol: protocol_api.ProtocolContext):

  protocol.home()

  ###
  ### User-defined variables
  ###

  aliquot_vol = 45            # volume of RNA to be aliquoted into each plate well

  negatives_tube = True       # if false, negatives will not be plated/aliquoted
  negatives_location = 'A5'   # location within 24-ct 1.5mL tube rack



  ###
  ### Initialization
  ###

  p300tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
  tubes = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 2)
  plate = protocol.load_labware('armadillo_96_wellplate_200ul_pcr_full_skirt', 1)

  # pipette initialization
  p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300tips])


  ###
  ### Visualization of deck layout - API 2.14 and above only!
  ### To use protocol simulator, downgrade this protocol to 2.13 and comment out this section
  ###
  
  # ************************************
  
  RNA_viz = protocol.define_liquid(
      'RNA Dilutions',
      '14 tubes arranged in columns [A1 is dilution 1, B1 is dilution 2, etc].',
      '#f44'
  )

  neg_viz = protocol.define_liquid(
      'Negative',
      '0.05 ng/µL hgDNA in 0.05 mg/mL tRNA-dH2O.',
      '#44f'
    )

  for i in range(14):
      tubes.wells()[i].load_liquid(
          RNA_viz,
          540
      )

  if negatives_tube == True:
      tubes[negatives_location].load_liquid(
          neg_viz,
          540
      )
  # ************************************



  ###
  ### 1. Aliquot dilutions to plate - 4 replicates (dilutions 1-9)
  ###

  for dil in range(9):  # dilutions with indices 0-8
     
     # create list containing wells to fill
     wells_to_fill = []
     
     if dil < 3:
        row = 0 # row A
     elif dil < 6:
        row = 1 # row B
     else:
        row = 2 # row C
        
     col_group = dil % 3  # columns 1-4, 5-8, or 9-12

     for col in range(4): # 4 replicates per row - 4 columns
        wells_to_fill.append(
            32*col_group +
            8*col +
            row
        )

     # fill wells
     p300.distribute(
         aliquot_vol,
         [tubes.wells()[dil]],
         [plate.wells()[well] for well in wells_to_fill],
         blow_out = True,
         blowout_location = 'source well'
      )



  ###
  ### 2. Aliquot dilutions to plate - 8 replicates (dilutions 10-11)
  ###

  for dil in range(9,11):  # dilutions with indices 9-10
     
     # create list containing wells to fill
     wells_to_fill = []

     row = dil - 6   # convert dilution index (ex. "9") to row index (ex. "3" - row D)

     for col in range(8): # 8 replicates per row
        wells_to_fill.append(
            8*col +
            row
        )

     # fill wells
     p300.distribute(
         aliquot_vol,
         [tubes.wells()[dil]],
         [plate.wells()[well] for well in wells_to_fill],
         blow_out = True,
         blowout_location = 'source well'
      )        
     


  ###
  ### 3. Aliquot dilutions to plate - 12 replicates (dilutions 12-14)
  ###

  for dil in range(11, 14):  # dilutions with indices 11-13
     
     # create list containing wells to fill
     wells_to_fill = []

     row = dil - 6   # convert dilution index (ex. "11") to row index (ex. "5" - row F)

     for col in range(12): # 12 replicates per row
        wells_to_fill.append(
            8*col +
            row
        )

     # fill wells
     p300.distribute(
         aliquot_vol,
         [tubes.wells()[dil]],
         [plate.wells()[well] for well in wells_to_fill],
         blow_out = True,
         blowout_location = 'source well'
      )


  ###
  ### 4. Aliquot negative control, if included
  ###

  if negatives_tube == True:
      
    # create list containing wells to fill
    wells_to_fill = []


    for row in range(3, 5):  # 2 rows: D ("3") and E ("4")
      for col in range(8, 12): # 4 replicates per row, in columns with indices 8-11
        wells_to_fill.append(
            8*col +
            row
        )

    # fill wells
    p300.distribute(
        aliquot_vol,
        tubes[negatives_location],
        [plate.wells()[well] for well in wells_to_fill],
        blow_out = True,
        blowout_location = 'source well'
      )
    
  protocol.home()
      
