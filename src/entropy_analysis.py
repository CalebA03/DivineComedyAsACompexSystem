import random
import matplotlib.pyplot as plt
from collections import Counter
import math

'''
Entropy pre-processing (additional steps to other processes). How we do this:

1. Take the pre-processed canticles from the network analysis - no lemmatisation because the text is old and lemmatisation may be innaccurate
'''

def split_canticle_into_canti(canticle_text):
    """
    Splits the canticle text into individual canti using '\n\n\n \n\n\n' as the separator.
    """
    # Define the specific separator for canti
    separator = '\n\n\n \n\n\n'
    
    # Split the text using the separator
    canti = canticle_text.split(separator)
    
    # Remove any leading/trailing whitespace from each canto and filter out empty ones
    return [canto.strip() for canto in canti if canto.strip()]


'''
Bigram entropy for each canto:
1. Iterates over each canto in a canticle and tokenises the text
2. the list of tokens for each canto is then split in tuples containing bigrams (words that appear together)
3. We then calculate the bigram entropy based on the frequency distribution of each bigram
4. Then the random bigram entropy is calculated by randomly rearranging all the tokens in a canto and calculating the shannon entropy of the resulting bigram frequency distribution averaged over 5 attempts
5. Relative entropy is then calculated by taking the random entropy and subtracting the real entropy
6. This is then plotted.'''

# Set global font style to Times New Roman
plt.rcParams["font.family"] = "Times New Roman"

def compute_ngrams(tokens, n=2):
    """
    Given a list of tokens, create all contiguous n-grams (default is bigrams).
    Example for n=2 (bigrams): ['love','thy','neighbour'] -> [('love','thy'), ('thy','neighbour')]
    """
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]

def calculate_ngram_entropy(tokens, n=2):
    """
    1) Create n-grams (bigrams if n=2).
    2) Calculate Shannon Entropy based on these n-grams' frequency distribution:
       H = -∑ p_i log2(p_i)
    """
    ngrams = compute_ngrams(tokens, n=n)
    freq_dist = Counter(ngrams)
    total = sum(freq_dist.values())
    entropy = -sum((freq / total) * math.log2(freq / total) for freq in freq_dist.values())
    return entropy

def calculate_ngram_entropy_random(tokens, n=2, n_shuffles=5, times=10):
    """
    Compute the average bigram entropy over multiple shuffled token lists.
    
    1) Shuffle the tokens `n_shuffles` times per iteration.
    2) Compute entropy for each shuffled token sequence.
    3) Repeat this `times` times to get a stable average.
    4) Return the average entropy.
    """
    entropy_list = []

    for _ in range(times):
        entropies = []
        for _ in range(n_shuffles):
            shuffled = tokens[:]
            random.shuffle(shuffled)
            entropies.append(calculate_ngram_entropy(shuffled, n=n))

        entropy_list.append(sum(entropies) / len(entropies))  # Store avg entropy for this iteration

    return sum(entropy_list) / len(entropy_list)  # Return overall avg entropy

def relative_ngram_entropy_canto(canto_tokens, n=2):
    """
    Calculate the relative entropy for a single canto:
    Relative Entropy = H_rand - H_orig
    """
    # Original bigram entropy
    H_orig = calculate_ngram_entropy(canto_tokens, n=n)

    # Random bigram entropy (averaged over multiple shuffles)
    H_rand = calculate_ngram_entropy_random(canto_tokens, n=n, n_shuffles=5)

    return H_rand - H_orig

def compute_relative_ngram_entropy_for_cantos(canti, n=2):
    """
    Applies relative_ngram_entropy_canto to each canto in 'canti' using n-grams of length n.
    Returns a list of (canto_index, relative_entropy).
    """
    results = []
    for idx, canto in enumerate(canti, start=1):
        # Tokenize each canto (assuming it's preprocessed and split into tokens)
        tokens = canto.split()  # Split the canto into tokens
        re_val = relative_ngram_entropy_canto(tokens, n=n)
        results.append((idx, re_val))
    return results

def plot_relative_entropy_journey(entropies, title):
    """
    Plots the relative n-gram entropy per canto in a simple line plot.
    """
    indices = [idx for idx, val in entropies]
    values = [val for idx, val in entropies]

    plt.figure(figsize=(10, 6))
    plt.plot(indices, values, marker='o', color='black')  # Set line color to black for readability
    plt.xlabel('Canto number', fontsize=12)
    plt.ylabel('Relative bigram entropy', fontsize=12)
    plt.grid(True)
    plt.show()



def evaluate_canti_entropy(inferno_clean, purgatorio_clean, paradiso_clean, n=2, canticle = 'inferno'): 
    
    # split into canti
    canti_inferno = split_canticle_into_canti(inferno_clean)
    canti_purgatorio = split_canticle_into_canti(purgatorio_clean)
    canti_paradiso = split_canticle_into_canti(paradiso_clean)

    #print results
    print("Number of Canti - Inferno:", len(canti_inferno)) 
    print("Number of Canti - Purgatorio:", len(canti_purgatorio))
    print("Number of Canti - Paradiso:", len(canti_paradiso))

    if canticle == "inferno":
        entropies_inferno = compute_relative_ngram_entropy_for_cantos(canti_inferno, n=n)  # bigrams
        plot_relative_entropy_journey(entropies_inferno, 'Relative N-gram Entropy across Canti')
    elif canticle == "prugatorio":
        entropies_purgatorio = compute_relative_ngram_entropy_for_cantos(canti_purgatorio, n=n)  # bigrams
        plot_relative_entropy_journey(entropies_purgatorio, 'Relative N-gram Entropy across Canti')
    elif canticle == "paradiso":
        entropies_paradiso = compute_relative_ngram_entropy_for_cantos(canti_paradiso, n=n)  # bigrams
        plot_relative_entropy_journey(entropies_paradiso, 'Relative N-gram Entropy across Canti')
