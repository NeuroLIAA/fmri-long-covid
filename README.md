# Resting state fMRI networks of long-COVID patients
## About
Code base used for the paper "Impact of long-COVID on the local and global efficiency of brain networks". *Clin Neuroimaging*. 2024;e70001.  42 subjects (32 females, 10 males, mean age 56) have reported subjective complaints such as loss of focus and brain fogs following a COVID-19 infection. Clinical tests carried out have shown low scores in memory, attention, language and executive control.

In this study, we analyse the functional connectivity of their functional brain networks based on resting state fMRI sessions. Topological measures (network efficiency, largest connected component and modularity) are computed on several thresholds (over the absolute correlation coefficients) and compared against a control group (43 pre-pandemic subjects with average scores on their clinical tests).

<div style="text-align: center;"><img src="modules/figures/global_networks_hlegend.png" alt="Mean global networks at 40% threshold" width="700"/></div>

## Usage
``nilearn`` is employed for data manipulation and ``networkx`` for graph analysis.

The following command will perform group-based analysis on the ```Default``` network using the ```schaefer``` atlas with 400 regions, applying a threshold at 5, 10, 15 and 20% of the maximum correlation coefficients:
```
python bold_analysis.py -n Default -a schaefer -nr 400 -tr 0.05 0.1 0.15 0.2
```

Any other of the seven brain networks in the ```schaefer``` atlas can also be extracted. Supported atlases for global analysis:
- ```schaefer```
- ```aal```
- ```destrieux```
- ```msdl```

Although outside the scope of the current study, the regions comprising a specific brain network in the ```aal``` atlas can also be defined in ```brain_networks.json```. Independent component analysis is also supported and can be run with the ```-nc``` flag, indicating the number of components to extract. 

## How to cite us
If you wish to cite us, please use the following BibTex:
```
@article{https://doi.org/10.1002/neo2.70001,
author = {Travi, Fermín and Hernández, Micaela A. and Bianchi, Bruno and Crivelli, Lucía and Allegri, Ricardo F. and Fernández Slezak, Diego and Calandri, Ismael L. and Kamienkowski, Juan E.},
title = {Impact of long-COVID on the local and global efficiency of brain networks},
journal = {Clinical Neuroimaging},
volume = {1},
number = {1-2},
pages = {e70001},
keywords = {cognitive impact, functional network analysis, long-COVID, network efficiency, rs-fMRI},
doi = {https://doi.org/10.1002/neo2.70001},
url = {https://onlinelibrary.wiley.com/doi/abs/10.1002/neo2.70001},
eprint = {https://onlinelibrary.wiley.com/doi/pdf/10.1002/neo2.70001},
year = {2024}
}
```
