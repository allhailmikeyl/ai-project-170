// Aldrin's Angels
// CMSC 170 - EF-3L
// Project: You Rice Me Up: Predicting Philippine Rice Price Movements from Weather
// File: script.js (draws the tables and charts of the Results section from results/results.js)

// Constants
var METHOD_ORDER = ["knn", "naive_bayes", "perceptron"]; // Order of the methods in tables and charts
var METHOD_NAMES = {knn: "kNN", naive_bayes: "Naive Bayes", perceptron: "Perceptron"};
var VARIETY_NAMES = {price_well_milled: "Well-milled", price_regular_milled: "Regular-milled", price_special: "Special"};
var FEATURE_SETS = ["price_only", "weather_only", "price_weather"]; // Order of the feature sets
var FEATURE_NAMES = {price_only: "Price only", weather_only: "Weather only", price_weather: "Price + weather"};
var DEFAULT_VARIETY = "price_regular_milled"; // Tab that is open first

// Chart size (the SVG scales to the width of the page)
var CW = 640; // Width
var CH = 300; // Height
var ML = 48; // Left margin
var MR = 16; // Right margin
var MT = 16; // Top margin
var MB = 60; // Bottom margin

// Formats a number with three decimals
function fmt(x) {
  return x.toFixed(3);
}

// Returns the method keys that have results, in the order of METHOD_ORDER
function methodKeys() {
  var keys = []; // Empty list for the method keys
  for (var i = 0; i < METHOD_ORDER.length; i++) {
    if (RESULTS[METHOD_ORDER[i]]) {
      keys.push(METHOD_ORDER[i]);
    }
  }
  for (var key in RESULTS) { // Any method that is not in METHOD_ORDER goes last
    if (keys.indexOf(key) === -1) {
      keys.push(key);
    }
  }
  return keys;
}

// Returns the display name of a method
function methodName(key) {
  return METHOD_NAMES[key] || key;
}

// Turns a parameter set into text such as "k=3"
function paramText(params) {
  var parts = []; // Empty list for the "name=value" pieces
  for (var key in params) {
    parts.push(key + "=" + params[key]);
  }
  return parts.join(", ");
}

// Turns a parameter set into a short tick label such as "0.01/50"
function tickText(params) {
  var parts = []; // Empty list for the values
  for (var key in params) {
    parts.push(params[key]);
  }
  return parts.join("/");
}

// Returns the legend of a chart, one item for each series and one dashed item for each baseline line
function legend(items, refs) {
  var html = '<ul class="ch-legend">'; // Start of the list
  for (var i = 0; i < items.length; i++) {
    html += '<li class="s' + (i + 1) + '"><span class="ch-swatch"></span>' + items[i] + '</li>';
  }
  for (var r = 0; r < (refs || []).length; r++) {
    html += '<li><span class="ch-swatch-ref r' + (r + 1) + '"></span>' + refs[r].name + ' baseline ' + refs[r].value.toFixed(2) + '</li>';
  }
  return html + '</ul>';
}

// Returns the opening of a chart: the grid, the y labels, and the axis titles
function chartFrame(ariaLabel, xTitle) {
  var ph = CH - MT - MB; // Height of the plot area
  var html = '<svg class="chart" viewBox="0 0 ' + CW + ' ' + CH + '" role="img" aria-label="' + ariaLabel + '">';
  for (var g = 0; g <= 4; g++) { // Grid lines at 0, 0.25, 0.5, 0.75, 1
    var y = MT + ph * (1 - g / 4);
    html += '<line class="ch-grid" x1="' + ML + '" x2="' + (CW - MR) + '" y1="' + y + '" y2="' + y + '"/>';
    html += '<text class="ch-ylab" x="' + (ML - 8) + '" y="' + (y + 4) + '">' + (g / 4).toFixed(2) + '</text>';
  }
  html += '<text class="ch-title" transform="rotate(-90)" x="' + (-(MT + ph / 2)) + '" y="12">Macro-F1</text>';
  html += '<text class="ch-title" x="' + (ML + (CW - ML - MR) / 2) + '" y="' + (CH - 6) + '">' + xTitle + '</text>';
  return html;
}

// Returns the x labels under the plot, rotated when they would not fit
function xLabels(labels) {
  var pw = CW - ML - MR; // Width of the plot area
  var step = pw / labels.length; // Width of one tick
  var longest = 0; // Length of the longest label
  for (var i = 0; i < labels.length; i++) {
    if (String(labels[i]).length > longest) {
      longest = String(labels[i]).length;
    }
  }
  var rotate = longest * 6.5 > step; // Labels would overlap
  var html = ""; // Start of the labels
  var y = CH - MB + 16; // Baseline of the labels
  for (var j = 0; j < labels.length; j++) {
    var x = ML + (j + 0.5) * step;
    if (rotate) {
      html += '<text class="ch-xlab rot" transform="rotate(-35 ' + x + ' ' + y + ')" x="' + x + '" y="' + y + '">' + labels[j] + '</text>';
    } else {
      html += '<text class="ch-xlab" x="' + x + '" y="' + y + '">' + labels[j] + '</text>';
    }
  }
  return html;
}

// Draws a line chart, series is a list of {name, values, best} and best is the index of the chosen setting
function lineChart(ariaLabel, xTitle, labels, series) {
  var pw = CW - ML - MR; // Width of the plot area
  var ph = CH - MT - MB; // Height of the plot area
  var step = pw / labels.length; // Width of one tick
  var html = chartFrame(ariaLabel, xTitle) + xLabels(labels);

  for (var s = 0; s < series.length; s++) { // One line for every series
    var path = ""; // Points of the line
    var dots = ""; // Dots on the line
    for (var i = 0; i < series[s].values.length; i++) {
      var x = ML + (i + 0.5) * step;
      var y = MT + ph * (1 - series[s].values[i]);
      path += (i === 0 ? "M" : "L") + x.toFixed(1) + " " + y.toFixed(1) + " ";
      dots += '<circle class="ch-dot" cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="3.5"><title>' +
              series[s].name + ", " + labels[i] + ": " + fmt(series[s].values[i]) + '</title></circle>';
      if (i === series[s].best) { // Ring around the setting chosen on validation
        dots += '<circle class="ch-ring" cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="7"/>';
      }
    }
    html += '<g class="s' + (s + 1) + '"><path class="ch-line" d="' + path + '"/>' + dots + '</g>';
  }
  return html + '</svg>';
}

// Draws grouped bars, series is a list of {name, values}, refs is a list of {name, value} drawn as dashed lines
function barChart(ariaLabel, xTitle, labels, series, refs) {
  var pw = CW - ML - MR; // Width of the plot area
  var ph = CH - MT - MB; // Height of the plot area
  var group = pw / labels.length; // Width of one group
  var bar = (group * 0.7) / series.length; // Width of one bar
  var html = chartFrame(ariaLabel, xTitle) + xLabels(labels);

  for (var s = 0; s < series.length; s++) { // One bar of every series in each group
    var bars = ""; // Bars of this series
    for (var g = 0; g < series[s].values.length; g++) {
      var v = series[s].values[g];
      var x = ML + g * group + group * 0.15 + s * bar;
      var y = MT + ph * (1 - v);
      bars += '<rect class="ch-bar" x="' + x.toFixed(1) + '" y="' + y.toFixed(1) + '" width="' + (bar - 2).toFixed(1) +
              '" height="' + (ph * v).toFixed(1) + '"><title>' + series[s].name + ", " + labels[g] + ": " + fmt(v) + '</title></rect>';
      bars += '<text class="ch-val" x="' + (x + (bar - 2) / 2).toFixed(1) + '" y="' + (y - 4).toFixed(1) + '">' + v.toFixed(2) + '</text>';
    }
    html += '<g class="s' + (s + 1) + '">' + bars + '</g>';
  }

  for (var r = 0; r < refs.length; r++) { // Baselines as dashed lines
    var ry = MT + ph * (1 - refs[r].value);
    html += '<line class="ch-ref r' + (r + 1) + '" x1="' + ML + '" x2="' + (CW - MR) + '" y1="' + ry.toFixed(1) + '" y2="' + ry.toFixed(1) + '"/>';
  }
  return html + '</svg>';
}

// Returns the table of the test results of one variety (baselines first, then every method on every feature set)
function resultsTable(variety, keys) {
  var rows = []; // Rows of {method, features, result, tuned}
  var baselines = RESULTS[keys[0]].varieties[variety].baselines;
  for (var name in baselines) {
    rows.push({method: name, features: "-", result: baselines[name], tuned: "-"});
  }
  for (var m = 0; m < keys.length; m++) {
    for (var f = 0; f < FEATURE_SETS.length; f++) {
      var entry = RESULTS[keys[m]].varieties[variety].feature_sets[FEATURE_SETS[f]];
      if (entry) {
        rows.push({method: methodName(keys[m]), features: FEATURE_NAMES[FEATURE_SETS[f]], result: entry.test,
                   tuned: paramText(entry.best_params) || "-"});
      }
    }
  }

  var best = 0; // Row with the highest macro-F1
  for (var i = 1; i < rows.length; i++) {
    if (rows[i].result.macro_f1 > rows[best].result.macro_f1) {
      best = i;
    }
  }

  var html = '<div class="table-scroll"><table class="results-table"><thead><tr><th>Method</th><th>Features</th>' +
             '<th class="num">Accuracy</th><th class="num">Macro-P</th><th class="num">Macro-R</th><th class="num">Macro-F1</th>' +
             '<th>Tuned</th></tr></thead><tbody>';
  for (var j = 0; j < rows.length; j++) {
    var r = rows[j].result;
    html += '<tr' + (j === best ? ' class="best-row"' : '') + '><td>' + rows[j].method + '</td><td>' + rows[j].features + '</td>' +
            '<td class="num">' + fmt(r.accuracy) + '</td><td class="num">' + fmt(r.macro_precision) + '</td>' +
            '<td class="num">' + fmt(r.macro_recall) + '</td><td class="num">' + fmt(r.macro_f1) + '</td>' +
            '<td class="tuned">' + rows[j].tuned + '</td></tr>';
  }
  return html + '</tbody></table></div>';
}

// Returns the bar chart of the test macro-F1 of every method on every feature set, with the baselines
function testChart(variety, keys) {
  var labels = []; // One group for each feature set
  for (var f = 0; f < FEATURE_SETS.length; f++) {
    labels.push(FEATURE_NAMES[FEATURE_SETS[f]]);
  }

  var series = []; // One series for each method
  var names = []; // Names for the legend
  for (var m = 0; m < keys.length; m++) {
    var values = []; // Test macro-F1 of this method on each feature set
    for (var g = 0; g < FEATURE_SETS.length; g++) {
      values.push(RESULTS[keys[m]].varieties[variety].feature_sets[FEATURE_SETS[g]].test.macro_f1);
    }
    series.push({name: methodName(keys[m]), values: values});
    names.push(methodName(keys[m]));
  }

  var baselines = RESULTS[keys[0]].varieties[variety].baselines; // Same for every method
  var refs = [
    {name: "Majority", value: baselines["Majority baseline"].macro_f1},
    {name: "Persistence", value: baselines["Persistence baseline"].macro_f1}
  ];
  return legend(names, refs) + barChart("Test macro-F1 of every method on every feature set", "Feature set", labels, series, refs);
}

// Returns the line chart of the validation macro-F1 of one method, with a table of the values
function validationChart(key, variety) {
  var result = RESULTS[key]; // Results of this method
  var grid = result.param_grid; // Parameter sets that were tried
  var labels = []; // Tick label of each parameter set
  for (var i = 0; i < grid.length; i++) {
    labels.push(tickText(grid[i]));
  }
  var xTitle = Object.keys(grid[0]).join(" / "); // Name of the parameters

  var series = []; // One line for each feature set
  var names = []; // Names for the legend
  for (var f = 0; f < FEATURE_SETS.length; f++) {
    var entry = result.varieties[variety].feature_sets[FEATURE_SETS[f]];
    var best = 0; // Index of the parameter set chosen on validation
    for (var j = 0; j < grid.length; j++) {
      if (paramText(grid[j]) === paramText(entry.best_params)) {
        best = j;
      }
    }
    series.push({name: FEATURE_NAMES[FEATURE_SETS[f]], values: entry.val_scores, best: best});
    names.push(FEATURE_NAMES[FEATURE_SETS[f]]);
  }

  var html = '<h4>' + methodName(key) + '</h4>' + legend(names) +
             lineChart(methodName(key) + " validation macro-F1 for each parameter set", xTitle, labels, series);

  html += '<details class="values"><summary>Show values</summary><div class="table-scroll"><table><thead><tr><th>' + xTitle + '</th>';
  for (var s = 0; s < series.length; s++) {
    html += '<th class="num">' + series[s].name + '</th>';
  }
  html += '</tr></thead><tbody>';
  for (var p = 0; p < grid.length; p++) {
    html += '<tr><td>' + paramText(grid[p]) + '</td>';
    for (var t = 0; t < series.length; t++) {
      html += '<td class="num">' + fmt(series[t].values[p]) + '</td>';
    }
    html += '</tr>';
  }
  return html + '</tbody></table></div></details>';
}

// Returns one sentence that says how the best model did against the persistence baseline (worked out from the results)
function takeaway(variety, keys) {
  var persistence = RESULTS[keys[0]].varieties[variety].baselines["Persistence baseline"].macro_f1;
  var best = null; // Best model so far as {name, features, f1}
  var beat = 0; // Number of models that scored above the persistence baseline
  var count = 0; // Number of models (methods x feature sets)

  for (var m = 0; m < keys.length; m++) {
    for (var f = 0; f < FEATURE_SETS.length; f++) {
      var entry = RESULTS[keys[m]].varieties[variety].feature_sets[FEATURE_SETS[f]];
      if (!entry) {
        continue;
      }
      count++;
      var f1 = entry.test.macro_f1;
      if (f1 > persistence) {
        beat++;
      }
      if (best === null || f1 > best.f1) {
        best = {name: methodName(keys[m]), features: FEATURE_NAMES[FEATURE_SETS[f]].toLowerCase(), f1: f1};
      }
    }
  }

  return '<p class="takeaway"><strong>Best model:</strong> ' + best.name + ' (' + best.features + '), with a macro-F1 of ' + fmt(best.f1) +
         ', against ' + fmt(persistence) + ' for the persistence baseline (repeating last month’s direction). ' +
         beat + ' of ' + count + ' model and feature set combinations ' + (beat === 1 ? 'beats' : 'beat') + ' it.</p>';
}

// Returns one cell of a confusion matrix, its color gets darker as it holds a larger share of its row
function confusionCell(kind, name, count, rowTotal) {
  var share = rowTotal === 0 ? 0 : count / rowTotal; // Share of the actual class that ended up here
  var mix = Math.round(6 + share * 49); // How much of the color is mixed in (kept low so the text stays readable)
  return '<td class="' + kind + '" style="--mix:' + mix + '%"><b>' + count.toLocaleString("en-US") + '</b><span>' +
         name + ' · ' + Math.round(share * 100) + '%</span></td>';
}

// Returns the 2 x 2 confusion matrix of one result with a caption (rows = what happened, columns = what was predicted)
function confusionFigure(label, r) {
  var ups = r.tp + r.fn; // Rows that really went up
  var downs = r.tn + r.fp; // Rows that really did not go up
  return '<figure class="cm"><figcaption>' + label + '</figcaption>' +
         '<table class="cm-table" aria-label="' + label + ': TP ' + r.tp + ', FN ' + r.fn + ', FP ' + r.fp + ', TN ' + r.tn + '">' +
         '<thead><tr><td></td><th scope="col">Predicted up</th><th scope="col">Predicted not up</th></tr></thead><tbody>' +
         '<tr><th scope="row">Actual up</th>' + confusionCell("good", "TP", r.tp, ups) + confusionCell("bad", "FN", r.fn, ups) + '</tr>' +
         '<tr><th scope="row">Actual not up</th>' + confusionCell("bad", "FP", r.fp, downs) + confusionCell("good", "TN", r.tn, downs) + '</tr>' +
         '</tbody></table></figure>';
}

// Method whose confusion matrices are shown right now (kept when you switch variety)
var cmSelected = "";

// Returns the confusion matrices of one variety: a card with the baselines, then a card with a picker for the methods
function confusionSection(variety, keys) {
  var baselines = RESULTS[keys[0]].varieties[variety].baselines;
  var baseGrids = ""; // One grid for each baseline
  for (var name in baselines) {
    baseGrids += confusionFigure(name, baselines[name]);
  }

  var selected = keys[0]; // Open the first method unless another one was picked before
  for (var k = 0; k < keys.length; k++) {
    if (keys[k] === cmSelected) {
      selected = cmSelected;
    }
  }

  var tabs = '<div class="tabs cm-tabs" role="group" aria-label="Confusion matrices of">';
  var panels = ""; // The grids of every method (only the picked one is visible)
  for (var m = 0; m < keys.length; m++) {
    var on = keys[m] === selected;
    tabs += '<button class="tab' + (on ? ' is-active' : '') + '" type="button" data-cm="' + keys[m] + '" aria-pressed="' + on + '">' + methodName(keys[m]) + '</button>';
    panels += '<div class="cm-panel" data-cm="' + keys[m] + '"' + (on ? '' : ' hidden') + '><div class="cm-row">';
    for (var f = 0; f < FEATURE_SETS.length; f++) {
      var entry = RESULTS[keys[m]].varieties[variety].feature_sets[FEATURE_SETS[f]];
      if (entry) {
        panels += confusionFigure(FEATURE_NAMES[FEATURE_SETS[f]], entry.test);
      }
    }
    panels += '</div></div>';
  }
  tabs += '</div>';

  return '<h3>Confusion matrices</h3>' +
         '<p class="results-note">Each grid counts one model’s predictions on the 2023 test rows. Rows are what actually happened, ' +
         'columns are what the model predicted, and each percentage is the share of its row.</p>' +
         '<p class="cm-key"><span><span class="cm-swatch good"></span>Correct (TP, TN)</span> ' +
         '<span><span class="cm-swatch bad"></span>Wrong (FP, FN)</span></p>' +
         '<div class="cm-card"><h4>Baselines</h4>' +
         '<p class="results-note">Simple rules that the methods need to beat.</p>' +
         '<div class="cm-row">' + baseGrids + '</div></div>' +
         '<div class="cm-card"><h4>Methods</h4>' +
         '<p class="results-note">Pick a method to see its three feature sets.</p>' +
         tabs + panels + '</div>';
}

// Shows the confusion matrices of one group (a method or the baselines)
function selectMatrixGroup(id) {
  cmSelected = id;
  var root = document.getElementById("results-root");
  var buttons = root.querySelectorAll(".cm-tabs .tab");
  for (var i = 0; i < buttons.length; i++) {
    var active = buttons[i].getAttribute("data-cm") === id;
    buttons[i].classList.toggle("is-active", active);
    buttons[i].setAttribute("aria-pressed", active ? "true" : "false");
  }
  var panels = root.querySelectorAll(".cm-panel");
  for (var j = 0; j < panels.length; j++) {
    panels[j].hidden = panels[j].getAttribute("data-cm") !== id;
  }
}

// Returns everything shown for one variety
function renderVariety(variety) {
  var keys = methodKeys();
  var majority = RESULTS[keys[0]].varieties[variety].baselines["Majority baseline"]; // Its counts describe the test set
  var total = majority.tp + majority.fp + majority.tn + majority.fn; // Number of test rows
  var up = Math.round((majority.tp + majority.fn) / total * 100); // Share of "up" in the test labels

  var html = takeaway(variety, keys) +
             '<h3>Test macro-F1 against the baselines</h3>' +
             '<p class="results-note">Each bar is one model’s macro-F1 on the 2023 test year, and a bar above a dashed line beats that baseline.</p>' +
             testChart(variety, keys) +
             '<h3>Test results (2023)</h3>' +
             '<p class="results-note">' + total.toLocaleString("en-US") + ' test rows, ' + up + '% of them “up”. ' +
             'The highest macro-F1 is in bold. “Tuned” is the setting chosen on the 2022 validation year.</p>' +
             resultsTable(variety, keys) +
             confusionSection(variety, keys);

  var charts = ""; // Validation charts of the methods that were tuned
  for (var m = 0; m < keys.length; m++) {
    if (RESULTS[keys[m]].param_grid.length > 1) {
      charts += validationChart(keys[m], variety);
    }
  }
  if (charts !== "") {
    html += '<h3>Choosing hyperparameters (validation, 2022)</h3>' +
            '<p class="results-note">Each point is the macro-F1 of one setting trained on 2020 to 2021 and scored on 2022, ' +
            'and the ring marks the one chosen for the test.</p>' + charts;
  }
  return html;
}

// Opens the tab of a variety and draws its tables and charts
function selectVariety(variety) {
  var buttons = document.getElementById("variety-tabs").querySelectorAll("button");
  for (var i = 0; i < buttons.length; i++) {
    var active = buttons[i].getAttribute("data-variety") === variety;
    buttons[i].classList.toggle("is-active", active);
    buttons[i].setAttribute("aria-pressed", active ? "true" : "false");
  }
  document.getElementById("results-root").innerHTML = renderVariety(variety);
}

// Builds the tabs and opens the first one
function init() {
  var root = document.getElementById("results-root");
  var tabs = document.getElementById("variety-tabs");
  if (!root || !tabs) { // This page has no Results section
    return;
  }
  if (typeof RESULTS === "undefined") { // results/results.js did not load
    root.innerHTML = '<p class="placeholder">Results are not available yet.</p>';
    return;
  }

  var varieties = Object.keys(RESULTS[methodKeys()[0]].varieties);
  var html = ""; // Buttons of the tabs
  for (var i = 0; i < varieties.length; i++) {
    html += '<button class="tab" type="button" data-variety="' + varieties[i] + '">' + (VARIETY_NAMES[varieties[i]] || varieties[i]) + '</button>';
  }
  tabs.innerHTML = html;

  tabs.addEventListener("click", function (event) {
    var button = event.target.closest("button");
    if (button) {
      selectVariety(button.getAttribute("data-variety"));
    }
  });

  root.addEventListener("click", function (event) { // Picker of the confusion matrices
    var button = event.target.closest(".cm-tabs .tab");
    if (button) {
      selectMatrixGroup(button.getAttribute("data-cm"));
    }
  });

  selectVariety(varieties.indexOf(DEFAULT_VARIETY) !== -1 ? DEFAULT_VARIETY : varieties[0]);
}

init();

// Marks the nav link of the section you are reading, so the line under the link follows you down the page
function initNavSpy() {
  var header = document.querySelector(".site-nav");
  var list = header ? header.querySelector("ul") : null;
  if (!list) { // This page has no nav
    return;
  }

  var links = list.querySelectorAll("a");
  var sections = []; // Pairs of {link, element} for every nav link that points to a section
  for (var i = 0; i < links.length; i++) {
    var element = document.getElementById(links[i].getAttribute("href").slice(1));
    if (element) {
      sections.push({link: links[i], element: element});
    }
  }

  var current = null; // Link that is marked right now
  var clicked = null; // Section whose link was clicked, until you scroll by yourself
  var waiting = false; // True while an update is already scheduled

  function update() {
    waiting = false;
    var line = header.offsetHeight + 40; // A section counts once its top passes this line
    var active = null; // Last section that passed the line
    for (var j = 0; j < sections.length; j++) {
      if (sections[j].element.getBoundingClientRect().top <= line) {
        active = sections[j].link;
      }
    }
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 4) { // Bottom of the page
      active = sections[sections.length - 1].link; // The last section, unless you clicked another one that is on screen
      if (clicked) {
        var box = clicked.element.getBoundingClientRect();
        if (box.top < window.innerHeight && box.bottom > 0) {
          active = clicked.link;
        }
      }
    }
    if (active === current) { // Nothing changed
      return;
    }

    current = active;
    for (var k = 0; k < links.length; k++) {
      links[k].removeAttribute("aria-current");
    }
    if (current) {
      current.setAttribute("aria-current", "true");
      list.scrollTo({left: current.offsetLeft - (list.clientWidth - current.clientWidth) / 2, behavior: "smooth"}); // Keeps it visible on small screens
    }
  }

  function schedule() { // Runs update once per frame while scrolling
    if (!waiting) {
      waiting = true;
      window.requestAnimationFrame(update);
    }
  }

  list.addEventListener("click", function (event) { // Short sections near the end cannot reach the top, so remember the click
    var link = event.target.closest("a");
    clicked = null;
    for (var m = 0; m < sections.length; m++) {
      if (sections[m].link === link) {
        clicked = sections[m];
      }
    }
  });
  var forget = function () { clicked = null; }; // Scrolling by yourself ends it
  window.addEventListener("wheel", forget, {passive: true});
  window.addEventListener("touchstart", forget, {passive: true});
  window.addEventListener("keydown", forget);

  window.addEventListener("scroll", schedule, {passive: true});
  window.addEventListener("resize", schedule);
  update();
}

initNavSpy();

// Member cards: long contribution lists show their first items, and a button opens or closes the rest with a smooth slide
function initContributions() {
  var SHOWN = 3; // Items that stay visible when the list is collapsed
  var DURATION = 300; // Length of the slide in milliseconds
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var lists = document.querySelectorAll(".contrib-list");

  for (var i = 0; i < lists.length; i++) {
    (function (list) {
      var items = list.querySelectorAll("li");
      if (items.length <= SHOWN) { // Short list, nothing to hide
        return;
      }

      var button = document.createElement("button");
      button.type = "button";
      button.className = "contrib-toggle";
      list.parentNode.insertBefore(button, list.nextSibling);

      var open = false; // True while the whole list is shown
      var finishNow = null; // Ends a slide that is still running

      function hideExtras(hidden) { // Hides or shows the items after the first ones
        for (var j = SHOWN; j < items.length; j++) {
          items[j].hidden = hidden;
        }
      }

      function fadeExtras(visible) { // Fades the extra items in or out while the list slides
        for (var j = SHOWN; j < items.length; j++) {
          items[j].style.transition = "opacity " + DURATION + "ms ease";
          items[j].style.opacity = visible ? "1" : "0";
        }
      }

      function clearFade() { // Removes the inline styles of the fade
        for (var j = SHOWN; j < items.length; j++) {
          items[j].style.transition = "";
          items[j].style.opacity = "";
        }
      }

      function slide(from, to, onDone) { // Moves the height of the list from one value to the other
        list.style.overflow = "hidden";
        list.style.height = from + "px";
        list.getBoundingClientRect(); // Makes the browser apply the start height before the change
        list.style.transition = "height " + DURATION + "ms ease";
        list.style.height = to + "px";

        var finished = false; // True once the slide has been cleaned up
        var timer = null; // Backup in case the transition never reports that it ended
        function end() {
          if (finished) {
            return;
          }
          finished = true;
          clearTimeout(timer);
          list.removeEventListener("transitionend", onEnd);
          list.style.height = "";
          list.style.overflow = "";
          list.style.transition = "";
          finishNow = null;
          onDone();
        }
        function onEnd(event) {
          if (event.target === list) {
            end();
          }
        }
        list.addEventListener("transitionend", onEnd);
        timer = setTimeout(end, DURATION + 100);
        finishNow = end;
      }

      button.addEventListener("click", function () {
        if (finishNow) { // A click in the middle of a slide ends it first
          finishNow();
        }
        var from = list.offsetHeight; // Height before the change
        open = !open;
        button.setAttribute("aria-expanded", open ? "true" : "false");
        button.textContent = open ? "Show less" : "Show all";

        if (reduceMotion) { // No slide for people who asked for less motion
          hideExtras(!open);
          return;
        }

        if (open) {
          hideExtras(false);
          var full = list.offsetHeight; // Height with every item shown
          for (var j = SHOWN; j < items.length; j++) {
            items[j].style.opacity = "0";
          }
          slide(from, full, clearFade);
          fadeExtras(true);
        } else {
          hideExtras(true);
          var short = list.offsetHeight; // Height with only the first items
          hideExtras(false);
          slide(from, short, function () {
            hideExtras(true);
            clearFade();
          });
          fadeExtras(false);
        }
      });

      button.setAttribute("aria-expanded", "false");
      button.textContent = "Show all";
      hideExtras(true);
    })(lists[i]);
  }
}

initContributions();