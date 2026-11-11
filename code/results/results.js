const RESULTS = {
  "naive_bayes": {
    "method": "naive_bayes",
    "param_grid": [
      {
        "variance_floor": 1e-09
      },
      {
        "variance_floor": 1e-06
      },
      {
        "variance_floor": 0.001
      },
      {
        "variance_floor": 0.1
      }
    ],
    "varieties": {
      "price_well_milled": {
        "baselines": {
          "Majority baseline": {
            "tp": 0,
            "fp": 0,
            "tn": 428,
            "fn": 1079,
            "accuracy": 0.2840079628400796,
            "macro_precision": 0.1420039814200398,
            "macro_recall": 0.5,
            "macro_f1": 0.22118863049095608
          },
          "Persistence baseline": {
            "tp": 739,
            "fp": 277,
            "tn": 151,
            "fn": 340,
            "accuracy": 0.5905773059057731,
            "macro_precision": 0.5174489231361354,
            "macro_recall": 0.518848579075468,
            "macro_f1": 0.5170536616276382
          }
        },
        "feature_sets": {
          "price_only": {
            "best_params": {
              "variance_floor": 1e-09
            },
            "val_scores": [
              0.35219693753316067,
              0.35219693753316067,
              0.35219693753316067,
              0.35219693753316067
            ],
            "test": {
              "tp": 174,
              "fp": 100,
              "tn": 328,
              "fn": 905,
              "accuracy": 0.33311214333112144,
              "macro_precision": 0.4505271695052717,
              "macro_recall": 0.4638077832537916,
              "macro_f1": 0.32607450698227636
            }
          },
          "weather_only": {
            "best_params": {
              "variance_floor": 1e-09
            },
            "val_scores": [
              0.441402369268748,
              0.441402369268748,
              0.441402369268748,
              0.441402369268748
            ],
            "test": {
              "tp": 410,
              "fp": 167,
              "tn": 261,
              "fn": 669,
              "accuracy": 0.44525547445255476,
              "macro_precision": 0.4956085425169117,
              "macro_recall": 0.4948972742154816,
              "macro_f1": 0.4397789445974116
            }
          },
          "price_weather": {
            "best_params": {
              "variance_floor": 1e-09
            },
            "val_scores": [
              0.44312911731240345,
              0.44312911731240345,
              0.44312911731240345,
              0.44312911731240345
            ],
            "test": {
              "tp": 415,
              "fp": 197,
              "tn": 231,
              "fn": 664,
              "accuracy": 0.42866622428666223,
              "macro_precision": 0.4681025669113083,
              "macro_recall": 0.4621675053918045,
              "macro_f1": 0.42002008767236443
            }
          }
        }
      },
      "price_regular_milled": {
        "baselines": {
          "Majority baseline": {
            "tp": 0,
            "fp": 0,
            "tn": 390,
            "fn": 1117,
            "accuracy": 0.258792302587923,
            "macro_precision": 0.1293961512939615,
            "macro_recall": 0.5,
            "macro_f1": 0.2055877701634159
          },
          "Persistence baseline": {
            "tp": 786,
            "fp": 275,
            "tn": 115,
            "fn": 331,
            "accuracy": 0.5978765759787658,
            "macro_precision": 0.4993290448557288,
            "macro_recall": 0.4992711704887175,
            "macro_f1": 0.4984413513121647
          }
        },
        "feature_sets": {
          "price_only": {
            "best_params": {
              "variance_floor": 1e-09
            },
            "val_scores": [
              0.4183370158159508,
              0.4183370158159508,
              0.4183370158159508,
              0.4183370158159508
            ],
            "test": {
              "tp": 216,
              "fp": 79,
              "tn": 311,
              "fn": 901,
              "accuracy": 0.34970139349701396,
              "macro_precision": 0.4944020249482576,
              "macro_recall": 0.4954055046713955,
              "macro_f1": 0.3471068388310646
            }
          },
          "weather_only": {
            "best_params": {
              "variance_floor": 1e-09
            },
            "val_scores": [
              0.4335067866616422,
              0.4335067866616422,
              0.4335067866616422,
              0.4335067866616422
            ],
            "test": {
              "tp": 420,
              "fp": 128,
              "tn": 262,
              "fn": 697,
              "accuracy": 0.45255474452554745,
              "macro_precision": 0.5198123044838373,
              "macro_recall": 0.5239010169180267,
              "macro_f1": 0.446470191466485
            }
          },
          "price_weather": {
            "best_params": {
              "variance_floor": 1e-09
            },
            "val_scores": [
              0.43312644517463794,
              0.43312644517463794,
              0.43312644517463794,
              0.43312644517463794
            ],
            "test": {
              "tp": 310,
              "fp": 119,
              "tn": 271,
              "fn": 807,
              "accuracy": 0.3855341738553417,
              "macro_precision": 0.48700109414395126,
              "macro_recall": 0.4862004453320478,
              "macro_f1": 0.38512236905647335
            }
          }
        }
      },
      "price_special": {
        "baselines": {
          "Majority baseline": {
            "tp": 0,
            "fp": 0,
            "tn": 480,
            "fn": 1016,
            "accuracy": 0.32085561497326204,
            "macro_precision": 0.16042780748663102,
            "macro_recall": 0.5,
            "macro_f1": 0.24291497975708504
          },
          "Persistence baseline": {
            "tp": 670,
            "fp": 301,
            "tn": 179,
            "fn": 346,
            "accuracy": 0.5675133689839572,
            "macro_precision": 0.5154813398067775,
            "macro_recall": 0.5161827427821523,
            "macro_f1": 0.5153011990876017
          }
        },
        "feature_sets": {
          "price_only": {
            "best_params": {
              "variance_floor": 1e-09
            },
            "val_scores": [
              0.39254386353763093,
              0.39254386353763093,
              0.39254386353763093,
              0.39254386353763093
            ],
            "test": {
              "tp": 160,
              "fp": 79,
              "tn": 401,
              "fn": 856,
              "accuracy": 0.375,
              "macro_precision": 0.49423479560486383,
              "macro_recall": 0.4964484908136483,
              "macro_f1": 0.35834784064662484
            }
          },
          "weather_only": {
            "best_params": {
              "variance_floor": 1e-09
            },
            "val_scores": [
              0.4418420965113572,
              0.4418420965113572,
              0.4418420965113572,
              0.4418420965113572
            ],
            "test": {
              "tp": 218,
              "fp": 135,
              "tn": 345,
              "fn": 798,
              "accuracy": 0.37633689839572193,
              "macro_precision": 0.45970050485898895,
              "macro_recall": 0.46665846456692917,
              "macro_f1": 0.37180963748381446
            }
          },
          "price_weather": {
            "best_params": {
              "variance_floor": 1e-09
            },
            "val_scores": [
              0.44997151882346853,
              0.44997151882346853,
              0.44997151882346853,
              0.44997151882346853
            ],
            "test": {
              "tp": 277,
              "fp": 167,
              "tn": 313,
              "fn": 739,
              "accuracy": 0.39438502673796794,
              "macro_precision": 0.46070119549207,
              "macro_recall": 0.46236056430446193,
              "macro_f1": 0.3940341213920384
            }
          }
        }
      }
    }
  }
};
