#!/bin/bash

# Straight forward

 mkdir folder1
 mkdir folder2
 mkdir folder3

 cd folder1

 mkdir folder4
 mkdir folder5
 mkdir folder6

 cd ..

 rmdir folder2
 rmdir folder3

# A bit more complex

# for i in {1..3}; do
#     mkdir "folder_$i"
# done

# cd folder_1

# for i in {4..6}; do
#     mkdir "folder_$i"
# done

# cd ..

# rmdir folder_2
# rmdir folder_3