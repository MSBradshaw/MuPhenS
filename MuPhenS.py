import sys
import pickle
import networkx as nx
import matplotlib.pyplot as plt
from webweb import Web
import pandas as pd

RED_TEXT = '\033[31m'
ORANGE_TEXT = '\033[33m'
COLOR_RESET = reset='\033[0m'


class MuPhenS:

    """
    Initializes the MuPhenS object
    Reads in the network from the pickle
    Define some test data sets
    """

    def __init__(self):
        # Initialize member variables
        self.source_ids = []
        self.source_labels = []
        self.target_ids = []
        self.target_labels = []
        self.paths = None
        self.small_graph = None
        self.webweb = None
        self.outputfile = 'network-plot.png'
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
            if len(path) is 1:
                self.small_graph.add_node(path[0])

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

        for t in self.target_ids:
            for s in self.source_ids:
                try:
                    # get the path from the gene to the disease and add the new path ot the list of paths
                    self.paths.append(self.single_search(s, t))
                except nx.exception.NetworkXNoPath:
                    print(ORANGE_TEXT + 'Warning: No path between source: ' + s + ' and target: ' + t)
                    print(COLOR_RESET)
                    # Add the node to paths so that is still appears in the network, but unconnected to everything else
                    self.paths.append([s])

        # make a smaller networks out of the paths found, save in self.small_graph
        self.make_network_of_paths(self.paths)

    """
    Plots the information currently stored in self.small_graph
    Displayed 1 of 2 types of plots based on self.webweb (boolean) 
        True: plot the network using the webweb internet display
        False: plot the network using the default networkx functionality
    """

    def plot(self):
        # Initialize all nodes in network with and empty name
        nx.set_node_attributes(self.small_graph, '', 'Name')

        # Give all genes a proper name
        for i in range(len(self.source_ids)):
            n = self.source_ids[i]
            self.small_graph.nodes[n]['Name'] = self.source_labels[i]

        # Give all genes a proper name
        for i in range(len(self.target_ids)):
            n = self.target_ids[i]
            self.small_graph.nodes[n]['Name'] = self.target_labels[i]

        # Extract the labels from the network
        labels = nx.get_node_attributes(self.small_graph, 'Name')

        if not self.webweb:
            pos = nx.spring_layout(self.small_graph)
            nx.draw_networkx(self.small_graph, with_labels=False, pos=pos)
            nx.draw_networkx_labels(self.small_graph, pos, labels, font_weight='bold')
            plt.savefig(self.outputfile)
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
    Reads in the given file path provided as filename
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
        source_ids, source_labels = self.read_file(source_file)
        target_ids, target_labels = self.read_file(target_file)

        for i in range(len(source_ids)):
            source_ids[i] = '<http://purl.uniprot.org/geneid/' + source_ids[i] + '>'
            # check if that node in in the network: otherwise exclude it
            if not self.G.has_node(source_ids[i]):
                print(ORANGE_TEXT + 'Node not found in network and is being excluded: ' + source_ids[i] + ' label: ' +
                      source_labels[i])
                print(COLOR_RESET)
            else:
                self.source_ids.append(source_ids[i])
                self.source_labels.append(source_labels[i])

        for i in range(len(target_ids)):
            target_ids[i] = '<http://purl.obolibrary.org/obo/HP_' + target_ids[i] + '>'
            # check if that node in in the network: otherwise exclude it
            if not self.G.has_node(target_ids[i]):
                print(ORANGE_TEXT + 'Node not found in network and is being excluded: ' + target_ids[i] + ' label: ' +
                      target_labels[i])
                print(COLOR_RESET)
            else:
                self.target_ids.append(target_ids[i])
                self.target_labels.append(target_labels[i])

    """
    Confirms that the parameters being passed in are the correct number and type of input
    """

    def validate_input(self,args):
        length = len(args)
        if length < 3:
            print(RED_TEXT + "Improper number of parameters!" + COLOR_RESET)
            self.help_information()
            quit()
        elif length is 3:
            return
        elif length is 4 or length is 5:
            print('here')
            if args[3] != 'webweb' and args[3] != 'default':
                print(RED_TEXT + 'Parameter 3 must be "webweb" or "default" not: "' + args[3] + '"' + COLOR_RESET)
                quit()
            else:
                if args[3] == 'webweb':
                    self.webweb = True
                else:
                    self.webweb = False
            if length is 5:
                if args[4][-4:] != '.png':
                    print(RED_TEXT + 'Parameter 4 must be a .png' + COLOR_RESET)
                    quit()
                else:
                    self.outputfile = args[4]

        else:
            print(RED_TEXT + "Improper number of parameters!" + COLOR_RESET)
            self.help_information()
            quit()

    """
    Prints the information about how to use MuPhenS
    """

    def help_information(self):
        print('Proper use of MuPhenS:')
        print('Required Parameters:')
        print('\t1. Sources file - csv file, first column is the gene ids second column is gene labels. Do not include '
              'any header lines or column names')
        print('\t2. Target file - csv file, first column is the gene ids second column is gene labels. Do not include '
              'any header lines or column names')
        print('Optional Parameters')
        print('\t3. Type of plot output - options "webweb" or "default"')
        print('\t4. Output figure name - must a .png type. Figure will only be saved if using default type plot')
        print('Example: python MuPhenS.py eeie-id-name.csv eeie-targets.csv default network-plot.png')


if __name__ == "__main__":
    muphen = MuPhenS()
    muphen.validate_input(sys.argv)
    muphen.load_files(sys.argv[1], sys.argv[2])
    muphen.get_gene_to_pheno_path()
    muphen.plot()
