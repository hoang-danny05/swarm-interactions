#!bin/bash

: << 'COMMENT'
This is a script to batch run our agent match-ups. It handels a few cases:
1. Checks if the runs are distributed unevenly and starts to run match-ups with the lowest runs to even everything out.
2. If all runs are the same/even the script runs an additional #number of runs per each matchup. 
COMMENT

declare -A myhash


update_myhash(){
    # updates the associative array 
    for file in $(find Warehouse/ -maxdepth 2 -name "results*"); do
        name=$(echo $file | grep -o '[A-Z]\{2\}') # extracts configuration case
        num=$(grep '"Total"' "$file" | grep -o '[0-9]\+') # gets number of runs in each match up
        myhash[$name]=$num
    done
}

for file in $(find Warehouse/ -maxdepth 2 -name "results*"); do
    name=$(echo $file | grep -o '[A-Z]\{2\}') # extracts configuration case
    num=$(grep '"Total"' "$file" | grep -o '[0-9]\+') # gets number of runs in each match up
    myhash[$name]=$num
    echo "Number of runs for $name is: $num" # prints number of run in each match up
done

min=$(for key in "${!myhash[@]}"; do echo "${myhash[$key]}"; done | sort -n | head -n 1)
max=$(for key in "${!myhash[@]}"; do echo "${myhash[$key]}"; done | sort -n | tail -n 1)

echo "The min of run is: $min; The max of the runs is: $max"

if [ "$min" -ne "$max" ]; then

    read -p "Would you like to top off the runs? 0 for yes 1 for no:   " top_off
    if [ "$top_off" == 1 ]; then
        
        read -p "Enter an integer amount of runs you would like to run in this session : " user_run_info
        count=1
        for ((i = 1; i <= user_run_info; i++)); do
            for key in "${!myhash[@]}"; do 
                if [ "${myhash[$key]}" == $min ]; then
                    foundkey="$key"
                fi
            done 
            echo "The key for the lowest amount of runs is: $foundkey"
            echo "****************************************************** STARTING RUN NUMBER: $count FOR CONFIGURATION $foundkey ******************************************************"

            # run assertiveness_observer with the proper key
            python assertiveness_observer.py "$foundkey" # I think this is how the positional argument works
            # Revaluate to prioritize lowest runs
            update_myhash
            min=$(for key in "${!myhash[@]}"; do echo "${myhash[$key]}"; done | sort -n | head -n 1)
            max=$(for key in "${!myhash[@]}"; do echo "${myhash[$key]}"; done | sort -n | tail -n 1)
            echo "****************************************************** COMPLETED RUN NUMBER: $count ******************************************************"
            ((count++))
            if [ "$min" == "$max" ]; then
                echo "runs are now even, exiting early"
                break
            fi
        done
    # Block where top off is carried out.
    else 
        echo # top off the runs; while {have to lowest run case populate until it equals the max; run lines 18-19 to check values finish when all are equal} 
    fi

# block where if all number of runs are even, the number of runs per each matchup is carried out
else
    echo # Here there should be a block to carry out the runs on each match-up
    read -p "How many runs per match-up would you like to perform:  " user_run_info
    for key in "${!myhash[@]}"; do
        echo " Completing runs for $key ..."
        for ((i = 1; i <= user_run_info; i++)); do
            # run assertiveness_observer with the proper key
            python assertiveness_observer.py "$key" # I think this is how the positional argument works
        done
    done
fi