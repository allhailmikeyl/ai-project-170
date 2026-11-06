# Aldrin's Angels
# CMSC 170 - EF-3L
# Project: You Rice Me Up: (Subtitle)
# File: main.py (runs the methods one after the other, then draws the charts)
# Run from the project folder with: python code/main.py (everything) or python code/main.py knn (only the methods you name)

import importlib # Loads a method by its name
import sys # Reads what was typed after main.py

# Constants
METHODS = ["knn", "naive_bayes", "perceptron"] # Every method, each file has a main() that saves its results

# Main Function
def main():
    chosen = sys.argv[1:] # Names typed after main.py, such as knn
    if len(chosen) == 0: # Nothing typed, so run every method
        chosen = METHODS

    for name in chosen:
        if name not in METHODS:
            print(f"Unknown method '{name}', choose from {METHODS}")
            return

    for name in chosen: # One after the other
        print(f"\n########## {name} ##########")
        method = importlib.import_module(name) # Same as import knn, import naive_bayes, import perceptron
        method.main() # Tune, test, print, and save results/<method>.json and results/results.js

    import plots # Imported here so the results are already saved even if matplotlib is missing
    plots.main() # Draw the charts from every results/<method>.json
    print("\nDone. Charts are in results/, and results.js is ready for the webpage.")

if __name__ == "__main__":
    main()