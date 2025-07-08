# !bin/bash


for file in $(find Warehouse/ -maxdepth 2 -name "results*"); do
    name=$(echo $file | grep -o '[A-Z]\{2\}') # extracts configuration case

    echo "$name" # prints number of run in each match up
done