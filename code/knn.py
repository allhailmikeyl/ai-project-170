# Responsible Use of AI
# During the preparation of this work, the author used Google AI (Gemini) and Claude (Anthropic) to assist in adapting the KNN
# implementation from Exercise 06 to the group project. After using these tools, the author reviewed and edited the content
# as needed and take(s) full responsibility for the content.

# Aldrin's Angels
# CMSC 170 - EF-3L
# Project: You Rice Me Up: (Subtitle)
# File: knn.py (K-Nearest Neighbors, adapted from Exercise 06)

import common # Shared data, split, tuning, and scoring

# Constants
K_VALUES = [1, 3, 5, 7, 9, 11, 15, 21, 31, 51] # Values of k tried on the validation year
P = 2 # Minkowski parameter, 2 is the Euclidean distance

# Every parameter set to try, one per k
PARAM_GRID = []
for k_value in K_VALUES:
    PARAM_GRID.append({"k": k_value})

# Computes the Minkowski distance without the final root: d = sum of |x_i - v_i|^p
# The p-th root is skipped because it does not change which points are the nearest
def minkowski_distance(x, v, p):
    total = 0.0 # Running sum of the differences
    for i in range(len(x)): # Loop through every feature
        total += abs(x[i] - v[i]) ** p # |x_i - v_i|^p
    return total

# Finds the k nearest neighbors of x as a list of (distance, label), sorted from the closest
def nearest_neighbors(x, train_features, train_labels, k, p):
    nearest = [] # The k nearest neighbors so far as (distance, label)

    for j in range(len(train_features)): # Loop through every training vector
        d = minkowski_distance(x, train_features[j], p) # Distance from x to v

        if len(nearest) < k or d < nearest[-1][0]: # Fewer than k neighbors, or closer than the farthest one
            position = len(nearest) # By default, d goes at the end
            for m in range(len(nearest)): # Find where d belongs in the sorted list
                if d < nearest[m][0]: # First neighbor that is farther than d
                    position = m
                    break
            nearest.insert(position, (d, train_labels[j])) # Remember it, list stays sorted by distance
            if len(nearest) > k: # Too many neighbors now
                nearest.pop() # Remove the farthest one

    return nearest

# Predicts 1 (up) or 0 (not up) from the first k neighbors by majority vote
def vote(nearest, k):
    up_count = 0 # Number of "up" among the k neighbors
    for m in range(k): # Count the label of each neighbor
        up_count += nearest[m][1]
    not_up_count = k - up_count # Number of "not up" among the k neighbors

    if up_count > not_up_count: # "up" has the maximum count
        return 1
    elif not_up_count > up_count: # "not up" has the maximum count
        return 0

    return nearest[0][1] # Tie (even k), use the class of the closest neighbor

# Predicts every test vector for every parameter set, the neighbors are searched once using the largest k
def predict_many(train_features, train_labels, test_features, param_grid):
    max_k = 0 # Largest k in the grid
    for params in param_grid:
        if params["k"] > max_k:
            max_k = params["k"]

    predictions = [] # One list of predictions for each parameter set
    for i in range(len(param_grid)):
        predictions.append([])

    for x in test_features: # Classify every test vector
        nearest = nearest_neighbors(x, train_features, train_labels, max_k, P)
        for i in range(len(param_grid)): # Reuse the same neighbors for every k
            predictions[i].append(vote(nearest, param_grid[i]["k"]))

    return predictions

# Main Function
def main():
    common.run_all("knn", predict_many, PARAM_GRID) # Tune, test, print, and save results/knn.json
    common.write_results_js() # Refresh results/results.js for the webpage

if __name__ == "__main__":
    main()