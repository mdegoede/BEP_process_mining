# PRIPEL

PRIPEL (Privacy-preserving event log publishing with contextual information) is a framework to publish event logs that fulfill differential privacy. We provide an implementation of PRIPEL in Python 3. Our code is available under the MIT license. If you use it for academic purposes please cite our paper:
```
@inproceedings{Fahrenkrog-Petersen20,
  author    = {Stephan A. Fahrenkrog{-}Petersen and
               Han van der Aa and
               Matthias Weidlich},
  editor    = {Dirk Fahland and
               Chiara Ghidini and
               J{\"{o}}rg Becker and
               Marlon Dumas},
  title     = {{PRIPEL:} Privacy-Preserving Event Log Publishing Including Contextual
               Information},
  booktitle = {Business Process Management - 18th International Conference, {BPM}
               2020, Seville, Spain, September 13-18, 2020, Proceedings},
  series    = {Lecture Notes in Computer Science},
  volume    = {12168},
  pages     = {111--128},
  publisher = {Springer},
  year      = {2020},
  url       = {https://doi.org/10.1007/978-3-030-58666-9\_7},
  doi       = {10.1007/978-3-030-58666-9\_7},
  timestamp = {Sun, 25 Jul 2021 11:49:33 +0200},
  biburl    = {https://dblp.org/rec/conf/bpm/Fahrenkrog-Petersen20.bib},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```

## Requirements
To run our algorithm you need the following Python packages:
- SciPy (https://www.scipy.org)
- PM4Py (https://pm4py.fit.fraunhofer.de) 
- IBM diffprivlib (https://diffprivlib.readthedocs.io/en/latest/) (in version 0.5.1 --> other versions might not work, since the API changed)

We did run our algorithm only with Python 3, so we can not guarantee that it works with Python 2.

## How to run PRIPEL
You can run the framework using the following command:
```
python pripel.py <fileName> <epsilon> <n> <k> 
```

The different parameters have the following meaning
- filename: Name of event log (xes-file) that shall be anonymised
- epsilon: Strength of the differential privacy guarantee. It must be a float
- n: Maximum prefix of considered traces for the trace-variant-query. It must be an integer
- k: Pruning parameter of the trace-variant-query. At least k traces must appear in a noisy variant count to be part of the result of the query. It must be an integer

The program will produce a xes-file that contains an anonymised event log.

### Runtime

Please note that certain combinations of n, k and epsilon can lead to very long runtime. If you experience such a runtime, try to higher values for k. Besides that, it might help to use a greedy trace matching strategy by setting the parameter <greedy> of the function matchQueryToLog from the class TraceMatcher to true.

### Customization
Additionally, please note that some event logs contain attributes that are equivalent to a case id. For privacy reasons such attributes must be deleted from the anonymised log. We handle such attributes with a blacklist. This blacklist is defined in the function __getBlacklistOfAttributes in tracematcher.py and attributeAnonymizer.py.

## Components

### pripel.py
These scripts run the overall PRIPEL-Framework. It takes in the event log (XES-File) performs the PRIPEL-based anonymisation and then saves the resulting anonmyised logs as an XES-File.

### trace_variant_query.py
Performs the trace-variant query on the input log. The query is based on the algorithm described in:
https://link.springer.com/article/10.1007/s12599-019-00613-3


### tracematcher.py
This script matches the cases from the input event log with the traces from the trace-variant-query. It uses standard assignment algroithm implemented in Numpy.

### attributeAnonymizier.py
In this script the contextual information of the matched log is anonymised.

### levenshtein.py
Contains implementation of the levenshtein-distance for traces. We use it in the tracematcher.py.


## How to contact us
PRIPEL was developed at the Process-driven Architecture group of Humboldt-Universität zu Berlin. If you want to contact us, just send us a mail at: fahrenks || hu-berlin.de
  
## Find out more about our research
If you want find out more about our research, you can visit the following website: 
https://sites.google.com/view/sfahrenkrog-petersen/home
