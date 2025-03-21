import scipy.stats as stats
import os
import json
import numpy as np

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