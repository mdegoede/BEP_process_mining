# Analyzing Privacy Preservation Techniques for Process Mining: Measuring Result Utility Across Different Event Log Dependency Types and Log sizes

Repository for the experiments described in "Analyzing Privacy Preservation Techniques for Process Mining: Measuring Result Utility Across Different Event Log Dependency Types and Log sizes", executed as Bachelor End Project for the Bachelor Data Science form the Technical University of Eindhoven.

## Overview

- [Paper Details](#PaperDetails)
  - [Summary](#Summary)
  - [Reproduction](#Reproduction)
  - [Dependencies](#Dependencies)
- [Extensions](#Extensions)

## Paper Details

### Summary

In the paper, the following topics are addressed:
- Event logs are important for improving organizational efficiency and competitiveness.
- Privacy issues can arise when sensitive data is spread and privacy concerns are raised.
- Privacy-preserving methods should balance confidentiality with utility in process mining.
- The research goal is to study the impact of applying privacy techniques on event logs on the process discovery task.
- This is done by evaluating process models from synthetic logs with various privacy methods across different event log dependency types and log sizes.

### Reproduction

To reproduce the results in "Analyzing Privacy Preservation Techniques for Process Mining: Measuring Result Utility Across Different Event Log Dependency Types and Log sizes", first run 'anonymize.py', then run 'compute_GED.py' and consequently run 'compute_precision.py' and 'compute_fitness.py'. 

Running 'anonymize.py' automates the process of applying PRETSAcase, TLKC-privacy and PRIPEL on the original logs simple and more complex event logs that are provided in the 'data\logs\simple' and 'data\logs\complex' folder. The anonymized event logs are then stored in a folder of the applied privacy-preserving method within the same folder, e.g. 'data\logs\simple\tlkc'.

Running 'compute_GED.py' converts the anonymized event logs to .pnml process models, using inductive miner, and stores it in the 'data\pnml_nets' folder under the respective model complexity, present dependency types and applied privacy method, e.g. data\pnml_nets\simple\XOR\tlkc. The pnml files are also stored in the folder 'CalculateGED'. The original event logs are also convertoed to .pnml models and stored in 'the folder 'data\pnml_nets' under the respective model complexity, e.g. 'data\pnml_nets\simple', and in the folder 'CalculateGED'. Then, the GED is calculated between the original and the privatized models and stores result as a dataframe in the path 'CalculateGED\geds\geds_df.csv'. The results are also visualized as a heatmap. 

Running 'compute_precision.py' and 'compute_fitness.py' computes the precision and recall values between the original and privatized process models and stores the result in 'CalculateGED\conformance_results\fit_df.csv'. The precision and recall values are also visualized as a heatmap. 

Additional log statistics can be obtained by running 'log_evaluations.py'. 

> The code was tested with Python 3.10 on Windows.

### Dependencies

The code was tested using these libraries and versions:

```
pm4py             2.7.11.7
pyfpgrowth        1.0
pandas            2.2.2
mlxtend           0.23.1
numpy             1.26.4
deprecation       2.1.0
scipy             1.13.0
python-dateutil   2.9.0.post0
diffprivlib       0.6.4
matplotlib        3.8.4
seaborn           0.13.2
```

This code also makes use of existing git-repositories that were made publicly available, namely:
- TLKC-Privacy: the original repository can be found at https://github.com/m4jidRafiei/TLKC-Privacy.git and is protected under the GNU General Public License v3.0. This repository is stored as 'tlkc' in the current repository. 
- PRIPEL: the original repository can be found at https://github.com/samadeusfp/PRIPEL.git and is protected under the MIT License. This repository is stored as 'PRIPEL_master' in the current repository. 
- pm4py-core: the original repository can be found at https://github.com/pm4py/pm4py-core.git and is proteted under the GNU General Public License v3.0. This repository is stored as 'pm4yp_copy' in the current repository. 

The code from these repositories was minimally modified to allow for automated repeating of the algorithms, specific parameter settings, and storing the results in the correct location. These changes are made in the 'anonymize.py' file, there the privacy-preserving algorithms are applied. Other changes are some of the import statements, changing 'import factory' to e.g. 'import importer'. 

## Extensions

This code can also be used on different event logs, if these are stored as .xes files in the \data folder. However, the code repeatedly assumes that the files are stored under a name of the following format: DEPENDENCY_TYPES + MODEL_COMPLEXITY + _ + LOG_SIZE.xes, where MODEL_COMPLEXITY∈{1, 2} denoting the simple and more complex models respectively. Additionally, the model settings can be adapted in 'anonymize.py' to provide different settings regarding the privacy strength.