# Step-by-step: implementing user-friendly CSV functionality
## PowerShell scripting
### Setting up and using SSH
To set up SSH, I used Opentrons' setup guide [here](https://support.opentrons.com/s/article/Setting-up-SSH-access-to-your-OT-2). There is no password for the SSH key pair.
The basic SSH command to connect to a robot is as follows:
```pwsh
ssh -i ot2_ssh_key root@ROBOT_IP
```
Find robot IP addresses by opening the Opentrons app, then navigating to **Devices** > robot > **Robot Settings** > **Networking**. Generally, you'll want to use the **Wireless IP**.
</br>

After establishing a key pair, I used Opentrons' file copying guide [here](https://support.opentrons.com/s/article/Copying-files-to-and-from-your-OT-2-with-SCP) to experiment with file uploading/downloading. The commands discussed in this linked Opentrons guide formed the basis for my PowerShell script (further down on this page).
- After establishing an SSH connection, you can use Linux commands as usual to navigate around the robot's file structure: `mkdir`, `rm`, etc.
- As outlined in the Opentrons guide, there are two folders on the robot where the user can save files: `/data/user_storage` and `/var/lib/jupyter/notebooks`. I made a folder for files to get saved to: `\data\user_storage\aldatubio`.
- To close an SSH session, type `exit`.

### Writing a PowerShell script
There's plenty of tutorials out there for PowerShell. These are some I found useful:
- [PowerShell crash course - brief reference](https://www.finitewisdom.com/blogs/joshua-golub/2020/11/27/a-crash-course-in-powershell-scripting)
- [PowerShell tutorial - in-depth](https://powershellbyexample.dev/)
- [Using parameters in PowerShell functions](https://www.techtarget.com/searchwindowsserver/tip/Understanding-the-parameters-of-Windows-PowerShell-functions)

### CopyCsvToSSH.ps1
A more robust version of this script, with some error handling, is available in the `dev` folder of this repository; I'm copying the basics here as a general framework.
```pwsh
param (
    [Parameter(Mandatory=$true, ValueFromPipeline=$true)]
    [string]$CsvFilePath
)
$remoteHost_1 = "root@10.225.42.84"  # 7B10 robot
$remoteHost_2 = "root@10.225.40.186" # 8B04 robot
$remotePath = "/data/user_storage/aldatubio" # location on robot
$sshKeyLocation = "C:/Users/username/ot2_ssh_key" # location on your computer - replace 'username' with your name

# Wrap variable names in curly brackets when next to colon - otherwise, script won't work
scp -i "$sshKeyLocation" "$CsvFilePath" "${remoteHost_1}:${remotePath}"
scp -i "$sshKeyLocation" "$CsvFilePath" "${remoteHost_2}:${remotePath}"
```

### Making a drag-and-drop shortcut
- Create the shortcut:
  - Right-click on your desktop or in a folder where you want the shortcut.
  - Choose *New -> Shortcut*.
  - In the location field, enter `powershell.exe -File "C:\path\to\your\CopyCsvToSSH.ps1"`, replacing `"C:\path\to\your\CopyCsvToSSH.ps1"` with the actual path to your PowerShell script.
  - Name the shortcut something meaningful, like *Copy CSV to SSH*.
- Make sure the shortcut is working:
  - Right-click on the shortcut you created (*Copy CSV to SSH*) and choose `Properties`.
  - In the `Target` field, make sure the path to your script is correct.
  - Click `Apply` and `OK`.

## Troubleshooting
- [Drag-and-drop .bat wrapper script](https://gist.github.com/jpoehls/1469460) - turn echo on to show more extensive error messages in command-line; also helps to ensure that drag-and-drop is working properly
