#!/bin/bash

# -f file / -d directory

# single brackets are obsolete - double brackets are modern

if [[ -d "new_folder" ]]; then
    mkdir if_folder
fi

if [[ -d "if_folder"]]; then
    mkdir hyperionDev
else
    mkdir new-projects
fi