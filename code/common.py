# Responsible Use of AI
# During the preparation of this work, the authors used Google AI (Gemini) and Claude (Anthropic) to assist in structuring the
# shared code for loading, splitting, scaling, tuning, and evaluating the dataset. After using these tools, the authors reviewed
# and edited the content as needed and take full responsibility for the content.

# Aldrin's Angels
# CMSC 170 - EF-3L
# Project: Predicting Rice Price Movement using Weather Data
# File: common.py (shared by all methods, so every method uses the same data, split, tuning, and scoring)

import csv # Reads the CSV file
import json # Writes the results files
import math # Used for the square root in the scaler
import os # Makes the results folder and lists its files

# Constants
CSV_FILE = "data/rice_per_weather.csv" # Input file name
RESULTS_FOLDER = "results" # Every method saves its results here
VARIETIES = ["price_well_milled", "price_regular_milled", "price_special"] # The three rice varieties, each modeled separately
ALL_WEATHER = ["temp_2m_mean", "temp_2m_max", "temp_2m_min", "precipitation_sum", "precipitation_hours",
               "wind_speed_10m_max", "wind_gusts_10m_max", "shortwave_radiation", "et0_fao_evapotranspiration"] # Every weather column in the CSV
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"] # Turns a month name into a number
FIRST_YEAR = 2020 # Month number 0 is January of this year
SEED = 170 # Fixed seed for any method that needs randomness (the perceptron)

# Feature vector layout: index 0 = price now, index 1 = price change, indices 2 to 10 = the nine weather columns
FEATURE_SET_NAMES = ["price_only", "weather_only", "price_weather"] # Order in which the feature sets are run
FEATURE_SETS = {"price_only": [0, 1],
                "weather_only": [2, 3, 4, 5, 6, 7, 8, 9, 10],
                "price_weather": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]} # Which feature indices each set keeps

# Month number t: 0 = Jan 2020 ... 47 = Dec 2023, and every range is inclusive
# Dec 2022 (t = 35) is skipped because its label comes from Jan 2023
TRAIN_RANGE = (1, 34) # Feature months for training, Feb 2020 to Nov 2022
TEST_RANGE = (36, 46) # Feature months for testing, Jan 2023 to Nov 2023
SUBTRAIN_RANGE = (1, 22) # For tuning, train on Feb 2020 to Nov 2021
VALIDATION_RANGE = (24, 34) # For tuning, validate on Jan 2022 to Nov 2022

# Turns a year and a month name into a month number (0 = January 2020)
def month_number(year, month_name):
    return (year - FIRST_YEAR) * 12 + MONTHS.index(month_name)

# Reads the dataset and returns {city: {month number: row}}
def load_dataset(filename):
    cities = {} # Empty dictionary for the rows of every city

    with open(filename, newline="", encoding="utf-8") as infile: # Read the file
        reader = csv.DictReader(infile) # Read each line as a dictionary keyed by the column name

        for row in reader: # Read each record in the given order
            t = month_number(int(row["year"]), row["month_year"]) # Month number of this record
            city = row["city_name"] # City of this record
            if city not in cities: # First time seeing this city
                cities[city] = {}
            cities[city][t] = row # Store the row under its month number

    return cities

# Builds one example for each city and month, returns a list of (t, feature vector, label)
# Feature vector: [price now, price now - price last month, nine weather columns...]
# Label: 1 if next month's price is higher, 0 if it is lower or unchanged
def build_examples(cities, price_column):
    examples = [] # Empty list for the examples

    for city in cities: # Loop through every city
        months = cities[city] # Rows of this city by month number
        for t in range(1, 47): # Needs month t - 1 and month t + 1 to exist
            price_now = float(months[t][price_column]) # Price this month
            price_before = float(months[t - 1][price_column]) # Price last month
            price_after = float(months[t + 1][price_column]) # Price next month

            record = [price_now, price_now - price_before] # Price features
            for column in ALL_WEATHER: # Add the weather of this month
                record.append(float(months[t][column]))

            if price_after > price_now: # Price went up
                label = 1
            else: # Price went down or stayed the same
                label = 0
            examples.append((t, record, label))

    return examples

# Returns the feature vectors and labels whose month number is inside the given range
def split_by_time(examples, month_range):
    features = [] # Empty list for the feature vectors
    labels = [] # Empty list for the labels

    for example in examples: # Loop through every example
        if example[0] >= month_range[0] and example[0] <= month_range[1]: # Month is inside the range
            features.append(example[1])
            labels.append(example[2])

    return features, labels

# Computes the mean and standard deviation of every feature (training rows only)
def fit_scaler(train_features):
    means = [] # Mean of each feature
    stds = [] # Standard deviation of each feature

    for j in range(len(train_features[0])): # Loop through every feature
        total = 0.0 # Running sum of the values
        for i in range(len(train_features)):
            total += train_features[i][j]
        mean = total / len(train_features)

        squares = 0.0 # Running sum of the squared differences
        for i in range(len(train_features)):
            squares += (train_features[i][j] - mean) ** 2
        std = math.sqrt(squares / len(train_features))
        if std == 0: # Avoid dividing by zero
            std = 1.0

        means.append(mean)
        stds.append(std)

    return means, stds

# Rescales every value to (value - mean) / std
def apply_scaler(features, means, stds):
    scaled = [] # Empty list for the scaled feature vectors

    for i in range(len(features)): # Loop through every feature vector
        record = []
        for j in range(len(features[i])): # Loop through every feature
            record.append((features[i][j] - means[j]) / stds[j])
        scaled.append(record)

    return scaled

# Builds everything for one rice variety, already split and scaled, returned as a dictionary (all 11 features are kept here)
# sub and val are for tuning (train 2020 to 2021, validate 2022)
# train and test are for the final run (train 2020 to 2022, test 2023)
# test_raw is the unscaled test features, which the persistence baseline needs
def prepare_data(cities, price_column):
    examples = build_examples(cities, price_column)

    sub_features, sub_labels = split_by_time(examples, SUBTRAIN_RANGE) # Tuning split
    val_features, val_labels = split_by_time(examples, VALIDATION_RANGE)
    means, stds = fit_scaler(sub_features) # Scaler fitted on the tuning training rows only
    sub = (apply_scaler(sub_features, means, stds), sub_labels)
    val = (apply_scaler(val_features, means, stds), val_labels)

    train_features, train_labels = split_by_time(examples, TRAIN_RANGE) # Final split
    test_features, test_labels = split_by_time(examples, TEST_RANGE)
    means, stds = fit_scaler(train_features) # Scaler fitted on the training rows only
    train = (apply_scaler(train_features, means, stds), train_labels)
    test = (apply_scaler(test_features, means, stds), test_labels)

    return {"sub": sub, "val": val, "train": train, "test": test, "test_raw": test_features, "price_column": price_column}

# Keeps only the feature indices given, in the given order
def select_features(features, indices):
    selected = [] # Empty list for the shorter feature vectors

    for i in range(len(features)): # Loop through every feature vector
        record = []
        for j in indices: # Keep only the chosen features
            record.append(features[i][j])
        selected.append(record)

    return selected

# Returns the four splits of one feature set as a dictionary (x = features, y = labels)
def get_split(data, feature_set):
    indices = FEATURE_SETS[feature_set] # Features this set keeps
    return {"sub_x": select_features(data["sub"][0], indices), "sub_y": data["sub"][1],
            "val_x": select_features(data["val"][0], indices), "val_y": data["val"][1],
            "train_x": select_features(data["train"][0], indices), "train_y": data["train"][1],
            "test_x": select_features(data["test"][0], indices), "test_y": data["test"][1]}

# Counts the confusion matrix (1 = up is the positive class)
def confusion_matrix(actual, predicted):
    tp = 0 # Predicted up, was up
    fp = 0 # Predicted up, was not up
    tn = 0 # Predicted not up, was not up
    fn = 0 # Predicted not up, was up

    for i in range(len(actual)): # Compare every actual label with its prediction
        if actual[i] == 1 and predicted[i] == 1:
            tp += 1
        elif actual[i] == 0 and predicted[i] == 1:
            fp += 1
        elif actual[i] == 0 and predicted[i] == 0:
            tn += 1
        else:
            fn += 1

    return tp, fp, tn, fn

# Divides a by b, and returns 0 when b is 0
def safe_divide(a, b):
    if b == 0:
        return 0.0
    return a / b

# Computes precision, recall, and F1 of one class
def precision_recall_f1(hits, false_alarms, misses):
    precision = safe_divide(hits, hits + false_alarms)
    recall = safe_divide(hits, hits + misses)
    f1 = safe_divide(2 * precision * recall, precision + recall)
    return precision, recall, f1

# Scores the predictions, returns a dictionary of the confusion matrix, accuracy, and macro-averaged metrics
def evaluate(actual, predicted):
    tp, fp, tn, fn = confusion_matrix(actual, predicted)
    accuracy = safe_divide(tp + tn, tp + fp + tn + fn)
    up_p, up_r, up_f1 = precision_recall_f1(tp, fp, fn) # Metrics of the "up" class
    down_p, down_r, down_f1 = precision_recall_f1(tn, fn, fp) # For "not up", the roles swap

    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "accuracy": accuracy,
            "macro_precision": (up_p + down_p) / 2, "macro_recall": (up_r + down_r) / 2,
            "macro_f1": (up_f1 + down_f1) / 2}

# Returns the line of a results table for one method
def result_line(name, r):
    return (f"{name:<24}{r['accuracy']:<10.3f}{r['macro_precision']:<10.3f}{r['macro_recall']:<10.3f}{r['macro_f1']:<10.3f}"
            f"TP={r['tp']} FP={r['fp']} TN={r['tn']} FN={r['fn']}")

# Returns the header line of a results table
def result_header():
    return f"{'Method':<24}{'Accuracy':<10}{'MacroP':<10}{'MacroR':<10}{'MacroF1':<10}Confusion matrix"

# Baseline 1: always predicts the more common label of the training set
def majority_baseline(train_labels, test_size):
    up_count = 0 # Number of "up" in the training labels
    for label in train_labels:
        up_count += label

    if up_count * 2 > len(train_labels): # "up" is the majority
        guess = 1
    else:
        guess = 0

    predicted = [] # Same guess for every test row
    for i in range(test_size):
        predicted.append(guess)
    return predicted

# Baseline 2: predicts "up" if the price already went up from last month to this month
def persistence_baseline(test_raw):
    predicted = [] # Empty list for the predictions

    for record in test_raw: # Feature 1 is the price change since last month
        if record[1] > 0:
            predicted.append(1)
        else:
            predicted.append(0)

    return predicted

# Scores both baselines on the test set, returns a list of (name, results)
def run_baselines(data):
    test_labels = data["test"][1]
    train_labels = data["train"][1]
    majority = evaluate(test_labels, majority_baseline(train_labels, len(test_labels)))
    persistence = evaluate(test_labels, persistence_baseline(data["test_raw"]))
    return [("Majority baseline", majority), ("Persistence baseline", persistence)]

# Tunes one method on the validation year, then scores the best setting once on the test year
# predict_many(train_x, train_y, test_x, param_list) must return one list of predictions for each parameter set
def tune_and_test(predict_many, param_grid, split):
    val_predictions = predict_many(split["sub_x"], split["sub_y"], split["val_x"], param_grid) # Train on 2020 to 2021, predict 2022
    val_scores = [] # Validation macro-F1 of each parameter set
    best_index = 0 # Index of the best parameter set so far

    for i in range(len(param_grid)): # Score every parameter set
        score = evaluate(split["val_y"], val_predictions[i])["macro_f1"]
        val_scores.append(score)
        if score > val_scores[best_index]: # Strictly better, so a tie keeps the earlier parameter set
            best_index = i

    best_params = param_grid[best_index]
    test_predictions = predict_many(split["train_x"], split["train_y"], split["test_x"], [best_params]) # Train on 2020 to 2022, predict 2023
    test_result = evaluate(split["test_y"], test_predictions[0])
    return best_params, val_scores, test_result

# Runs one method on all 27 configurations (3 varieties x 3 feature sets x the method), saves and returns the results
def run_all(method_name, predict_many, param_grid):
    cities = load_dataset(CSV_FILE)
    output = {"method": method_name, "param_grid": param_grid, "varieties": {}} # Everything that gets saved

    for variety in VARIETIES: # Each rice variety is modeled separately
        data = prepare_data(cities, variety)
        entry = {"baselines": {}, "feature_sets": {}}
        print(f"\n=== {method_name} | {variety} ===")
        print(result_header())

        for name, result in run_baselines(data): # Baselines do not depend on the feature set
            entry["baselines"][name] = result
            print(result_line(name, result))

        for feature_set in FEATURE_SET_NAMES: # Price only, weather only, price + weather
            split = get_split(data, feature_set)
            best_params, val_scores, test_result = tune_and_test(predict_many, param_grid, split)
            entry["feature_sets"][feature_set] = {"best_params": best_params, "val_scores": val_scores, "test": test_result}
            print(result_line(f"{method_name} ({feature_set})", test_result) + f"  best={best_params}")

        output["varieties"][variety] = entry

    save_results(method_name, output)
    return output

# Saves the results of one method as results/<method>.json
def save_results(method_name, output):
    os.makedirs(RESULTS_FOLDER, exist_ok=True) # Make the folder if it is missing
    with open(f"{RESULTS_FOLDER}/{method_name}.json", "w", encoding="utf-8") as outfile:
        json.dump(output, outfile, indent=2)

# Reads every results/<method>.json and returns {method: results}
def load_results():
    all_results = {} # Empty dictionary for the results of every method
    if not os.path.isdir(RESULTS_FOLDER): # Nothing has been saved yet
        return all_results

    files = os.listdir(RESULTS_FOLDER)
    files.sort() # Same order on every computer
    for filename in files:
        if filename.endswith(".json"):
            with open(f"{RESULTS_FOLDER}/{filename}", encoding="utf-8") as infile:
                all_results[filename[:-5]] = json.load(infile)

    return all_results

# Combines every results/<method>.json into results/results.js for the webpage
def write_results_js():
    all_results = load_results()
    with open(f"{RESULTS_FOLDER}/results.js", "w", encoding="utf-8") as outfile:
        outfile.write("const RESULTS = " + json.dumps(all_results, indent=2) + ";\n")