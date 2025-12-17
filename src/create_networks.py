import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import networkx as nx

nltk.download('punkt')
nltk.download('stopwords')



'''
How do we create the network?
1. Split the text into individual "tokens" which are the words
2. Remove stop-words (common filler words) - generic nltk italian stop words library plus custom words: ['altro','altri','e','lor','giù','com','laltro','elli','te','tal','sù','or','ciò','chè','sé','pur','fa','cha','son','disse','vidi','ché','né','però','chio','ancor','qui','pero','qual', 'già', 'così', 'là', 'de', 'poi', 'quando', 'quel', 'sì', 'gia', 'me', 'ne', 'non', 'che', 'di', 'la', 'il', 'le', 'lo', 'gli', 'dei', 'delle', 'un', 'una', 'uno']
3. Build an adjacency list by iterating through pairs of consecutive tokens and adding unique pairs to a dictionary of adjacent tokens. If the pair is already in the list, then we increment the weight of the pair by 1. 
4. Use the networkx library to visualise the graph created by the adjacency list.

'''

# Define function to create word-adjacency network
def create_word_adjacency_network(text):
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('italian'))
    # Additional Italian stopwords
    additional_stopwords = ['altro','tanto','altri','e', 'ei','lor','giù','com','laltro','elli','te','tal','sù','or','ciò','chè', 'sé','pur','fa','cha','son','disse','vidi','ché','né','però','chio','ancor','qui','pero','qual', 'già', 'così', 'là', 'de', 'poi', 'quando', 'quel', 'sì', 'gia', 'me', 'ne', 'non', 'che', 'di', 'la', 'il', 'le', 'lo', 'gli', 'dei', 'delle', 'un', 'una', 'uno']
    stop_words.update(additional_stopwords)
    tokens = [word for word in tokens if word not in stop_words]
    # Build adjacency list
    adjacency = {}
    for i in range(len(tokens) - 1):
        pair = (tokens[i], tokens[i + 1])
        if pair in adjacency:
            adjacency[pair] += 1
        else:
            adjacency[pair] = 1
    # Create the network
    G = nx.Graph()
    for (word1, word2), weight in adjacency.items():
        G.add_edge(word1, word2, weight=weight)
    return G

def create_networks(inferno_clean, purgatorio_clean, paradiso_clean , whole_clean):
    # Create networks
    G_inferno = create_word_adjacency_network(inferno_clean)
    G_purgatorio = create_word_adjacency_network(purgatorio_clean)
    G_paradiso = create_word_adjacency_network(paradiso_clean)
    G_whole = create_word_adjacency_network(whole_clean)
    return G_inferno, G_paradiso, G_purgatorio, G_whole
