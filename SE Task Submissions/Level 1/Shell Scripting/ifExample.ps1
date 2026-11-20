$NewFolder = ".\new_folder"

if (Test-Path $NewFolder) {
    New-Item -Path "if_folder" -ItemType Directory
}

$IfFolder = ".\if_folder"

if (Test-Path $IfFolder) {
    New-Item -Path "hyperionDev" -ItemType Directory
} else {
    New-Item -Path "new-projects" -ItemType Directory
}