# Responsible Use of AI
# During the preparation of this work, the author used []
# After using this tool, the author reviewed and edited the content as needed and take(s)
# full responsibility for the content.

# Aldrin's Angels
# CMSC 170 - EF-3L
# Project: Predicting Rice Price Movement using Weather Data
# File: naive_bayes.py (Gaussian Naive Bayes, adapted from Exercise 04)

import common # Shared data, split, tuning, and scoring
import math # For log, sqrt, and pi

# Constants
# Exercise 04 used Laplace smoothing (k) because the features were word counts
# Here the features are continuous, so each feature is modeled as a Gaussian per class, and the smoothing becomes a tiny
# number added to every variance so it is never 0 (a feature with the same value in every row would divide by zero)
VARIANCE_FLOORS = [1e-9, 1e-6, 1e-3, 1e-1] # Values to try on the validation year (change or shrink this list if you want)

# Every parameter set to try, one per value above
PARAM_GRID = []
for floor in VARIANCE_FLOORS:
    PARAM_GRID.append({"variance_floor": floor})

# Learns what Naive Bayes needs from the training rows, returns the priors, means, and variances of each class
def fit(train_features, train_labels):
    pass

# Computes log of the Gaussian density of one value: log P(x_i | class)
def log_gaussian(value, mean, variance):
    pass

# Computes the score of one class for one vector: log P(class) + sum of log P(x_i | class)
def class_score(x, prior, means, variances, variance_floor):
    pass

# Predicts the label of one vector (1 = up, 0 = not up)
def predict(x, model, variance_floor):
    pass

# Predicts every test vector for every parameter set, returns one list of predictions for each parameter set
def predict_many(train_features, train_labels, test_features, param_grid):
    pass

# Main Function
def main():
    common.run_all("naive_bayes", predict_many, PARAM_GRID) # Tune, test, print, and save results/naive_bayes.json
    common.write_results_js() # Refresh results/results.js for the webpage

if __name__ == "__main__":
    main()