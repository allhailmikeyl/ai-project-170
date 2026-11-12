# Responsible Use of AI
# During the preparation of this work, the author used ChatGPT and Claude to assist in understanding the algorithm for Naive-Bayes and double-checking the implementation
# After using this tool, the author reviewed and edited the content as needed and take(s)
# full responsibility for the content.

# Aldrin's Angels
# CMSC 170 - EF-3L
# Project: You Rice Me Up: (Subtitle)
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
def fit(train_features, train_labels, variance_floor):
    # Initialize the priors, means, and variances dictionaries
    # key = class_label (0, 1) ; value = priors/means/variances of the class
    priors = {0: None, 1: None}
    means = {0: None, 1: None}
    variances = {0: None, 1: None}

    for class_label in [0, 1]:
        # Holds the rows of the corresponding class
        class_rows = []

        # Loop through the train_labels
        for i, label in enumerate(train_labels):
            # Check if the label of current train_features is equal to current class_label
            # If so, append it to class_rows
            if label == class_label:
                class_rows.append(train_features[i])
        
        # Compute for class_prior 
        class_prior = len(class_rows) / len(train_features)

        # Set the prior of current class_label to the computed class_prior
        priors[class_label] = class_prior

        # Initialize the list that will hold the feature means and variances
        feature_means = []
        feature_variances = []
        for i in range(len(class_rows[0])):
            # Holds the values of feature i from each row
            features = []
            for row in class_rows:
                # Append feature i of current row
                features.append(row[i])
            
            # Compute for the feature_mean and append it to feature_means
            feature_mean = sum(features) / len(class_rows)
            feature_means.append(feature_mean)

            # FORMULA FROM: https://python.plainenglish.io/calculating-variance-and-standard-deviation-from-the-user-input-in-python-987866064638
            deviation = sum((x - feature_mean)**2 for x in features)
            variance = deviation / len(features)
            
            # Add variance_floor to variance
            variance += variance_floor

            # Append variance to feature_variances
            feature_variances.append(variance)

        # Set the means & variances of current class_label to computed feature_means and feature_variances
        means[class_label] = feature_means
        variances[class_label] = feature_variances
    
    # Create a model dictionary that contains the priors, means, and variances
    model = {
        "priors": priors,
        "means": means,
        "variances": variances
    }

    return model

# Computes log of the Gaussian density of one value: log P(x_i | class)
def log_gaussian(value, mean, variance):
    log_probability = -0.5 * math.log(2 * math.pi * variance) - ((value - mean)**2 / (2 * variance))

    return log_probability

# Computes the score of one class for one vector: log P(class) + sum of log P(x_i | class)
def class_score(x, prior, means, variances):
    score = math.log(prior)

    for i in range(len(x)):
        feature_score = log_gaussian(x[i], means[i], variances[i])
        score += feature_score

    return score

# Predicts the label of one vector (1 = up, 0 = not up)
def predict(x, model):
    # Get the priors, means, and variances from the model dictionary
    priors = model["priors"]
    means = model["means"]
    variances = model["variances"]

    # Get class_score of down label (key = 0)
    down_score = class_score(x, priors[0], means[0], variances[0])

    # Get class_score of up label (key = 1)
    up_score = class_score(x, priors[1], means[1], variances[1])

    # Compare the scores and return the class/label with a larger score
    if up_score > down_score:
        return 1
    else:
        return 0

# Predicts every test vector for every parameter set, returns one list of predictions for each parameter set
def predict_many(train_features, train_labels, test_features, param_grid):
    all_predictions = []

    for param in param_grid:
        # Get variance floor from param
        variance_floor = param["variance_floor"]

        # Get model (priors, means, and variances) from training data
        model = fit(train_features, train_labels, variance_floor)

        # List of predictions for this param
        predictions = []
        for x in test_features:
            predicted_label = predict(x, model)
            predictions.append(predicted_label)

        # Append the prediction for this param to all_predictions
        all_predictions.append(predictions)

    return all_predictions

# Main Function
def main():
    common.run_all("naive_bayes", predict_many, PARAM_GRID) # Tune, test, print, and save results/naive_bayes.json
    common.write_results_js() # Refresh results/results.js for the webpage

if __name__ == "__main__":
    main()