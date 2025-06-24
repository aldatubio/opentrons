# opentrons
Scripts for the operation of Opentrons pipetting robots to prepare qPCR runs.

## Useful scripts and custom definitions
### Freetown scripts
- [Custom 8x8 primer evaluation (Assay Design)](https://github.com/aldatubio/opentrons/blob/main/protocols/Freetown/Assay%20Development/PrimerEval_PlatePrimers_Custom.py) - evaluates different primer combinations (up to 8 forward / 8 reverse, for 64 combinations). Plates primer combinations on a 384-well plate.
- [Custom primer titration (Assay Design)](https://github.com/aldatubio/opentrons/blob/main/protocols/Freetown/Assay%20Development/PrimerOptimization_Custom.py) - prepares forward/reverse primer dilutions as described in Primer Optimization protocols.
- [RNA Dilutions for Reportable Range (Analytical Inclusivity 2024)](https://github.com/aldatubio/opentrons/blob/main/protocols/Freetown/Performance%20Evaluations%20-%202024/Freetown_RNA_Dil_ReportableRange_v2.py) - prepares dilution series used in Freetown's 2024 analytical inclusivity experiments.
- [RNA Plating for Reportable Range (Analytical Inclusivity 2024)](https://github.com/aldatubio/opentrons/blob/main/protocols/Freetown/Performance%20Evaluations%20-%202024/Freetown_RNA_Aliquots_ReportableRange.py) - plates dilution series used in Freetown's 2024 analytical inclusivity experiments (for stamping onto mastermix plate using multichannel pipette).
- [Standard Curve Preparation and Plating (2025)](https://github.com/aldatubio/opentrons/blob/main/protocols/Freetown/Performance%20Verification%20-%202025/StdCurve_Dil_Plate.py) - prepares a standard curve, then plates it in a 96-well plate, following Freetown's 2025 Verification planning.
### Pretoria scripts
- [RNA Dilutions](https://github.com/aldatubio/opentrons/blob/main/protocols/Pretoria/Pretoria_RNA_Dil_ReportableRange.py) - prepares reportable range dilutions.
- [RNA Plating](https://github.com/aldatubio/opentrons/blob/main/protocols/Pretoria/Pretoria_RNA_Aliquots_ReportableRange.py) - plates reportable range.
### Other scripts
- [Labware definition check](https://github.com/aldatubio/opentrons/blob/main/dev/Labware_Definition_Check.py) - can be used to check whether a new custom labware definition is correctly configured. Uses the P300 to "pipette sample" into all wells of the new custom labware, making sure that all wells can be accessed correctly.
### Labware definitions
Custom definitions have been defined for: 5mL screw-cap tubes, 25mL tubes, 200µL strip tubes, 0.1mL 96-well plates.

## Contributions
**Note:** All contributions prior to July 2025 were authored by Lucy Langenberg during her employment at Aldatu Biosciences (2022 - 2025).
