# AI Project 170

This repository contains the source code and project website for **AI Project 170**, a machine learning project that predicts whether the retail price of rice in a Philippine city will increase, decrease, or stay the same in the following month using historical rice prices and weather data.

**Course:** CMSC 170 - EF-3L  
**Group:** Aldrin's Angels

## Project Page

**[Visit the AI Project 170 Website](https://allhailmikeyl.github.io/ai-project-170/)**

Explore the project's problem statement, datasets, machine learning methods, experimental setup, results, and conclusions.

## Group Members

- Alvis, Franchesca Niña Marie M.
- Belonio, Yvonne Mari C.
- Bulatao, Nestor Victus T.
- Perlas, Mikhail Adrian Jude S.

## Project Overview

The project explores the use of machine learning to predict the direction of retail rice price changes in Philippine cities.

### Machine Learning Methods

The project uses three classification algorithms:

- **K-Nearest Neighbors (KNN)** – Classifies price movement based on the nearest data points.
- **Naive Bayes** – Uses probability-based classification.
- **Perceptron** – Uses a linear classification approach.

### Feature Sets

The models are evaluated using three different feature sets:

- **Price-only** – Uses historical rice price information.
- **Weather-only** – Uses weather-related information.
- **Price + Weather** – Combines rice price and weather information.

## Folder Structure

```text
ai-project-170/
│
├── code/
│   ├── common.py
│   ├── knn.py
│   ├── main.py
│   ├── naive_bayes.py
│   ├── perceptron.py
│   └── plots.py
│
├── data/
│   ├── raw_rice.csv
│   ├── raw_weather.csv
│   └── rice_per_weather.csv
│
├── images/
│   ├── hero-rice.jpg
│   ├── icon-moon.png
│   └── icon-sun.png
│
├── results/
│   ├── knn.json
│   ├── naive_bayes.json
│   ├── perceptron.json
│   └── results.js
│
├── .gitignore
├── index.html
├── README.md
├── script.js
└── styles.css
```

## Requirements

### Prerequisites

- **Python 3.x**
- **Matplotlib**
- **Git** (for cloning the repository)
- A modern web browser (for viewing the project website)

### Technologies Used

- **Python** – Machine learning implementation and data processing.
- **HTML5** – Project website structure.
- **CSS3** – Website styling and layout.
- **JavaScript** – Website interactions and results visualization.
- **Matplotlib** – Generation of machine learning plots.

## Local Setup and Execution

### 1. Clone the repository

```bash
git clone https://github.com/allhailmikeyl/ai-project-170.git
cd ai-project-170
```

### 2. Install dependencies

Install Matplotlib:

```bash
pip install matplotlib
```

### 3. Run the project

From the repository's root directory, execute:

```bash
python code/main.py
```

This runs the three machine learning methods and generates the corresponding results and visualizations.

To run an individual method:

```bash
python code/main.py knn
python code/main.py naive_bayes
python code/main.py perceptron
```

### 4. View the project website

Open `index.html` in a web browser to view the website locally.

The website uses the generated `results/results.js` file to display the machine learning results. Make sure this file is present in the repository.

The deployed website is also available through GitHub Pages:

**[https://allhailmikeyl.github.io/ai-project-170/](https://allhailmikeyl.github.io/ai-project-170/)**

## Data Sources

The project uses the following datasets:

1. **PSA OpenSTAT – Retail Prices of Agricultural Commodities (Cereals)**

   [PSA OpenSTAT](https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__2M__2018NEW/0042M4ARN01.px/?rxid=ce15d7b1-4c83-4f0a-a151-6619d027ddd5)

2. **Philippine Cities Weather Data (2020–2023)**

   [Kaggle Dataset](https://www.kaggle.com/datasets/bwandowando/philippine-cities-weather-data-2020-2023?select=daily_data_combined_2020_to_2023.csv)

The datasets were processed and combined to create the project's final dataset, `rice_per_weather.csv`.
