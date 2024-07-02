param (
    [Parameter(Mandatory=$true, ValueFromPipeline=$true)]
    [string]$CsvFilePath
)

# Validate CSV file
if (-not (Test-Path $CsvFilePath -PathType Leaf)) {
    Write-Host "File '$CsvFilePath' does not exist or is not a valid CSV file."
    exit 1
}

# Log the received file path
Write-Output "Received file path: $CsvFilePath"

# Define SSH details
$remoteHost_1 = "root@10.225.42.84"  # 7B10 robot
$remoteHost_2 = "root@10.225.40.186" # 8B04 robot
$remotePath = "/data/user_storage/aldatubio"

# Path to scp executable (OpenSSH)


try {  
    # Execute scp command to copy the file using SSH key authentication
    # Wrap variable names in curly brackets when next to colon - otherwise, script won't work
    scp -i "C:/Users/lucy/ot2_ssh_key" "$CsvFilePath" "${remoteHost_1}:${remotePath}"
    scp -i "C:/Users/lucy/ot2_ssh_key" "$CsvFilePath" "${remoteHost_2}:${remotePath}"
    Write-Host "File copied successfully!"
}
catch {
    Write-Host "Error copying file: $_"
}
