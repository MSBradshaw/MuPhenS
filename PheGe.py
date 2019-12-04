import sys
import pickle
import networkx as nx
import matplotlib.pyplot as plt
from webweb import Web
import pandas as pd

RED_TEXT = '\033[31m'


class PheGe:

    """
    Initializes the PheGe object
    Reads in the network from the pickle
    Define some test data sets
    """

    def __init__(self):
        # Initialize member variables
        self.source_ids = None
        self.source_labels = None
        self.target_ids = None
        self.target_labels = None
        self.paths = None
        self.small_graph = None
        # Load the network from the pickle
        self.G = None
        with (open('network.gpickle', 'rb')) as openfile:
            self.G = pickle.load(openfile)

    """
    Given a set of paths create a directed network saved in the member variable self.small_graph 
    """

    def make_network_of_paths(self, paths):
        self.small_graph = nx.DiGraph()
        for path in paths:
            for i in range(len(path) - 1):
                self.small_graph.add_edge(path[i], path[i + 1])

    """
    Find a path between a given source and target node
    """

    def single_search(self, source, target):
        return nx.shortest_path(self.G, source=source, target=target)

    """
    Find paths between all source and target nodes
    Source and targets are taken from the member variables self.source_ids and self.target_ids
    If a path is not found, the error is handled and reported
    """

    def get_gene_to_pheno_path(self):
        self.paths = []
        # find paths from all sources to all targets
        s = ''
        t = ''

        for target in self.target_ids:
            t = '<http://purl.obolibrary.org/obo/HP_' + target + '>'
            for id in self.source_ids:
                s = '<http://purl.uniprot.org/geneid/' + id + '>'
                try:
                    # get the path from the gene to the disease and add the new path ot the list of paths
                    self.paths.append(self.single_search(s, t))
                except nx.exception.NetworkXNoPath:
                    print(RED_TEXT + 'Warning: No path between source: ' + s + ' and target: ' + t)

        # make a smaller networks out of the paths found, save in self.small_graph
        self.make_network_of_paths(self.paths)

    """
    Plots the information currently stored in self.small_graph
    webweb (boolean) 
        True: plot the network using the webweb internet display
        False: plot the network using the default networkx functionality
    """

    def plot(self, webweb=False):
        # Initialize all nodes in network with and empty name
        nx.set_node_attributes(self.small_graph, '', 'Name')

        # Give all genes a proper name
        for i in range(len(self.source_ids)):
            n = '<http://purl.uniprot.org/geneid/' + self.source_ids[i] + '>'
            self.small_graph.nodes[n]['Name'] = self.source_labels[i]

        # Give all genes a proper name
        for i in range(len(self.target_ids)):
            n = '<http://purl.obolibrary.org/obo/HP_' + self.target_ids[i] + '>'
            self.small_graph.nodes[n]['Name'] = self.target_labels[i]

        # Extract the labels from the network
        labels = nx.get_node_attributes(self.small_graph, 'Name')

        if not webweb:
            pos = nx.spring_layout(self.small_graph)
            nx.draw_networkx(self.small_graph, with_labels=False, pos=pos)
            nx.draw_networkx_labels(self.small_graph, pos, labels, font_weight='bold')
            plt.show()
        else:
            ww_labels = {}
            count = 0
            for l in labels.values():
                v = l
                if l == '':
                    v = str(count)
                ww_labels[count] = {'name': v}
                count += 1
            w = Web(adjacency=nx.to_numpy_array(self.small_graph), display={'nodes': ww_labels})
            # set some default visualization settings in webweb
            w.display.linkLength = 100
            w.display.charge = 200
            w.display.showNodeNames = True
            w.display.colorBy = 'degree'
            w.show()

    """
    Reads in the given filepath provided as filename
    Returns list of ids and list of labels
    Assumptions:
    1. Files is a csv
    2. There are not column names or headers
    3. The first column contains the ids
    4. The second column contains the labels
    """

    def read_file(self, filename):
        # read files in assuming there is are no headers and everything is a string (so leading 0's are not removed)
        sources = pd.read_csv(filename, header=None, dtype=object)
        return list(sources.iloc[:, 0]), list(sources.iloc[:, 1])

    """
    Takes the path to the source and target file. 
    Reads them in and store information in self.source_ids, self.source_labels, self.target_ids, self.target_labels
    """

    def load_files(self, source_file, target_file):
        self.source_ids, self.source_labels = self.read_file(source_file)
        self.target_ids, self.target_labels = self.read_file(target_file)


if __name__ == "__main__":
    p = PheGe()
    p.load_files('eeie-id-name.csv', 'eeie-targets.csv')
    p.get_gene_to_pheno_path()
    p.plot(True)
