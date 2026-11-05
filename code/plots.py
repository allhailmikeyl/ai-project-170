# Aldrin's Angels
# CMSC 170 - EF-3L
# Project: Predicting Rice Price Movement using Weather Data
# File: plots.py (draws the charts from results/<method>.json, matplotlib is used here only)

import matplotlib.pyplot as plt # Draws the charts
import common # Shared constants and the results reader

# Turns a parameter set into a short label such as "k=3"
def param_label(params):
    parts = [] # Empty list for the "name=value" pieces
    for key in params:
        parts.append(f"{key}={params[key]}")
    return ", ".join(parts)

# Draws the validation macro-F1 of every parameter set, one chart per variety and one line per feature set
def plot_validation(method_name, output):
    if len(output["param_grid"]) < 2: # Nothing was tuned (such as Naive Bayes), so there is no curve to draw
        return
    fig, axes = plt.subplots(1, len(common.VARIETIES), figsize=(15, 4), sharey=True) # One panel per variety
    labels = [] # Text under each x position
    for params in output["param_grid"]:
        labels.append(param_label(params))
    positions = list(range(len(labels))) # Evenly spaced x positions

    for v in range(len(common.VARIETIES)):
        variety = common.VARIETIES[v]
        for feature_set in common.FEATURE_SET_NAMES: # One line per feature set
            scores = output["varieties"][variety]["feature_sets"][feature_set]["val_scores"]
            axes[v].plot(positions, scores, marker="o", label=feature_set.replace("_", " "))
        axes[v].set_title(variety.replace("price_", "").replace("_", "-"))
        axes[v].set_xticks(positions)
        axes[v].set_xticklabels(labels)
        axes[v].set_ylim(0, 1)
        axes[v].set_xlabel("Parameter set")
    axes[0].set_ylabel("Validation macro-F1 (2022)")
    axes[0].legend()
    fig.suptitle(f"{method_name}: validation macro-F1 per parameter set")
    fig.tight_layout()
    fig.savefig(f"{common.RESULTS_FOLDER}/{method_name}_validation.png", dpi=150)
    plt.close(fig)

# Draws the test macro-F1 of every method next to the two baselines, one chart per variety
def plot_test(all_results):
    methods = list(all_results.keys()) # Every method that has saved results
    fig, axes = plt.subplots(1, len(common.VARIETIES), figsize=(15, 4), sharey=True)
    width = 0.8 / len(methods) # Width of one bar

    for v in range(len(common.VARIETIES)):
        variety = common.VARIETIES[v]
        for m in range(len(methods)): # One bar per method in each feature set group
            scores = []
            for feature_set in common.FEATURE_SET_NAMES:
                scores.append(all_results[methods[m]]["varieties"][variety]["feature_sets"][feature_set]["test"]["macro_f1"])
            positions = []
            for i in range(len(scores)):
                positions.append(i + m * width)
            axes[v].bar(positions, scores, width, label=methods[m])

        baselines = all_results[methods[0]]["varieties"][variety]["baselines"] # Same for every method
        axes[v].axhline(baselines["Majority baseline"]["macro_f1"], color="gray", linestyle="--", label="majority")
        axes[v].axhline(baselines["Persistence baseline"]["macro_f1"], color="black", linestyle=":", label="persistence")
        axes[v].set_title(variety.replace("price_", "").replace("_", "-"))
        axes[v].set_xticks([0.4 - width / 2 + i for i in range(3)])
        axes[v].set_xticklabels(["price only", "weather only", "price + weather"])
        axes[v].set_ylim(0, 1)
    axes[0].set_ylabel("Test macro-F1 (2023)")
    axes[0].legend()
    fig.suptitle("Test macro-F1 against the baselines")
    fig.tight_layout()
    fig.savefig(f"{common.RESULTS_FOLDER}/test_comparison.png", dpi=150)
    plt.close(fig)

# Main Function
def main():
    all_results = common.load_results()
    for method_name in all_results:
        plot_validation(method_name, all_results[method_name])
    if len(all_results) > 0:
        plot_test(all_results)

if __name__ == "__main__":
    main()