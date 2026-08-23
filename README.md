# SATPROF

SATPROF is a tool to visualize the runtime profiling data for SAT-Solvers like CaDiCaL and Kissat.
SATPROF reads the profiling block from the Solver logfiles and displays them as a DAG. This works
for a single run or for an aggregated benchmark suite, it can optionally show a plotted distribution
for an aggregation.


## Prerequisites

* Python 3.12 or newer
* Graphviz as systempackage
* Python dependencies: graphviz, matplotlib

The Python package graphviz only yields the .dot description, while the dot programm from the system package
does the rendering.

## Installation

Run the following commands to install SATPROF, it is recommended to use a virtual enviroment to avoid conflicts
with other python projects

```bash
git clone <REPO-URL>
cd SATPROF
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Logfiles
SATRPOF evaluates the Profiling-block which the solvers print at the end of their run, the profiling block
only exists if the solver was run with active profiling flag. A Logfile with a valif profiling block has a section like this 

```
c --- [ run-time profiling ] ------------------------------------------------
c
c         seconds   percent
c
c           4.29     35.71 %  propagate
c           1.88     15.65 %  analyze
...

```

## Usage

```bash
# run the script on a single benchmark
./main.py --file <filename>.log

# run the script on a suite of benchmarks without additional distiribution plot

./main.py --aggregate <folder>

# run the script on a suite of benchmarks with additional distiribution plot
./main.py --aggregate <folder> --dist

```

| Flag | Meaning | Default |
|---|---|---|
| `--file PFAD` | visualization of a single run | – |
| `--aggregate ORDNER` | aggregates all `.log`-files from a folder  | – |
| `--solver NAME` | overrides the automatic solver detection | automatic |
| `--dist` | Generates an additional distribution plot (only with `--aggregate`) | off |

The flags `--file` and `--aggregate` exclude eachtother but at least one is necessary for the script to be able to run.

## Solver detection

If you leave out the `--solver` flag the solvername , which the logfiles are created with, are read from the Banner-Block from the and picks the corresponding config file from /configs and checks if the logfile and the 
solver have the same solvername, if not the run crashes with an error.


## Output

```
output/
├── benchmarks/
│   └── <filename>_<solvername>_tree.png
└── suites/
    └── <foldername>_<solvername>/
        ├── <foldername>_<solvername>_tree.png
        ├── <foldername>_<solvername>_outliers.txt
        └── <foldername>_<solvername>_dist.png      (only with --dist)
```

The `outliers.txt` contains every Benchmark with the highest and lowest percentual runtime value per Node.

## Configs

The Config files should be placed in `configs/` as a JSON file. The config file describes, which Profiling-steps
are displayed as well as their hierarchie.

# Format

```json
{
  "name": "total",
  "solver": "kissat",
  "profiling_lvl": 0,
  "color": "black",
  "children": [
    {
      "name": "search",
      "profiling_lvl": 0,
      "color": "darkgreen",
      "children": [
        { "name": "propagate", "profiling_lvl": 0 }
      ]
    }
  ]
}
```

| Field | Where | Meaning |
|---|---|---|
| `solver` | only present in the rood node | Name of the solver, must be same as in the logfile banner |
| `name` | must be present in every node  | Name of the Profiling-step |
| `profiling_lvl` | every node | Profiling-level correpsonding to the solver option `PROFILING=n` |
| `color` | optional | frame-color of the node, the default is blue |
| `children` | optional | Substeps, should be an empty list for leave nodes |


Steps which are present in the config but not in the logfile are left out in the tree, while steps from the logfile, which are not present in the config, are jsut ignored. Which means that the Config decides what is displayed and what not.
