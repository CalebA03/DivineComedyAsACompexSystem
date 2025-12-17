from src.preprocessing import preprocessing
from src.create_networks import create_networks
from src.display_network import display_network
from src.centrality_measures import plot_evaluate_centrality_measures
from src.frequency_analysis import plot_freq_dist
from src.entropy_analysis import evaluate_canti_entropy

def main():
    # reads in the txt file for the Divine comedy and does preprocessing (Accessed from Alighieri, D., Doré, G. and Cary, H.F. (2023) The divine comedy by Dante Alighieri, Project Gutenberg. Available at: https://www.gutenberg.org/ebooks/8800 (Accessed: 17 September 2024). )
    inferno_clean, purgatorio_clean, paradiso_clean , whole_clean = preprocessing()

    # Turn txt into an adjacency network
    G_inferno, G_paradiso, G_purgatorio, G_whole = create_networks(inferno_clean, purgatorio_clean, paradiso_clean , whole_clean)
    
    #visualise the network (commented out as it take a while to run)
    #display_network(G_whole)

    #Display the measures of centrality (plotting only the eigenvector centrality)
    plot_evaluate_centrality_measures(G_inferno, G_purgatorio, G_paradiso)

    #plot the frequency distribution of the words, set binned = False or True depending on whether you want to view the binned results
    plot_freq_dist(inferno_clean, purgatorio_clean, paradiso_clean, binned = True)

    # plots and evaluates entropy by canti using shannon entropy with an n-grams of n and only generates a plot for the specific canticle that you want (this only takes "inferno", "paradiso", or "purgatorio")
    evaluate_canti_entropy(inferno_clean, purgatorio_clean, paradiso_clean, n=2, canticle = 'inferno')

main()