# bsc-ndd-paraeval
This repository contains supplementary code for BSc thesis "Evaluierung von Parametern für Near-Duplicate Detection verschiedener Textsorten" at the University of Potsdam.

If not stated otherwise, code was written for and executed with Python3.10. If additional external packages are necessary, they are listed in a `requirements.txt` file in the respective subdirectory.


## Structure of the repository
```
.
├── data-generation
│   ├── near-duplicate-generation
│   └── preprocessing
│       ├── wikipedia
│       └── wikisource
├── evaluation
└── param_config
```
The `data-generation` subdirectory contains files related to preprocessing the raw data and creating the near-duplicates datasets.
The `evaluation` subdirectory contains the files for the computation of the gold standard and for the experiment run.
In the `param_config` subdirectory, the parameter configurations that were used for the experiments are stored.




## Author
Luise Köhler

email: luise.koehler(at)uni-potsdam.de
