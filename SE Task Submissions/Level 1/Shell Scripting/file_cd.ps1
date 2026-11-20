New-Item -ItemType Directory -Name "folder1"
New-Item -ItemType Directory -Name "folder2"
New-Item -ItemType Directory -Name "folder3"

Set-Location folder1

New-Item -ItemType Directory -Name "folder4"
New-Item -ItemType Directory -Name "folder5"
New-Item -ItemType Directory -Name "folder6"

Set-Location ..

Remove-Item "folder2" -Recurse