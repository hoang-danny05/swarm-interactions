# !bin/bash

touch sampled_files.txt
find Warehouse/ -mindepth 1 -maxdepth 1 -type d -name '[A-Z][A-Z]' | head -n 36 | while read -r dir; do
    config=$(echo $dir | grep -o '[A-Z]\{2\}') 
    find $dir -type f -name "run4o*" | shuf -n 5 | while read -r file; do
        echo $file >> sampled_files.txt
        name=$(echo $file | sed -n 's/.*\(run4o.*\)/\1/p')
        cp "$file" "Warehouse/testing/$config" 
    done

done