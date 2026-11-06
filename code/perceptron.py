# Responsible Use of AI
# During the preparation of this work, the author used []
# After using this tool, the author reviewed and edited the content as needed and take(s)
# full responsibility for the content.

# Aldrin's Angels
# CMSC 170 - EF-3L
# Project: Predicting Rice Price Movement using Weather Data
# File: perceptron.py (Perceptron, adapted from Exercise 08)

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
    pass

# Computes the actual response using the threshold function (+1 or -1)
def activation(v):
    # Same as Exercise 08: +1 if v >= 0, otherwise -1
    pass

# Trains the weights on the training rows, returns the final weights (w0 is the bias weight)
def train(train_features, train_labels, learning_rate, max_epochs):
    pass

# Predicts the label of one vector (1 = up, 0 = not up)
def predict(x, weights):
    pass

# Predicts every test vector for every parameter set, returns one list of predictions for each parameter set
def predict_many(train_features, train_labels, test_features, param_grid):
    pass

# Main Function
def main():
    common.run_all("perceptron", predict_many, PARAM_GRID) # Tune, test, print, and save results/perceptron.json
    common.write_results_js() # Refresh results/results.js for the webpage

if __name__ == "__main__":
    main()