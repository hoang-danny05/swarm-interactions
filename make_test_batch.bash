# !bin/bash

find Warehouse/ -mindepth 1 -maxdepth 1 -type d -name '[A-Z][A-Z]' | head -n 36 | while read -r dir; do
    config=$(echo $dir | grep -o '[A-Z]\{2\}') 
    mkdir "Warehouse/testing/$config"
    #echo "$dir"
    #echo $config
    #files=$(find $dir -maxdepth 1 -type f -name "run4o*" | shuf -n 5)
    #echo $files
done