# Divine Comedy As A Compex System (in review)
This repository provides the computational analysis and visualisation code used in the accompanying paper. The project is organised as a reproducible Python codebase, with modular analysis and plotting components and scripts to reproduce the figures presented in the paper.

Divine Comedy Text Analysis
===================================
Tools to preprocess Dante's *Divine Comedy*, build word-adjacency networks, visualise them, and analyse centrality and word frequency distributions.

## Project structure
- `divine_comedy.txt`: Source text (Project Gutenberg).
- `main.py`: Orchestrates preprocessing, network construction, centrality evaluation, and frequency plots.
- `src/preprocessing.py`: Cleans and splits the text into the three canticles.
- `src/create_networks.py`: Builds weighted word-adjacency graphs for each canticle and the full poem.
- `src/display_network.py`: Optional network visualisation (spring layout).
- `src/centrality_measures.py`: Computes and plots top centrality measures and subgraphs.
- `src/frequency_analysis.py`: Word frequency distributions (raw or log-binned Zipf plots).

## Setup (Windows-friendly)
1) Create/activate a virtual environment (Python 3.10):  
   ```powershell
   py -3.10 -m venv .venv
   .\.venv\Scripts\activate
   ```

2) Install dependencies:  
   ```powershell
   .\.venv\Scripts\python -m pip install -r requirements.txt
   ```
   *On first run, NLTK will download `punkt` and `stopwords` automatically; this may take a moment.*

## Running the analysis
From the repo root (with the venv active):  
```powershell
.\.venv\Scripts\python main.py
```
This reads `divine_comedy.txt`, builds networks for Inferno, Purgatorio, Paradiso, computes centrality stats, and plots word-frequency distributions. Network visualisation in `display_network.py` is optional and commented out by default because it can be slow on large graphs—uncomment in `main.py` if needed.

a nice one liner to run would be:
```py -3.10 -m venv .venv && .\.venv\Scripts\python -m pip install -r requirements.txt && .\.venv\Scripts\python main.py```


