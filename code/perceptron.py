# Responsible Use of AI
# During the preparation of this work, the author used ChatGPT and Claude to assist in understanding the algorithm for Perceptron and double-checking the implementation
# After using this tool, the author reviewed and edited the content as needed and take(s) full responsibility for the content.

# Aldrin's Angels
# CMSC 170 - EF-3L
# Project: You Rice Me Up: (Subtitle)
# File: perceptron.py (Perceptron, adapted from Exercise 08)

import random # For shuffling the training order each epoch
import common # Shared data, split, tuning, and scoring

# Constants
LEARNING_RATES = [0.001, 0.01, 0.1] # Values of the learning rate to try (change or shrink this list if you want)
MAX_EPOCHS = [10, 50, 100] # Stopping condition, the rice data is not linearly separable, so it will usually run to the limit

# Every parameter set to try, one per combination
PARAM_GRID = []
for rate in LEARNING_RATES:
    for epochs in MAX_EPOCHS:
        PARAM_GRID.append({"learning_rate": rate, "max_epochs": epochs})

# Computes the linear combiner output: v = sum of (w_i * x_i)
def linear_combiner(x, w):
    # Same as Exercise 08, but here x does not have x0 in it yet (see train), so decide where the bias weight goes
    # w[0] is the bias weight (its input x0 is always 1), and w[i + 1] goes with x[i]
    v = w[0] # w0 * x0, where x0 = 1
    for i in range(len(x)):
        v += w[i + 1] * x[i]
    return v

# Computes the actual response using the threshold function (+1 or -1)
def activation(v):
    # Same as Exercise 08: +1 if v >= 0, otherwise -1
    if v >= 0:
        return 1
    return -1

# Trains the weights on the training rows, returns the final weights (w0 is the bias weight)
def train(train_features, train_labels, learning_rate, max_epochs):
    rng = random.Random(common.SEED) # Fixed seed, so every run gives the same results
    weights = [0.0] * (len(train_features[0]) + 1) # One weight per feature plus the bias weight w0

    order = list(range(len(train_features))) # Row positions, shuffled every epoch

    for epoch in range(max_epochs): # Stopping condition 1: reached the epoch limit
        rng.shuffle(order)
        errors = 0 # Number of misclassified rows in this epoch

        for j in order:
            x = train_features[j]
            if train_labels[j] == 1: # Desired response d: +1 for "up", -1 for "not up"
                d = 1
            else:
                d = -1

            y = activation(linear_combiner(x, weights)) # Actual response

            if y != d: # Wrong prediction, so adjust the weights: w = w + learning_rate * (d - y) * x
                errors += 1
                change = learning_rate * (d - y)
                weights[0] += change # Bias weight, x0 = 1
                for i in range(len(x)):
                    weights[i + 1] += change * x[i]

        if errors == 0: # Stopping condition 2: every row is classified correctly
            break

    return weights

# Predicts the label of one vector (1 = up, 0 = not up)
def predict(x, weights):
    if activation(linear_combiner(x, weights)) == 1:
        return 1
    return 0

# Predicts every test vector for every parameter set, returns one list of predictions for each parameter set
def predict_many(train_features, train_labels, test_features, param_grid):
    all_predictions = []

    for params in param_grid:
        weights = train(train_features, train_labels, params["learning_rate"], params["max_epochs"])

        predictions = [] # List of predictions for this parameter set
        for x in test_features:
            predictions.append(predict(x, weights))
        all_predictions.append(predictions)

    return all_predictions

# Main Function
def main():
    common.run_all("perceptron", predict_many, PARAM_GRID) # Tune, test, print, and save results/perceptron.json
    common.write_results_js() # Refresh results/results.js for the webpage

if __name__ == "__main__":
    main()