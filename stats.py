import os
import json
import numpy as np
import pandas as pd
import scipy
import itertools

def resultsDF(directory, filename, tocsv=False) -> pd.DataFrame:
    """
    Takes the run directories, results to export the data as a dataframe object. Optionally exports data to csv
    Args:
        directory (str): Directory of all runs.
        filename (str): Name of the results file.
        tocsv (bool): Whether to export to CSV. Defaults to False.
    Returns:
        pd.DataFrame: The result data as a DataFrame.
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
    
    # for all configs AA, AB ...
    for comb in itertools.product("ABCDEF", "ABCDEF"):
        config = "".join(comb)
        fullfile = directory + config +'/'+filename
        # print(f"Analyzing file: {fullfile}")

        with open(fullfile, 'r') as file:
            raw = json.load(file)

            # raw = file.read()
            # # Trim at "Results" key if present
            # if '"Results":' in raw:
            #     raw = raw.split('"Results":')[0].rstrip(', \n\t')
            #     raw += '}'
                
            # the result data
            d = raw["Results"]
            result = dict()
            result["Arrangement"] = str(config)
            for key in d:
                if key == "Results": break 
                if key == "SuccessfulFiles": break # skip successful files
                result[key] = d[key]
            rows.append(result)
    df = pd.DataFrame(rows)
    if tocsv==True:df.to_csv(os.path.join(os.getcwd(), f"stats_data/data.csv"))
    return pd.DataFrame(rows)

def df_to_pairwise(data, tocsv=False) -> pd.DataFrame:
    """
    Takes a dataframe and returns a second data frame with outcomes of matches with player vs player.
    Args:
        data (pd.DataFrame): Pandas dataframe of the wins
        tocsv (bool): Whether to export to CSV. Defaults to False.
    Returns:
        pd.DataFrame: Returns the pairwise dataframe to be used in bradley-terry ranking.
    """
    pairwise = []

    for _, row in data.iterrows():
        arrangement = row['Arrangement']
        #Assuming Oppenhimer is first
        pairwise.append({"P1":arrangement[0], 
                        "P2": arrangement[1],
                        "W1": row['Oppenheimer'],
                        "W2": row['Barbie']
                        })
    if tocsv==True:df.to_csv(os.path.join(os.getcwd(), f"stats_data/pair_wise_data.csv"))
    return pd.DataFrame(pairwise)

def pairwise_to_win_matrix(df, return_players=False, tocsv=False):
    """
    Takes a dataframe of pairwise wins, and returns a numpy win matrix, and a list of players.
    Args:
        df (pd.DataFrame): Pandas dataframe of the pairwise wins
        return_players (bool): whether to return players.
        tocsv (bool): Whether to export to CSV. Defaults to false. 
    Returns:
        W (pd.DataFrame): Returns the pairwise dataframe to be used in bradley-terry ranking.
        players (dict): Returns a dictionary of the players corresponding to a column index in the pairwise dataframe.
    """
    players = pd.unique(df[['P1', 'P2']].values.ravel())
    players.sort()
    player_indices = {name: idx for idx, name in enumerate(players)}

    # Initialize win matrix
    n = len(players)
    W = np.zeros((n, n), dtype=int)

    # Populate the win matrix
    for _, row in df.iterrows():
        p1, p2 = row['P1'], row['P2']
        w1, w2 = int(row['W1']), int(row['W2'])

        i, j = player_indices[p1], player_indices[p2]
        W[i, j] += w1  # P1 beats P2 w1 times
        W[j, i] += w2  # P2 beats P1 w2 times
    
    if tocsv==True:
        df = pd.DataFrame(W)
        df.columns = ["A","B","C","D","E","F"]
        df.to_csv(os.path.join(os.getcwd(), f"stats_data/win_matrix.csv"))
    if return_players: return W, players
    else: return W

def bradley_terry_ranking(W, players, print_stats=False, tocsv=False, max_iter=10000, tol=1e-6):
    """
    Perform Bradley-Terry ranking from a win matrix W.

    Args:
        W (ndarray): A square numpy array where W[i, j] is number of wins of i over j.
        players (array): A string array of players to rank.
        print_stats (bool): Option to print how many iterations to converge.
        tocsv (bool): Whether to export to CSV. Defaults to false.  
        max_iter (int): Maximum number of iterations.
        tol (float): Convergence tolerance.

    Returns:
        rankings (dict): A dictionary with skill scores for each player (normalized).
    """
    n = W.shape[0]
    r = np.ones(n)  # initial ratings

    for iteration in range(max_iter):
        r_old = r.copy()
        for i in range(n):
            denom_sum = 0
            for j in range(n):
                if i != j:
                    denom_sum += (W[i, j] + W[j, i]) / (r[i] + r[j])
            r[i] = np.sum(W[i, :]) / denom_sum if denom_sum > 0 else r[i]

        # Normalize
        r /= np.sum(r)

        # Check convergence
        if np.linalg.norm(r - r_old, ord=1) < tol:
            if print_stats: print(f"Converged in {iteration + 1} iterations.")
            break

    rankings = {k: v for k, v in zip(players, r)}

    if tocsv==True:
        df = pd.DataFrame(list(rankings.items()), columns=["Key", "Value"])
        df.to_csv(os.path.join(os.getcwd(), f"stats_data/bradley_terry_rankings.csv"))
    return rankings

filename = 'results_NEW_run4o.json'
directory = 'Warehouse/'

data = resultsDF(directory=directory, filename=filename, tocsv=True)


print('-'*100)
print("Total number of runs is: "+str(data['Total'].sum()))
print('-'*100)
df = df_to_pairwise(data)

W, players = pairwise_to_win_matrix(df, return_players=True, tocsv=True)

rankings = bradley_terry_ranking(W, players, print_stats=True, tocsv=True)

print("******** Rankings ********")
for key, item in rankings.items():
    print(f"Player {key} with {item}")


# 96 * log( A over B)

print(players)
print(W)

gathered_strengths = list(rankings.values())

def calculate_log_likelihood(strengths):
    sum = 0
    for i in range(len(players)):
        for j in range(len(players)):
            if i != j:
                # wins of I over J * probability I wins over J
                sum += W[i][j] * np.log((strengths[i])/(strengths[i]+strengths[j]))
    return sum

print("NULL")
null_sum = calculate_log_likelihood(np.ones(6)/6)

print("DATA")
data_sum = calculate_log_likelihood(gathered_strengths)

# chi^2 sample statistic
g2 = 2*(data_sum-null_sum)

print(f"{g2 = }")
df = 5

pvalue = scipy.stats.chi2.cdf(g2, df)

print(f"{pvalue = }")



