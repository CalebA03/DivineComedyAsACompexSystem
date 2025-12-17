'''
Compute the frequency distributions. We do this by:
1. Tokenising the text
2. Count frequency of each word and then orders them to get a rank
'''

from nltk.tokenize import word_tokenize
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


def get_word_frequencies(text):

    tokens = word_tokenize(text)  # Tokenize the text
    freq_dist = Counter(tokens)  # Count occurrences of each word
    return freq_dist

# Compute frequency distributions for each canticle
def freq_dist(inferno_clean, purgatorio_clean, paradiso_clean):
    freq_inferno = get_word_frequencies(inferno_clean)
    freq_purgatorio = get_word_frequencies(purgatorio_clean)
    freq_paradiso = get_word_frequencies(paradiso_clean)
    return freq_inferno, freq_purgatorio, freq_paradiso

'''
Plotting the frequency distribution:
1. Plots word frequency against rank on a log-log scale
2. fit a power law distribution
3. Determine the slop beta value to provide insight into the frequency distribution  
'''

def plot_word_frequency_rank(freq_dist, title):
    """
    Plot word frequencies on a log-log scale with power-law fitting.
    """
    # Get frequencies sorted in descending order
    frequencies = sorted(freq_dist.values(), reverse=True)
    # Compute ranks
    ranks = np.arange(1, len(frequencies) + 1)
    
    # Set font to Times New Roman
    plt.rcParams["font.family"] = "Times New Roman"

    # Plot on a log-log scale
    plt.figure(figsize=(10, 6))
    plt.loglog(ranks, frequencies, marker='o', linestyle='None')
    plt.xlabel('Rank', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(True)

    # Fit a power-law distribution and overlay it
    log_ranks = np.log10(ranks)
    log_freq = np.log10(frequencies)
    coeffs = np.polyfit(log_ranks, log_freq, 1)
    fitted_line = coeffs[0] * log_ranks + coeffs[1]
    plt.plot(ranks, 10**fitted_line, color='red')

    # Display the beta value in the top right-hand corner
    plt.text(0.95, 0.95, f'β = {coeffs[0]:.2f}', transform=plt.gca().transAxes, 
             fontsize=14, fontweight='bold', family="Times New Roman",
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'),
             horizontalalignment='right', verticalalignment='top')

    plt.show()


'''Logrithmic binning for Zipf plots (to clean up noisy right tail)'''

def _log_bin_by_rank(ranks, freqs, n_bins=50, min_points_per_bin=1):
    """
    Logarithmic binning in rank space to reduce right tail noise.
    Returns (binned_ranks, binned_freqs) using:
      - geometric mean for rank
      - arithmetic mean for frequency
    """
    ranks = np.asarray(ranks, dtype=float)
    freqs = np.asarray(freqs, dtype=float)

    mask = (ranks > 0) & (freqs > 0)
    ranks = ranks[mask]
    freqs = freqs[mask]

    if len(ranks) == 0:
        return np.array([]), np.array([])

    # Log spaced bin edges in rank space
    edges = np.logspace(np.log10(ranks.min()), np.log10(ranks.max()), n_bins + 1)

    binned_r = []
    binned_f = []

    for lo, hi in zip(edges[:-1], edges[1:]):
        in_bin = (ranks >= lo) & (ranks < hi)
        if np.count_nonzero(in_bin) < min_points_per_bin:
            continue

        r_bin = ranks[in_bin]
        f_bin = freqs[in_bin]

        # geometric mean rank, mean frequency
        r_gm = np.exp(np.mean(np.log(r_bin)))
        f_mean = np.mean(f_bin)

        binned_r.append(r_gm)
        binned_f.append(f_mean)

    return np.asarray(binned_r), np.asarray(binned_f)


def plot_word_frequency_rank_binned(freq_dist, title, n_bins=50, min_points_per_bin=2, fit_on="binned"):
    """
    Zipf style rank frequency plot with optional logarithmic binning.
    fit_on: "binned" or "raw"
    """
    frequencies = np.array(sorted(freq_dist.values(), reverse=True), dtype=float)
    ranks = np.arange(1, len(frequencies) + 1, dtype=float)

    plt.rcParams["font.family"] = "Times New Roman"

    # Bin for visualisation (and optionally for fitting)
    b_ranks, b_freqs = _log_bin_by_rank(ranks, frequencies, n_bins=n_bins, min_points_per_bin=min_points_per_bin)

    plt.figure(figsize=(8, 6))
    plt.xscale("log")
    plt.yscale("log")

    # Light raw curve for context
    plt.plot(ranks, frequencies, marker="o", linestyle="None", markersize=2, alpha=0.25, label="Raw")

    # Binned curve for clarity
    if len(b_ranks) > 0:
        plt.plot(b_ranks, b_freqs, marker="o", linestyle="None", markersize=5, label="Log binned")

    # Choose data for power law fit (in log10 space)
    if fit_on == "raw":
        x = ranks
        y = frequencies
    else:
        x = b_ranks
        y = b_freqs

    mask = (x > 0) & (y > 0)
    x = x[mask]
    y = y[mask]

    beta = np.nan
    if len(x) >= 2:
        logx = np.log10(x)
        logy = np.log10(y)
        coeffs = np.polyfit(logx, logy, 1)
        beta = coeffs[0]
        fitted_line = coeffs[0] * logx + coeffs[1]
        plt.plot(x, 10 ** fitted_line, linewidth=2, label="Fit")

        plt.text(
            0.95, 0.95, f"β = {beta:.2f}",
            transform=plt.gca().transAxes,
            fontsize=14, fontweight="bold", family="Times New Roman",
            bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3"),
            horizontalalignment="right", verticalalignment="top"
        )

    plt.title(f"Word frequency rank distribution in {title}", fontsize=16, fontweight="bold")
    plt.xlabel("Rank", fontsize=14, fontweight="bold")
    plt.ylabel("Frequency", fontsize=14, fontweight="bold")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return beta

def plot_freq_dist(inferno_clean, purgatorio_clean, paradiso_clean, binned = True):
    freq_inferno, freq_purgatorio, freq_paradiso = freq_dist(inferno_clean, purgatorio_clean, paradiso_clean)

    if binned == True:
        plot_word_frequency_rank_binned(freq_inferno, "Inferno")
        plot_word_frequency_rank_binned(freq_purgatorio, "Purgatorio")
        plot_word_frequency_rank_binned(freq_paradiso, "Paradiso")
    else:
        plot_word_frequency_rank(freq_inferno, 'Inferno')
        plot_word_frequency_rank(freq_purgatorio, 'Purgatorio')
        plot_word_frequency_rank(freq_paradiso, 'Paradiso')