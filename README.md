# vegetation-dynamics
Investigating cluster dynamics in models of patchy ecosystems

## Requirements

This repository requires installation of compilers/interpreters of the following programming languages, and the corresponding packages/modules:

1) Python: matplotlib, multiprocessing, numba, numpy, pickle, scikit-image, tqdm
2) R: ggplot, reticulate, spatialwarnings (from [Genin et. al](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13058))

## Models

This repository contains code to simulate the following models/automatons:
1) Static null model: A 2D lattice that is randomly assigned with 0's and 1's, based on some occupational probability 'p'. Used as benchmark for percolation transitions
2) Stochastic null model: A model that is initialized with some fractional occupancy 'f', and evolves in a completely random manner (0 -> 1, 1 -> 0) whilst hovering around the initialized fractional occupancy. Proposed in [Kefi et. al](https://onlinelibrary.wiley.com/doi/full/10.1111/j.1461-0248.2010.01553.x). Used as control for cluster dynamics
3) Tricritical Directed Percolation (TDP): The central model of this project. Proposed in [this paper](https://arxiv.org/abs/cond-mat/0608339). Initialized with two parameters, (p, q), the working of this model is decrbied by the following schematic from [Sankaran et. al](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.13304)

![alt text](https://i.ibb.co/k95q8tF/tdp-schematic.png)

4) Scanlon Model: This model is from [Scanlon et. al](https://www.nature.com/articles/nature06060). The only parameter in this model is rainfall. Ubiquitously produces power-law distribution in cluster sizes. Used in addition to gauge how cluster dynamics varies across models. This model is simulated using Markov chain Monte Carlo method, with the following transition rates:

![alt text](https://i.ibb.co/vBR8qps/scanlon-equations.png)

5) Contact Process: Tricritical Directed Percolation with q = 0 is known as Contact Process. Infact, TDP is actually an extension of this model

Code for all models can be found inside the models folder. Each model has different versions of similar code that are intended for different purposes:

1) `in_place_processing.py`: For tracking cluster dynamics. After equilibriation, this script will pass consecutive landscapes that differ by a single update to cluster_dynamics.py
2) `coarse_dynamics.py`: Utilizes a difference map technique to approximate cluster dynamics across larger timescales
3) `dumper.py`: Returns the final density associated with initialized parameter value(s), averaged across all ensembles. Ideal for plotting phase transitions/diagrams
4) `final_lattice.py`: Saves all final lattices associated with initialized parameter value(s). Required for probing cluster size distribution
5) `spanning_cluster.py`: Returns the percolation probability associated with initialized parameter value(s). Basically, it is the fraction of ensembles that have a percolation/spanning cluster

## How to Run

The entire repository needs to be downloaded since none of the scripts are self-contained. All versions of all models are imported in the `terminal.py` file. Used this file to run jobs. The 'code_snippets' folder contains lines of code for specific purposes. A particular snippet has been explained below:

```python
set_start_method("spawn")
num_simulations = cpu_count() - 1
p_values = [0.70, 0.71]
q = 0.25

for p in p_values:
    purge_data()
    print(f"\n---> Simulating p = {p} <---")
    file_string = str(p).replace('.', 'p')
    tricritical(p, q, num_simulations, save_series=False, save_cluster=True, calc_residue=True)
    compile_changes("tricritical", range(num_simulations), plot_name=file_string)
    plot_changes(file_string)
```

1) `set_start_method("spawn")`: required for proper parallelization
2) `num_simulations = cpu_count() - 1`: specifies the number of simulations that will be run parallely
3) `p_values = [0.70, 0.71]` and `q = 0.25`: we will simulate p = 0.7 and 0.71 for q = 0.25 (TDP)
4) `purge_data()`: required to get rid of transient data created by step 5 from previous simulation
5) `tricritical(p, q, num_simulations, save_series=False, save_cluster=True, calc_residue=True)`: simulates the TDP model using `in_place_processing.py` (hence, cluster dynamics will be tracked). Will not save time evolution of landscape, but will save cluster dynamics and also calculate residues (for deducing nature of noise). The saved files are dumped in the corresponding model's folder. If you intend to modify secondary model parameters like length of the landscape or time of the simulation/equilibration phase, then it can be done in the bottom of `in_place_processing.py`
6) `compile_changes("tricritical", range(num_simulations), plot_name=file_string)`: Goes through the `tricritical` model folder and compiles relevant data into text files (prefixed with `file_string`) which is saved in the `outputs` folder
7) `plot_changes(file_string)`: Goes through the `outputs` folder and plots graphs from the text files beginning with `file_string`

The repository is organized as follows:

1) Operational scripts in the root folder: terminal.py should be used for running jobs, compile_changes.py performs all the analysis and dumps data in a folder named "outputs" located in the root, and plot_changes.py generates graphs from the aforementioned data
2) This project explores several models.  Every model has different variations of scripts that return/save different data and are optimized for different purposes. The data generated by these scripts are dumped in the same folder and analyzed by the compile_changes.py file
3) cluster_dynamics.py looks at two lattices that differ by a single update and returns (a) process undergone by the lattice (growth, decay, split, merge, appearance, disappearance), (b) sizes of the participating cluster(s), and (c) sizes of the resulting cluster(s)
4) The "code_snippets" folder contains grouped lines of code for analyzing specific aspects of each model. These can be readily copied and modified in the terminal.py script
5) The "consistency_checks" folder contains scripts that simulate the inferred stochastic differential equations from a realisation and compares the resultant distribution to the actual distribution
6) The "fitters" folder contains Python and R scripts that fit (a) cluster size distribution and (b) cluster dynamics to power-law, truncated power-law and exponential distributions using an R package called spatialwarnings
7) A folder named "outputs" is generated during runtime, for dumping .txt files (generated by compile_changes.py) and .png files (generated by plot_changes.py). Within this folder, organizer.py can be used to group files with same prefix into a single folder. These folders were then moved to the "results" section
8) The "plotters" folder contains scripts uses data from the "results" folder to generate figures for thesis/publication
