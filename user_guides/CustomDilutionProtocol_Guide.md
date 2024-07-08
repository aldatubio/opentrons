# Custom Dilution Protocol - How to use
This guide walks you through the use of the custom dilutions protocol:
1. Making a custom dilution series and saving it as a CSV file
2. Uploading the dilution series to the robot using the `Upload CSV to Opentrons` drag-and-drop widget
3. Clicking on the `Freetown | Custom Dilution Series` protocol in the Opentrons app and following the app's instructions

## Creating a custom dilution series
In an Excel file with the columns shown, list the dilutions you'd like the robot to perform. (Do not include any manually-prepared dilutions in this file.) Using the "Save As" option in Excel, save this workbook as `Dilution Series.csv`, ensuring that you've selected the `CSV - UTF-8` save option from the drop-down menu. 
<p align = "left">
  <img src = "https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20125841.png"
    width = "50%">
</p>
    
> :warning: **Warning:** Your file *must* have the name `Dilution Series.csv`, because the Opentrons app doesn't allow for custom text input yet.
</br>

## Uploading the dilution series file to the robot
Transfer your new CSV file to the lab's Opentrons laptop, either via thumb drive or upload to the L drive. Ensure the robot is turned on.
</br>

On the laptop's desktop, there is a widget: `Upload CSV to Opentrons`. Drag-and-drop your CSV file onto this widget.
<p float = "left" align = "left">
  <img src = "https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20130017.png"
    width = "34%" />
  <img src = "https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20130037.png"
    width = "50%" />
</p>

</br>

## Loading protocol parameters
Open the Opentrons app and select the protocol `Freetown | Custom Dilution Series`.
<p align = "left">
  <img src = "https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20130059.png"
    width = "75%">
</p>

On the next page, click the blue `Start setup` button.
<p align = "left">
  <img src = "https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20130120.png"
    width = "75%">
</p>

Use the next two screens to choose the robot you want, as well as pipettes and diluent tube size. 
<p float = "left" align = "left">
  <img src = "https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20130554.png"
    width = "29%" />
  <img src = "https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20130621.png"
    width = "30%" />
</p>

[Image 1]: https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20125841.png
[Image 2]: https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20130017.png
[Image 3]: https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20130037.png
[Image 4]: https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20130059.png
[Image 5]: https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20130120.png
[Image 6]: https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20130554.png
[Image 7]: https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20130621.png
[Image 8]: https://github.com/aldatubio/opentrons/blob/main/dev/images/custom_dil_guide/Screenshot%202024-07-08%20130656.png
