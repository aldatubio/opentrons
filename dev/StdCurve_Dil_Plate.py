'''
Project Freetown
Standard Curve Dilution and Plating for Pre-LoD Work (Extracted Viral RNA)
Updated 2025-03-14
Author: OP13 LL

INSTRUCTIONS FOR USE

This protocol takes two parameters, entered in the Opentrons app interface:
 - Number of plates (integer)
 - Negative plating: manual, plate using template diluent, or plate using kit negative (separate user-provided tube)

A ten-point serial dilution series is generated (1.0E6 to 0.5 copies per µL), then plated on a 96-well plate.
Dilutions can then be transferred to another plate containing mastermix using a multichannel pipette.

The serial dilution values can be changed here in Python, if desired;
from an end-user perspective, these values are hard-coded as to reduce risk of user error.


PLATE LAYOUT (copies per well)

      1   2   3   4   5   6   7   8   9   10   11   12   
    ┌───────────────────┬───────────┬─────────────┬─────┐
  A │                   │  1.0E+07  │   1.0E+06   │     │
    │                   ├───────────┼─────────────┤     │
  B │                   │  1.0E+05  │   1.0E+04   │ Kit │
    │                   ├───────────┴─────────────┤     │
  C │                   │          1000           │ Neg │
    │                   ├─────────────────────────┤     │
  D │                   │           200           │     │
    │               ┌───┴─────────────────────────┴─────┤
  E │               │               100                 │
    │               ├───────────────────────────────────┤
  F │               │                20                 │
    │               ├───────────────────────────────────┤
  G │               │                10                 │
    │               ├───────────────────────────────────┤
  H │               │                 5                 │
    └───────────────┴───────────────────────────────────┘

'''


from opentrons import protocol_api
import pandas as pd
import math


vol_per_well = 10 #µL
copies_per_well =    [1*10**7, 1*10**6, 1*10**5, 1*10**4, 1000, 200, 100, 20, 10, 5]
wells_per_dilution = [      3,       3,       3,       3,    6,   6,   8,  8,  8, 8]
num_plates = 1
excess_vol = 5 #µL

dil_loc = 'A1'
neg_loc = 'A6'


def ceil_10(num):
    '''Round value up to the nearest 10.'''
    return int(math.ceil(num/10.0))*10


def get_volumes(vol_per_well:float, copies_per_well:list, wells_per_dilution:list, num_plates=1, excess_vol=10.0):
    '''Based on volume per well, copies per well (list of floats), and wells per dilution (list of ints),
    create a table containing volumes of RNA and diluent required for each dilution step.
    
    For ease of use in Opentrons commands, table is returned as a dictionary of lists.
    '''

    # construct data frame from existing lists
    data = {'cp/well': copies_per_well, 'wells/dil': wells_per_dilution}
    df = pd.DataFrame(data)

    # calculate dilution factor for each step
    df['dil factor'] = 1
    for i in range(1, len(df)):
        df.loc[i, 'dil factor'] = df.loc[i-1, 'cp/well'] // df.loc[i, 'cp/well']

    # calculate exact volume needed for plating in each step (wells * volume per well, plus 20 µL excess, plus 15 µL per plated well)
    df['exact vol'] = (df['wells/dil'] * (vol_per_well+excess_vol)) * num_plates + 20

    # calculate adjusted volume needed, accounting for downstream dilutions
    df['adj vol'] = df['exact vol']
    for i in range(len(df) - 2, -1, -1): #start at second-to-last dilution and iterate backwards through first dilution
        df.loc[i, 'adj vol'] = ceil_10(df.loc[i, 'exact vol'] + (df.loc[i+1,'adj vol'] // df.loc[i+1,'dil factor']))

    # calculate volumes of RNA and diluent needed for each step
    df['rna vol'] = df['adj vol'] // df['dil factor']
    df['dil vol'] = df['adj vol'] - df['rna vol']

    # calculate volumes to dispense into wells

    dict = {'rna': df['rna vol'].to_list(),
            'dil': df['dil vol'].to_list()}
    return dict


def choose_pipette(vol, range1:dict, range2:dict):
    '''Based on a volume, choose between two pipette ranges for optimal dispensing.'''
    # choose pipette that contains the volume within its pipettable range
    if vol > range1['min'] and vol <= range1['max']:
        return list(range1.values())
    elif vol > range2['min'] and vol <= range2['max']:
        return list(range2.values())
    
    # if pipette vol is smaller than either range, choose lower-vol pipette
    elif vol <= range1['min'] and vol <= range2['min']:
        if range1['min'] <= range2['min']:
            return list(range1.values())
        else:
            return list(range2.values())
        
    # otherwise, choose higher-vol pipette
    else:
        if range1['max'] >= range2['max']:
            return list(range1.values())
        else:
            return list(range2.values())


def choose_mixing(rna_vol:float, dil_vol:float, range1:dict, range2:dict):
    '''Based on RNA volume, diluent volume, and available pipette ranges,
    choose pipettes for dispensing and mixing, plus mixing volume.'''
    use_p300_mix = False
    pipette, _, p_max = choose_pipette(rna_vol, range1, range2)
    totalvol_80percent = 0.8*(rna_vol + dil_vol)
    
    # if 80% of total volume in tube is less than pipette's max, use this as mixing vol
    if totalvol_80percent < p_max:
        mix_vol = totalvol_80percent
    # if this volume is greater than the pipette's max, check which pipette is being used
    else:
        # if P20 is being used, switch to p300 for mixing
        if p_max == 20.0:
            if totalvol_80percent < 200.0:
                mix_vol = totalvol_80percent
                use_p300_mix = True
            else:
                mix_vol = 200.0
                use_p300_mix = True
        # if P20 isn't being used for the dilution step, current pipette - P300 or P1000 - is fine
        else:
            mix_vol = p_max

    return pipette, mix_vol, use_p300_mix

        
def get_wells():
    '''For the plate map shown in this protocol, get a list of lists containing indices for wells to plate.'''
    wells_list = []

    # first 4 points in series
    for i in range(4):
        wells = [8*x + math.floor(i/2) for x in range(5,8)]
        if i % 2 != 0: #i is odd
            wells = [x+24 for x in wells] #shift over by 3 columns for odd i
        wells_list.append(wells)

    # next 2 points in series
    for i in range(2,4):
        wells = [8*x + i for x in range(5,11)]
        wells_list.append(wells)

    # final 4 points in series
    for i in range(4,8):
        wells = [8*x + i for x in range(4,12)]
        wells_list.append(wells)

    return wells_list


metadata = {
    'apiLevel': '2.22',
    'protocolName': 'Freetown | Standard Curve for Pre-LoD',
    'author': 'OP13 LL',
    'description': 'Prepares and plates a ten-point serial dilution series.'
}

requirements = {
    'robotType': 'OT-2'
}


def add_parameters(parameters: protocol_api.Parameters):
    
    parameters.add_str(
        variable_name = "robot",
        display_name = "Robot",
        choices = [
            {"display_name": "7B10", "value": "7B10"},
            {"display_name": "8B04", "value": "8B04"}
        ],
        default = "7B10"
    )
    
    parameters.add_str(
        variable_name = "neg_handling",
        display_name = "Negative control plating",
        choices = [
            {"display_name": "Manual", "value": "manual"},
            {"display_name": "Auto - use kit negative", "value": "kit"},
            {"display_name": "Auto - use diluent as negative", "value": "diluent"}
        ],
        default = "kit"
    )

    parameters.add_int(
        variable_name = "num_plates",
        display_name = "Number of plates to prepare",
        default = 1,
        minimum = 1,
        maximum = 4
    )


def run(protocol: protocol_api.ProtocolContext):

    protocol.home()

    # to use this protocol with simulator, get rid of protocol params temporarily
    num_plates = protocol.params.num_plates
    neg_handling = protocol.params.neg_handling
    robot = protocol.params.robot
    
    vols = get_volumes(vol_per_well, copies_per_well, wells_per_dilution, num_plates=num_plates, excess_vol=excess_vol)


    ###
    ### Deck setup
    ###

    tubes = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 4)
    diluent = protocol.load_labware('usascientific_15_tuberack_5000ul', 1)
    plate = protocol.load_labware('abs_usasci_96well_200ul', 2)

    p300_tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
    p300 = protocol.load_instrument('p300_single_gen2', 'right', tip_racks=[p300_tips])
    p300_range = {'pipette': p300, 'min': 20.0, 'max': 200.0}
    if robot == '7B10':
        left_tips = protocol.load_labware('opentrons_96_filtertiprack_20ul', 6)
        left_pipette = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[left_tips])
        left_pipette_range = {'pipette': left_pipette, 'min': 0.0, 'max': 20.0}
    else:
        left_tips = protocol.load_labware('opentrons_96_filtertiprack_1000ul', 6)
        left_pipette = protocol.load_instrument('p1000_single_gen2', 'left', tip_racks=[left_tips])
        left_pipette_range = {'pipette': left_pipette, 'min': 200.0, 'max': 1000.0}

    
    ### Visualization of deck layout - API 2.14 and above only!
    ### To use protocol simulator, downgrade this protocol to 2.13 and comment out this section
    ###
    
    # ************************************
    def visualize_deck():
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

        neg_viz = protocol.define_liquid(
            'Kit negative control',
            'In 1.5mL tube',
            '#4f4'
        )

        empty_viz = protocol.define_liquid(
            'Empty Tube',
            '1.5mL tubes. Once filled, tubes are arranged in columns [B1 is dilution 1, C1 is dilution 2, D1 is dilution 3, A2 is dilution 4, etc.].',
            '#777'
        )

        diluent[dil_loc].load_liquid(
            diluent_viz,
            200 + ceil_10(sum(vols['dil']))
        )

        tubes['A1'].load_liquid(
            RNA_viz,
            vols['rna'][0] + 20
        )

        for i in range(1, len(vols['rna'])):
            tubes.wells()[i].load_liquid(
                empty_viz,
                0
            )

        if neg_handling == 'kit':
            tubes[neg_loc].load_liquid(
                neg_viz,
                vol_per_well * excess_vol + 20
            )

    visualize_deck()
    # ************************************
       

    ###
    ### 1. Transfer diluent
    ###

    pipette, _, _ = choose_pipette(max(vols['dil']), p300_range, left_pipette_range)

    pipette.pick_up_tip()
    pipette.transfer(
        vols['dil'],
        diluent[dil_loc],
        [tubes.wells()[i] for i in range(len(vols['dil']))],
        blow_out = True,
        blowout_location = 'source well',
        new_tip = 'Never'
    )
    pipette.drop_tip()


    ###
    ### 2. Perform dilutions
    ###

    for i in range(1, len(vols['rna'])):

        pipette, mix_vol, use_p300_mix = choose_mixing(vols['rna'][i], vols['dil'][i],
                                                       p300_range, left_pipette_range)

        if not use_p300_mix:
            pipette.transfer(
                vols['rna'][i],
                tubes.wells()[i-1],
                tubes.wells()[i],
                mix_after = (5, mix_vol)
            )
        
        else:
            pipette.transfer(
                vols['rna'][i],
                tubes.wells()[i-1],
                tubes.wells()[i]
            )
            p300.pick_up_tip()
            p300.mix(5, mix_vol, tubes.wells()[i])
            p300.drop_tip()


    ###
    ### 3. Plate dilutions
    ###

    wells = get_wells()

    for i in range(len(vols['rna'])):
        p300.distribute(
            vol_per_well+excess_vol,
            tubes.wells()[i],
            [plate.wells()[x] for x in wells[i]],
            disposal_volume = 10
        )

    if neg_handling != 'manual':
        if neg_handling == 'kit':
            loc = tubes[neg_loc]
        else:
            loc = diluent[dil_loc]

        p300.distribute(
            vol_per_well+excess_vol,
            loc,
            [plate.wells()[x] for x in [88, 89, 90, 91]],
            disposal_volume = 10
        )

    protocol.home()