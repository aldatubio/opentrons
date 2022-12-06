# Troubleshooting
This guide contains code snippets and script references for problems we've encountered in the past (hardware and software) and the software solutions we used to fix or get around these problems.

See also: [Opentrons API Version 2 Reference](https://docs.opentrons.com/v2/new_protocol_api.html)

**Contents**
- [Liquid handling](#liquid-handling)
  - [Viscous liquids](#viscous-liquids)
  - [Robot skips wells](#robot-is-skipping-wells-when-dispensing)
- [Decreasing tip usage](#robot-is-using-more-tips-than-necessary)
- [Displaying in-app messages and adding pause steps](#displaying-in-app-messages-and-adding-pause-steps)
- [Help with building block commands](#help-with-building-block-commands)
- [Copy-and-paste troubleshooting scripts](#copy-and-paste-troubleshooting-scripts)

## Liquid handling
### Viscous liquids
Generally, issues with viscous liquids can be solved by using building block commands to access additional pipetting parameters.

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

### Robot is skipping wells when dispensing
Make sure the volume being dispensed is reasonable. Disregarding Opentrons recommendations, the P300 seems to be able to pipette as little as 10uL at a time; when pipetting 5uL, liquid would randomly fail to be dispensed into some wells. Adjust pipetting steps and reagent concentrations to avoid pipetting volumes that are too small.

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
p300.aspirate(100, rack['A1])
p300.dispense(100, rack['A2'])
p300.drop_tip()
```

`InstrumentContext.dispense()` provides powerful additional argument options, but lacks the multi-dispense function offered by complex commands like
`InstrumentContext.transfer()` and `InstrumentContext.distribute()`. To get around this, we have to get creative with nested loops.

Within well plates, Opentrons organizes wells by column, then by row. For example, wells 1-16 on a 384-well plate are wells A1 through P1; well A2 is number 17, well A3 is number 33, and so on. The following code example (from [8x8 Primer Screen](2022-11-17_8x8primerScreen.py)) fills the top half of a 384-well plate. Because of Opentrons' well organization system, this code iterates through pairs of columns instead of rows, as this allows for a nested loop that accesses each well within a column. Pairs of columns are used here to minimize aspirations while still maintaining simple loop logic.
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
