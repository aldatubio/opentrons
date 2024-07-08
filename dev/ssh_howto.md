# Step-by-step: implementing user-friendly CSV functionality
## Setting up and using SSH
To set up SSH, I used Opentrons' setup guide [here](https://support.opentrons.com/s/article/Setting-up-SSH-access-to-your-OT-2). There is no password for the SSH key pair.
The basic SSH command to connect to a robot is as follows:
```pwsh
ssh -i ot2_ssh_key root@ROBOT_IP
```
Find robot IP addresses by opening the Opentrons app, then navigating to **Devices** > robot > **Robot Settings** > **Networking**. Generally, you'll want to use the **Wireless IP**.
</br>

After establishing a key pair, I used Opentrons' file copying guide [here](https://support.opentrons.com/s/article/Copying-files-to-and-from-your-OT-2-with-SCP) to experiment with file uploading/downloading.
- After establishing an SSH connection, you can use Linux commands as usual to navigate around the robot's file structure: `mkdir`, `rm`, etc.
- To close an SSH session, type `exit`.




## Making a drag-and-drop shortcut
- Create the shortcut:
  - Right-click on your desktop or in a folder where you want the shortcut.
  - Choose *New -> Shortcut*.
  - In the location field, enter `powershell.exe -File "C:\path\to\your\CopyCsvToSSH.ps1"`, replacing `"C:\path\to\your\CopyCsvToSSH.ps1"` with the actual path to your PowerShell script.
  - Name the shortcut something meaningful, like *Copy CSV to SSH*.
- Make sure the shortcut is working:
  - Right-click on the shortcut you created (*Copy CSV to SSH*) and choose `Properties`.
  - In the `Target` field, make sure the path to your script is correct.
  - Click `Apply` and `OK`.

## File structure
- Upload/download files to this location in the Opentrons SSH: `/data/user_storage/aldatubio`
- You can also access Jupyter Notebook through SSH (or, alternately, use Jupyter Notebook as another place to upload files to the robot).

## Troubleshooting
- [Drag-and-drop .bat wrapper script](https://gist.github.com/jpoehls/1469460) - turn echo on to show more extensive error messages in command-line; also helps to ensure that drag-and-drop is working properly


## Reference links - a work in progress
- **[Drag-and-drop files onto PowerShell scripts](https://stackoverflow.com/questions/2819908/drag-and-drop-to-a-powershell-script/67655089#67655089)**
- **[PowerShell crash course - brief reference](https://www.finitewisdom.com/blogs/joshua-golub/2020/11/27/a-crash-course-in-powershell-scripting)**
- **[PowerShell tutorial - in-depth](https://powershellbyexample.dev/)**
- **[Using parameters in PowerShell functions](https://www.techtarget.com/searchwindowsserver/tip/Understanding-the-parameters-of-Windows-PowerShell-functions)**
- **[Learn Windows PowerShell in a Month of Lunches - video series](https://www.youtube.com/playlist?list=PL6D474E721138865A)**
