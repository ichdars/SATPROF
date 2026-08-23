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
