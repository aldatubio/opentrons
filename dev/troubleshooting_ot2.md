# Troubleshooting Opentrons
This guide contains code snippets and script references for problems we've encountered in the past (hardware and software) and the software solutions we used to fix or get around these problems.

See also:
- **[Opentrons API Version 2 Reference](https://docs.opentrons.com/v2/new_protocol_api.html)**
- **[Opentrons comprehensive user guide](https://insights.opentrons.com/hubfs/Products/OT-2/OT-2R%20User%20Manual%20V1.0.pdf?_gl=1*19jxt1n*_ga*MjEzMDcwMDU2MS4xNjY3NTY2OTg3*_ga_66HK7MC5D7*MTY3OTkyNjM2NC41LjAuMTY3OTkyNjM2NC42MC4wLjA.*_ga_GNSMNLW4RY*MTY3OTkyNjM2NC40My4wLjE2Nzk5MjYzNjQuNjAuMC4w)** (.docx)


## Contents
- [Smoothie errors](#smoothie-errors)
- [Liquid handling](#liquid-handling)
  - [Viscous liquids](#viscous-liquids)
  - [Robot skips wells](#robot-is-skipping-wells-when-dispensing)
- [Decreasing tip usage](#robot-is-using-more-tips-than-necessary)
- [Displaying in-app messages and adding pause steps](#displaying-in-app-messages-and-adding-pause-steps)
- [Help with building block commands](#help-with-building-block-commands)
- [Troubleshooting scripts](#troubleshooting-scripts)

## Smoothie errors
Sometimes, the robot will throw an error during a run, typically looking something like this:
```
SmoothieError:
2M907 A0.1 B0.3 C0.3 X0.3 Y0.3 Z0.8 G4P0.005 G0B2.5 returned ALARM: Hard limit +B
```
Smoothieboard is the name of the motor controller board that Opentrons uses (open-source, originally a CNC controller meant for use in 3D printers). This type of error, then, is a hardware error, and is easily fixed by manual manipulation of the robot.

### Homing fail
A homing fail error might look something like this:
```
SmoothieError:
M907 A0.1 B0.05 C1.0 X0.3 Y0.3 Z0.1 G4P0.005 G28.2C returned ALARM: Homing fail
```
These types of errors will have the words `Homing fail` at the end of the error message. The relevant information here is the letter following the G-code: `G28.2K`, where K is one of the following letters:

| Axis Name                                   | Description                                                                      | Limit Switch Location                       |
| ------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------------- |
| X                                           | Gantry right (+X) and left (-X).                                                 | +X                                          |
| Y                                           | Gantry back, away from front window (+Y) and forward, towards front window (-Y). | +Y                                          |
| Z                                           | Left pipette mount up (+Z) and down (-Z).                                        | +Z                                          |
| A                                           | Right pipette mount up (+A) and down (-A).                                       | +A                                          |
| B                                           | Left pipette plunger up (+B) and down (-B).                                      | +B                                          |
| C                                           | Right pipette plunger up (+C) and down (-C).                                     | +C                                          |

The letter code indicates where the robot had issues homing; in our example, the "C" at the end of the error code indicates there was an issue with the right pipette plunger. Usually, re-homing the gantry will solve this issue - try running [`Troubleshooting_HomeGantry.py`](https://github.com/aldatubio/opentrons/blob/main/protocols/Troubleshooting/Troubleshooting_HomeGantry.py), which is a troubleshooting protocol located in `protocols/Troubleshooting`. If the issue persists, Opentrons has some [additional recommendations](https://support.opentrons.com/s/article/SmoothieError-Homing-fail).

### Hard limit
A hard limit error might look something like this:
```
SmoothieError:
2M907 A0.1 B0.3 C0.3 X0.3 Y0.3 Z0.8 G4P0.005 G0B2.5 returned ALARM: Hard limit +B
```

These types of errors will have the words `Hard limit` and a `+/-K` at the end of the error message, where `K` could be one of several letters. See the table in the "Homing fail" section for details on what this letter code indicates.

The most frequent hard limit errors seem to be those concerning the pipette plunger up/down (`+/-B` or `+/-C`) - the easiest way to troubleshoot these is to manually pull the pipette plunger down several times in a row to release any static electricity buildup. Usually this simple step fixes the problem; if the problem persists, Opentrons has some [additional recommendations](https://support.opentrons.com/s/article/SmoothieError-Hard-limit#:~:text=X%2FY%20%2D%20Gantry-,Description,%E2%80%9Chard%20limit%20%2BX.%E2%80%9D), or you can try out the [`Troubleshooting_HomeGantry.py`](https://github.com/aldatubio/opentrons/blob/main/protocols/Troubleshooting/Troubleshooting_HomeGantry.py) protocol, which moves the pipettors around to unstick axes/pipettors.


## Liquid handling
### Viscous liquids
Generally, issues with viscous liquids can be solved by using building block commands to access additional pipetting parameters.

#### Opentrons-provided resources
For in-depth guides that provide a multitude of fixes for volatile and viscous liquid handling, check out the links below. 
- **[Webinar: Viscous and volatile liquid handling](https://insights.opentrons.com/lp/webinar-01-11-23-tips-and-tricks-viscous-liquids-typ?submissionGuid=8d793e68-d66e-499f-9713-9c2d932e8856)** - includes code snippets (defining functions for repeat transfer of liquids)
- **[Support: Viscous liquid handling with Python API](https://support.opentrons.com/s/article/How-to-handle-viscous-liquids-in-the-Python-API)**
- **[PDF: Viscous liquid handling using the OT-2](https://opentrons-landing-img.s3.amazonaws.com/application+notes/Viscous+Liquids+App+Note.pdf)** - includes example code blocks, some of which are described in further detail below
- Note that Opentrons does not recommend using multi-dispense functionality with viscous liquids, as this can lead to inconsistent dispenses.

#### Liquid isn't dispensing completely, or air bubbles are present when aspirating
`InstrumentContext.aspirate()` and `InstrumentContext.dispense()` can take an additional argument that specifies a rate multiplier. See the bottom of Opentrons API v2's [Pipettes reference page](https://docs.opentrons.com/v2/new_pipette.html) for default speeds.

```python
p300.pick_up_tip()

# Aspirate at 115% of default speed
p300.aspirate(100, rack['A1'], 1.15)

# Dispense at 70% speed
p300.dispense(100, rack['A2'], 0.7)

p300.drop_tip()
```
#### Large droplets accumulating on pipette tip after aspirating
`InstrumentContext.touch_tip()` can take a vertical offset argument (in mm) - performing touch tip deeper within the source tube (negative offset value) can help shake off any particularly stubborn droplets. If this still doesn't work, try wrapping `InstrumentContext.touch_tip()` in a loop to perform the action several times in a row.
```python
p300.pick_up_tip()
p300.aspirate(100, rack['A1'])

# Without additional input, robot will touch tip in whatever well it most recently referenced
for i in range(3):
  p300.touch_tip(v_offset = -15)
  
p300.dispense(100, rack['A2'])
p300.drop_tip()
```

#### Large droplets present on pipette tip after dispensing
- If droplets are still present after dispensing, but before the blowout step, dispenses can be adjusted such that the pipette tip is touching the side of the destination well during the dispense step (visualized below).
- If droplets are still present after the blowout step, blowout speed can be reduced to ensure full elimination of any residual liquid. 
<p align = 'center'>
  <img src="https://user-images.githubusercontent.com/119699492/228574261-4521577d-c851-40c7-ac14-537117f60a42.png" width="782" height="357">
</p>

The code snippet below shows the use of both of these techniques to aspirate 100uL of liquid from a tube in A1 of a rack and dispense the liquid into A2 of the same rack. Note:
- In order to adjust tip location within a well using `types.Point(x,y,z)`, the import statement `from opentrons.types import Point` must be present at the top of the script.
- `InstrumentContext.blow_out()` does not take a rate modifier argument. Therefore, the blowout rate of the pipette itself must be changed, then changed back to its original value after blowout.
```python
from opentrons import protocol_api
from opentrons.types import Point

metadata = {
    'apiLevel': '2.13'
}

def run(protocol: protocol_api.ProtocolContext):
    
    protocol.home()
    
    p300tips = protocol.load_labware('opentrons_96_filtertiprack_200ul',3, 'tip rack')
    rack = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap',2, 'tube rack')
    
    p300 = protocol.load_instrument('p300_single_gen2', 'left', tip_racks = [p300tips])
    
    p300.pick_up_tip()
    p300.aspirate (
        100,
        rack['A1'],
        rate = 1.05     # 1.05x default rate
        )
    protocol.delay(20)
    p300.dispense(
        100,
        rack['A2'].top()                                # from default dispense location,
            .move(Point(x=(rack['A2'].diameter/2-1))),  # move 1 radius minus 1 mm in the x direction
        rate = 0.05                                     # 1/20th of default rate
        )
    
    # first, save the default blowout rate in a new variable
    default_p300_blowout = p300.flow_rate.blow_out
    # lower the blowout rate
    p300.flow_rate.blow_out = 10 #uL/s
    # blowout step 
    p300.blow_out()
    # change blowout rate back to saved default 
    p300.flow_rate.blow_out = default_p300_blowout
    
    
    p300.drop_tip()
    
    protocol.home()
 ```

### Robot is skipping wells when dispensing
Ensure the volume being dispensed is reasonable. Disregarding Opentrons recommendations, the P300 seems to be able to pipette as little as 10uL at a time; when pipetting 5uL, liquid randomly fails to be dispensed into some wells. Adjust pipetting steps and reagent concentrations to avoid pipetting volumes that are too small.

## Robot is using more tips than necessary
`InstrumentContext.distribute()` allows the user to specify when to get a new tip - `'never'` is a valid argument, but make sure that if you choose this, you're using `InstrumentContext.pick_up_tip()` and `InstrumentContext.drop_tip()` before and after distributing liquid.

Conversely, never use these tip pick-up/drop-off methods with liquid handling commands that *don't* have the `'never'` new-tip argument - this will cause an error.

```python
p300.pick_up_tip()

# Fill first four rows of plate
# Normally, this would require tip changes for every aspiration, but here we're forcing Opentrons to only use one tip
p300.distribute(
    25,
    reservoir['A1'],
    plate.rows()[:4],
    new_tip = 'never'
)

p300.drop_tip()
```

## Displaying in-app messages and adding pause steps
When scripts are run through Jupyter Notebook, each cell is independent and a pause step is automatically added between cells. Creating a more user-friendly Python script requires use of the `pause()` method. Optionally, you can add a display message argument. Note that this message will show up in the run log, and may not be obvious to those not closely watching the run log.
```python
protocol.pause()
protocol.pause('Run paused.')
```

As of 12-2022, OP13 has had issues getting these messages to display; the `comment()` method can be used as a workaround.
```python
protocol.pause()
protocol.comment('This message will appear in the run log.')
```

## Help with building block commands
When using building block commands, every step of liquid handling must be specified individually. Opentrons will throw an error if there is no tip attached and it is told to aspirate, or if there is still a tip attached and it is told to pick up a new tip.

```python
p300.pick_up_tip()
p300.aspirate(100, rack['A1'])
p300.dispense(100, rack['A2'])
p300.drop_tip()
```

`InstrumentContext.dispense()` provides powerful additional argument options, but lacks the multi-dispense function offered by complex commands like
`InstrumentContext.transfer()` and `InstrumentContext.distribute()`. To get around this, we have to get creative with nested loops.

Within well plates, Opentrons organizes wells by column, then by row. For example, wells 0-15 on a 384-well plate are wells A1 through P1; well A2 is number 16, well A3 is number 32, and so on. The following code example (from [8x8 Primer Screen](2022-11-17_8x8primerScreen.py)) fills the top half of a 384-well plate. Because of Opentrons' well organization system, this code iterates through pairs of columns instead of rows, as this allows for a nested loop that accesses each well within a column. Pairs of columns are used here to minimize aspirations while still maintaining simple loop logic.
```python
    p300.pick_up_tip()
    for column in range(12):
        p300.aspirate((mastermixVolume*17 + 10), mastermixes['A5'], 0.7)
        p300.dispense(mastermixVolume, mastermixes['A5'], 0.7)
        for i in range(3):
            p300.touch_tip(v_offset = -15)
        for well in range(8):
            p300.dispense(mastermixVolume, plate.wells()[well+(column*16)], 0.7)
            p300.touch_tip()
        for well in range(8):
            p300.dispense(mastermixVolume, plate.wells()[well+((column+12)*16)], 0.7)
            p300.touch_tip()
        p300.blow_out(mastermixes['A5'])
    p300.drop_tip()
```

## Troubleshooting scripts
Find troubleshooting scripts in `protocols\Troubleshooting`.
