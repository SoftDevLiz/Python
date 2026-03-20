New-Item -Path "Shell Scripting 1" -ItemType Directory
New-Item -Path "Shell Scripting 2" -ItemType Directory
New-Item -Path "Shell Scripting 3" -ItemType Directory

$Folder = "C:\Users\lizmo\Desktop\Hyperiondev\Python\Shell Scripting 2"

if (Test-Path $Folder) {
    Set-Location $Folder
    Write-Host "You're in!"

    New-Item -Path "Sub Folder 1" -ItemType Directory
    New-Item -Path "Sub Folder 2" -ItemType Directory
    New-Item -Path "Sub Folder 3" -ItemType Directory

    Set-Location ..

    Remove-Item -Path ".\Shell Scripting 1"
    Remove-Item -Path ".\Shell Scripting 3"

} else {
    Write-Host "No such folder exists"
}



