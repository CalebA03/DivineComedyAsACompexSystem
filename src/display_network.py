import matplotlib.pyplot as plt
import networkx as nx

'''How do we display the network:
1. Generate node positions using the spring layout algorithm (seed = 42)
2. Calculate node sizes by the degree of each node (weighted degree) and scale node size proportionally to the degree
3. To visualise nodes we assign a unique colour based on location, size based on degree, grey edges, no node borders, use a viridis colour scheme, and disable node labels.'''


def display_network(G):
    # Set figure size
    plt.figure(figsize=(14, 10))

    # Generate a spring layout with limited iterations for faster computation
    pos = nx.spring_layout(G, iterations=20, seed=42)  # Reduce iterations to speed up layout generation

    # Calculate node degrees to scale node sizes
    degrees = dict(G.degree(weight='weight'))
    node_sizes = [degrees[node] for node in G.nodes()]

    # Use a gradient color map for nodes
    node_colors = range(len(G.nodes()))
    cmap = plt.cm.viridis

    # Subsample edges for dense graphs
    edges_to_draw = list(G.edges(data=True))

    # Draw the graph
    nx.draw_networkx_nodes(
        G, pos,
        node_size=[size * 5 for size in node_sizes],  # Reduce scaling factor for node sizes
        node_color=node_colors,
        cmap=cmap,
        alpha=0.7  # Slightly reduce alpha for better visual clarity
    )

    nx.draw_networkx_edges(
        G, pos,
        edgelist=edges_to_draw,
        edge_color='gray',
        alpha=0.4,  # Increase transparency for less visual clutter
        width=0.3  # Reduce edge width further
    )

    # Turn off axis
    plt.axis('off')

    # Show plot
    plt.show()

# Visualize the graph
#display_network(G_whole)
