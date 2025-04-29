import os
import json
import numpy as np
import pandas as pd
import choix
'''
def chitestNprint(observed):
    chi2_stat, p_value, dof, expected = stats.chi2_contingency(observed)
    
    print(f"Chi-square Statistic: {chi2_stat:.4f}")
    print(f"P-value: {p_value:.4f}")
    print(f"Degrees of Freedom: {dof}")
    print("Expected Frequencies:")
    print(np.round(expected, 3)) 

    return chi2_stat, p_value, dof, expected

filenames = ["./Warehouse/BB/results_run4o.json","./Warehouse/BA/results_run4o.json",
             "./Warehouse/AB/results_run4o.json","./Warehouse/AA/results_run4o.json"]

observations = np.empty((4,3))
for i, name in enumerate(filenames):
    data = json.load(open(name))
    observations[i,:] = [data["PajamaWins"], data["FormalWins"], data['NoWins']]

print(observations)

chi2_stat, p_value, dof, expected = chitestNprint(np.transpose(observations)) 
'''

def resultsDF(directory, filename, tocsv=False):
    """
    Takes the run directories, results to export the data as a dataframe object. Optionally exports data to csv
    params:
        directory: str  
            A string containing the directory of all runs
        filename: str
            A string containing the filename of the results
        tocsv: bool
            Default false. If yes exports
    """
    col = [
    "Arrangement",
    "Oppenheimer",
    "Barbie",
    "NoWins",
    "Compromise",
    "TokenLimitExceeded",
    "ConfusedIdentity",
    "Total",
    ]
    rows = []
    for i in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, i)) and len(i)==2:
            fullfile = directory+i+'/'+filename

            with open(fullfile, 'r') as file:
                d = json.load(file)
                result = {}
                result["Arrangement"] = str(i)
                for key in d:
                    if key == "Results": break
                    result[key] = d[key]
                rows.append(result)
    df = pd.DataFrame(rows)
    if tocsv==True:df.to_csv(os.path.join(os.getcwd(), "pairwise_data.csv"), index=False)
    return pd.DataFrame(rows)

filename = 'results_run4o_discovery.json'
directory = './Warehouse/'

data = resultsDF(directory=directory, filename=filename, tocsv=True)

print(data.head())

pairwise = []

for _, row in data.iterrows():
    arrangement = row['Arrangement']
    #Assuming Oppenhimer is first
    pairwise.append({"P1":arrangement[0], 
                     "P2": arrangement[1],
                     "W1": row['Oppenheimer'],
                     "W2": row['Barbie']
                     })
    
df = pd.DataFrame(pairwise)
