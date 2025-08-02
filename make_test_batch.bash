# !bin/bash

: << 'COMMENT'
This is a script to sample a subset of the runs in the parent Warehouse/ directory and copy them into Warehouse/testing/.
It logs the runs in sampled_files.txt. I am curently lazy to integrate commandline arguments.
Notes:
    1) Change '[A-Z][A-Z]' on line 13 to a specific subdirectory (ex.'AE'), to sample from there
    2) Change the '5' in shuf -n 5, on line 15, to another integer to sample n runs.
    3) Comment out: touch sampled_files.txt, once the log has been made.
COMMENT

touch sampled_files.txt
find Warehouse/ -mindepth 1 -maxdepth 1 -type d -name '[A-Z][A-Z]' | head -n 36 | while read -r dir; do
    config=$(echo $dir | grep -o '[A-Z]\{2\}') 
    find $dir -type f -name "run4o*" | shuf -n 5 | while read -r file; do
        echo $file >> sampled_files.txt
        name=$(echo $file | sed -n 's/.*\(run4o.*\)/\1/p')
        cp "$file" "Warehouse/testing/$config" 
    done

done