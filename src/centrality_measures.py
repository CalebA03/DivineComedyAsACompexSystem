import networkx as nx
import matplotlib.pyplot as plt

'''
How do we calculate the centrality measures? - Note that each of these measures account for the weighting of the edges.
    1. We compute the degree centrality for all nodes in the graph by calculating the sum of all edge weights to each node and normalise this centrality by the total possible weighted edges in the graph. We then sort the nodes in descending order of centrality value.
    2. We compute betweenness centrality by computing the number of shortests paths a node lies on between other nodes accounting for edge weights. We use a parameter k=5000 to determine how many of these paths we sample to get our results. These are then sorted in descending order of centrality value
    3. To compute the eigenvector centrality, we measure the nodes centrality based on the influence of its surrounding nodes. These are then sorted into descending order of centrality value.
'''

def top_centrality_measures_weighted(G, top_n=10):
    # Weighted Degree Centrality
    weighted_degree_centrality = {node: sum(data['weight'] for _, _, data in G.edges(node, data=True)) for node in G.nodes()}
    top_weighted_degree = sorted(weighted_degree_centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Betweenness Centrality
    betweenness_centrality = nx.betweenness_centrality(G, weight='weight', k=1000)
    top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Eigenvector Centrality
    eigenvector_centrality = nx.eigenvector_centrality_numpy(G, weight='weight')
    top_eigenvector = sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:top_n]

    return top_weighted_degree, top_betweenness, top_eigenvector



# Function to print results
def print_top_centrality_weighted(title, top_weighted_degree, top_betweenness, top_eigenvector):
    print(f'\nTop 10 Words by Weighted Degree Centrality - {title}')
    for word, centrality in top_weighted_degree:
        print(f'{word}: {centrality:.3f}')
    print(f'\nTop 10 Words by Betweenness Centrality - {title}')
    for word, centrality in top_betweenness:
        print(f'{word}: {centrality:.3f}')
    print(f'\nTop 10 Words by Eigenvector Centrality - {title}')
    for word, centrality in top_eigenvector:
        print(f'{word}: {centrality:.3f}')
        


'''
High-centrality sub-graphs

How do we do this?
    1. Create a set of sub-graph nodes that initially contains the top weighted nodes - by eigenvector centrality
    2. For each of these top nodes, we then iterate through its neighbours
    3. We then retrieve the neighbours with the top 5 weights, add these to sub-graph nodes and store their weights
    4. Graph the top nodes and the sub-graph nodes
    5. To plot these we let node size be determined by degree, central node as in blue, neighbour nodes are in red.
'''

def create_high_centrality_subgraph(G, top_nodes, top_n_edges=5, centrality_nodes=set()):
    """
    Create a subgraph containing the top eigenvector centrality nodes and their highest-weighted neighbors, ensuring connections between top neighbors and other top centrality nodes.
    """
    sub_nodes = set(top_nodes)  # Initialize with top eigenvector centrality nodes
    edges = []  # Store edges to build the subgraph

    for node in top_nodes:
        if node in G:
            neighbors = list(G.neighbors(node))
            # Collect weights for edges to neighbors
            neighbor_weights = [
                (neighbor, G[node][neighbor]['weight'])
                for neighbor in neighbors if node != neighbor  # Exclude self-loops
            ]
            # Sort neighbors by edge weight (highest first)
            neighbor_weights.sort(key=lambda x: x[1], reverse=True)
            # Get top weighted neighbors
            top_neighbors = [neighbor for neighbor, _ in neighbor_weights[:top_n_edges]]
            sub_nodes.update(top_neighbors)  # Add neighbors to the subgraph nodes
            # Add edges between the node and its top neighbors
            for neighbor in top_neighbors:
                edges.append((node, neighbor, G[node][neighbor]['weight']))

    # Add edges between highly weighted neighbors or other top centrality nodes
    for node in sub_nodes:
        if node in G:
            for neighbor in G.neighbors(node):
                if neighbor in sub_nodes and node != neighbor:
                    edges.append((node, neighbor, G[node][neighbor]['weight']))

    # Build the subgraph
    subgraph = nx.Graph()
    for u, v, weight in edges:
        if u != v:  # Ensure no self-loops
            subgraph.add_edge(u, v, weight=weight)

    return subgraph


def display_subgraph(subgraph, central_nodes):
    """
    Display the subgraph highlighting central nodes and their neighbors.
    """
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(subgraph, k=0.5, seed=42)
    degrees = dict(subgraph.degree())
    node_sizes = [degrees[node] * 400 for node in subgraph.nodes()]
    # Colors: blue for central nodes, red for neighbors
    node_color = ['steelblue' if node in central_nodes else 'lightcoral' for node in subgraph.nodes()]
    # Draw nodes and edges
    nx.draw_networkx_nodes(subgraph, pos, node_size=node_sizes, node_color=node_color, alpha=0.9)
    nx.draw_networkx_edges(subgraph, pos, edge_color='gray', alpha=0.7)
    # Add labels
    nx.draw_networkx_labels(subgraph, pos, font_size=12, font_color='black')
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def plot_evaluate_centrality_measures(G_inferno, G_purgatorio, G_paradiso):
    # Inferno
    top_weighted_degree_inferno, top_betweenness_inferno, top_eigenvector_inferno = top_centrality_measures_weighted(G_inferno)
    # Purgatorio
    top_weighted_degree_purgatorio, top_betweenness_purgatorio, top_eigenvector_purgatorio = top_centrality_measures_weighted(G_purgatorio)
    # Paradiso
    top_weighted_degree_paradiso, top_betweenness_paradiso, top_eigenvector_paradiso = top_centrality_measures_weighted(G_paradiso)

    # Print results for each canticle
    print_top_centrality_weighted('Inferno', top_weighted_degree_inferno, top_betweenness_inferno, top_eigenvector_inferno)
    print_top_centrality_weighted('Purgatorio', top_weighted_degree_purgatorio, top_betweenness_purgatorio, top_eigenvector_purgatorio)
    print_top_centrality_weighted('Paradiso', top_weighted_degree_paradiso, top_betweenness_paradiso, top_eigenvector_paradiso)
    
    # Inferno
    top_eigenvector_nodes_inferno = [node for node, _ in top_eigenvector_inferno]
    subgraph_inferno = create_high_centrality_subgraph(
        G_inferno, top_eigenvector_nodes_inferno, top_n_edges=5, centrality_nodes=set(top_eigenvector_nodes_inferno[:10])
    )
    print("Inferno - High Eigenvector Centrality Subgraph")
    display_subgraph(subgraph_inferno, top_eigenvector_nodes_inferno)

    # Purgatorio
    top_eigenvector_nodes_purgatorio = [node for node, _ in top_eigenvector_purgatorio]
    subgraph_purgatorio = create_high_centrality_subgraph(
        G_purgatorio, top_eigenvector_nodes_purgatorio, top_n_edges=5, centrality_nodes=set(top_eigenvector_nodes_purgatorio[:10])
    )
    print("Purgatorio - High Eigenvector Centrality Subgraph")
    display_subgraph(subgraph_purgatorio, top_eigenvector_nodes_purgatorio)

    # Paradiso
    top_eigenvector_nodes_paradiso = [node for node, _ in top_eigenvector_paradiso]
    subgraph_paradiso = create_high_centrality_subgraph(
        G_paradiso, top_eigenvector_nodes_paradiso, top_n_edges=5, centrality_nodes=set(top_eigenvector_nodes_paradiso[:10])
    )
    print("Paradiso - High Eigenvector Centrality Subgraph")
    display_subgraph(subgraph_paradiso, top_eigenvector_nodes_paradiso)
