'''
Project Freetown
Custom Dilution Series
Updated 2024-07-02
Author: OP13 LL

INSTRUCTIONS FOR USE

This protocol takes parameters (volumes, number of tubes/dilutions) in csv format -
either as a pasted list of values, or as an imported csv file "Dilution Series.csv".

1. OPTION 1: Paste csv data as list into "csv_raw" variable. Ensure that the pasted list only concerns tube dilutions
   performed by the robot - for example, the stock/starting tube ("dilution 0") should not be included in the list.
2. OPTION 2: Using the provided "Dilution Series.csv" file as a template, fill out the file with your dilution series.
   Then, drag the file onto the "Upload CSV to Opentrons" widget to securely copy the file to Opentrons via SSH.
2. If needed, you can also change the position of the tube of diluent - "diluent_location" variable.

'''

from datetime import datetime
import csv
import io
from opentrons import protocol_api

# To paste a list below (edit default volumes):
# Create an Excel sheet with the following columns:
# dilution number, RNA volume, diluent volume
# then export this sheet as a csv. Open the csv with Notepad and paste contents in the "csv_raw" variable below.
# Ensure that column headers and stock/source tube information ("dilution 0") are EXCLUDED.


metadata = {
    'apiLevel': '2.18',
    'protocolName': 'Freetown | Custom Dilution Series',
    'author': 'OP13 LL',
    'description': 'Custom dilution series.'
}

requirements = {
    'robotType': 'OT-2'
}

def add_parameters(parameters: protocol_api.Parameters):
    parameters.add_bool(
        variable_name = "default_volumes",
        display_name = "Default Volumes",
        # description can only be 100 characters
        description = "14-point dilution series from the Analytical Inclusivity protocol (2.5E6 - 0.5 cp/µL) for 3 plates.",
        default = True
    )
    parameters.add_str(
        variable_name = "file_name",
        display_name = "Name of CSV File", # must be less than 30 characters
        choices = [
            {"display_name": "", "value": ""},
            {"display_name": "Dilution Series.csv", "value": "Dilution Series.csv"}
        ],
        description = "If applicable (must switch Default Volumes to Off).",
        default = ""
    )
    parameters.add_str(
        variable_name = "diluent_rack",
        display_name = "Diluent Tube",
        choices = [
            {"display_name": "1.5 mL", "value": "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap"},
            {"display_name": "5 mL", "value": "usascientific_15_tuberack_5000ul"},
            {"display_name": "25 mL", "value": "opentrons_6_tuberack_25ml"}
        ],
        default = "usascientific_15_tuberack_5000ul"
    )
    parameters.add_str(
        variable_name = "left_pipettor",
        display_name = "Left Pipette",
        description = "Pipette installed on left mount.",
        choices = [
            {"display_name": "1-Channel 20 µL", "value": "p20_single_gen2"},
            {"display_name": "1-Channel 300 µL", "value": "p300_single_gen2"},
            {"display_name": "1-Channel 1000 µL", "value": "p1000_single_gen2"}
        ],
        default = "p1000_single_gen2"
    )
    parameters.add_str(
        variable_name = "right_pipettor",
        display_name = "Right Pipette",
        description = "Pipette installed on right mount.",
        choices = [
            {"display_name": "1-Channel 20 µL", "value": "p20_single_gen2"},
            {"display_name": "1-Channel 300 µL", "value": "p300_single_gen2"},
            {"display_name": "1-Channel 1000 µL", "value": "p1000_single_gen2"}
        ],
        default = "p300_single_gen2"
    )

def run(protocol: protocol_api.ProtocolContext):

    protocol.home()

    ### dummy param - forces protocol reanalysis to fix bug described here:
    ### https://github.com/Opentrons/opentrons/issues/14598
    
    now = datetime.now()
    protocol.comment(f"Run started {now}")
    
    
    ###
    ### csv handling
    ###

    if protocol.params.default_volumes is True:
        csv_raw = '''1,50,200
2,50,200
3,50,200
4,50,200
5,50,200
6,50,200
7,105,420
8,375,375
9,375,375
10,375,375
11,375,375
12,375,375
13,375,375
'''
        # Parsing csv input - StringIO method treats pasted string as file object
        csv_file = io.StringIO(csv_raw)
        csv_reader = csv.reader(csv_file, delimiter = ",")
            # saving the csv_reader as a list allows us to iterate over the reader more than once -
        # using the reader and doing a "for row in csv_reader" loop consumes the reader
        dataset = list(csv_reader)
        protocol.comment("Using default CSV data")

    else:
        file_path = "/data/user_storage/aldatubio/Dilution Series.csv"
        with open(file_path, encoding = "utf-8-sig", newline="") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ",")
            next(csv_reader) # skip header row
            dataset = list(csv_reader)
            protocol.comment(f"Loading CSV data from {file_path}")
            protocol.comment(f"Loaded CSV data: {dataset}")


    ###
    ### Initialization
    ###

    diluent_location = 'A1'

    tubes = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 2)
    diluent = protocol.load_labware(protocol.params.diluent_rack, 1)

    if protocol.params.left_pipettor == "p20_single_gen2":
        left_tips = protocol.load_labware('opentrons_96_filtertiprack_20ul', 6)
        left_max_vol = 20
    elif protocol.params.left_pipettor == "p300_single_gen2":
        left_tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 6)
        left_max_vol = 200
    elif protocol.params.left_pipettor == "p1000_single_gen2":
        left_tips = protocol.load_labware('opentrons_96_filtertiprack_1000ul', 6)
        left_max_vol = 1000
    
    left_pipette = protocol.load_instrument(protocol.params.left_pipettor, 'left', tip_racks=[left_tips])

    if protocol.params.right_pipettor == "p20_single_gen2":
        right_tips = protocol.load_labware('opentrons_96_filtertiprack_20ul', 3)
        right_max_vol = 20
    elif protocol.params.right_pipettor == "p300_single_gen2":
        right_tips = protocol.load_labware('opentrons_96_filtertiprack_200ul', 3)
        right_max_vol = 200
    elif protocol.params.right_pipettor == "p1000_single_gen2":
        right_tips = protocol.load_labware('opentrons_96_filtertiprack_1000ul', 3)
        right_max_vol = 1000
    
    right_pipette = protocol.load_instrument(protocol.params.right_pipettor, 'right', tip_racks=[right_tips])


    if left_max_vol > right_max_vol:
        larger_pipette = left_pipette
        larger_max_vol = left_max_vol
        smaller_pipette = right_pipette
        smaller_max_vol = right_max_vol
    else:
        larger_pipette = right_pipette
        larger_max_vol = right_max_vol
        smaller_pipette = left_pipette
        smaller_max_vol = left_max_vol

    
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

    total_diluent_vol = 200
    for row in dataset:
        total_diluent_vol = total_diluent_vol + int(row[2])

    diluent[diluent_location].load_liquid(
        diluent_viz,
        total_diluent_vol
    )

    tubes['A1'].load_liquid(
        RNA_viz,
        int(dataset[0][1]) + 20
    )

    for row in dataset:
        tubes.wells()[int(row[0])].load_liquid(
            empty_viz,
            0
        )
    # ************************************
    

    ###
    ### 1. Transfer diluent
    ###

    counter = []
    diluent_vols = []
    tubes_to_fill = []

    for row in dataset:

        # ensure that row data is wrapped in int() - needs to be number type, not string
        diluent_vols.append(int(row[2]))
        tubes_to_fill.append(int(row[0]))

        # Choose pipette to use: first, create list: any time a volume greater than smaller max vol is detected, a "1" gets added to the list
        if int(row[2]) > smaller_max_vol:
            counter.append(1)
        else:
            counter.append(0)
        
    protocol.comment(f"Diluent volumes: {diluent_vols}")
    protocol.comment(f"Tubes being filled: {tubes_to_fill}")
    
    # Choosing pipette: check: are there any "1"s in the list? if so, a volume greater than smaller max vol is present, and we will need the larger pipette
    if sum(counter) > 0:
        pipette = larger_pipette
    else:
        pipette = smaller_pipette

    pipette.pick_up_tip()
    pipette.transfer(
        diluent_vols,
        diluent[diluent_location],
        [tubes.wells()[index] for index in tubes_to_fill],
        blow_out = True,
        blowout_location = "source well",
        new_tip = "Never"
    )
    pipette.drop_tip()
    

    ###
    ### 2. Transfer RNA
    ###

    for row in dataset:

        # choose pipette
        if int(row[1]) > smaller_max_vol:
            pipette = larger_pipette
            pipette_max_vol = larger_max_vol
        else:
            pipette = smaller_pipette
            pipette_max_vol = smaller_max_vol

        # set mixing volume - must be less than max pipette volume
        if (int(row[1]) + int(row[2]))*0.8 < pipette_max_vol:
            mix_vol = (int(row[1]) + int(row[2]))*0.8
        else:
            mix_vol = pipette_max_vol
        
        pipette.transfer(
            int(row[1]),
            [tubes.wells()[int(row[0]) - 1]],
            [tubes.wells()[int(row[0])]],
            mix_after = (
                5,
                mix_vol
            )
        )

    protocol.home()