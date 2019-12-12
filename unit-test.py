import MuPhenS as muph
import networkx as nx

def test_init():
    muphen = muph.MuPhenS()

    # validate that all variables are initialized as expected
    assert len(muphen.source_ids) == 0, 'length of MuPhenS.source_ids should be 0'
    assert len(muphen.source_labels) == 0, 'length of MuPhenS.source_labels should be 0'
    assert len(muphen.target_ids) == 0, 'length of MuPhenS.target_ids should be 0'
    assert len(muphen.target_labels) == 0, 'length of MuPhenS.target_labels should be 0'
    assert muphen.paths is None, 'MuPhenS.paths should be None'
    assert muphen.small_graph is None, 'MuPhenS.small_graph should be None'
    assert muphen.webweb is None, 'MuPhenS.webweb should be None'
    assert muphen.outputfile == 'network-plot.png', 'MuPhenS.outputfile should be "network-plot.png"'

    # validate that the network read in correctly
    assert muphen.G is not None, 'MuPhenS.G should be a networkx object, not None'

    # validate number of nodes and edges in G
    assert len(muphen.G.nodes) == 109272, 'The number of nodes in G should be 109272 not ' + str(len(muphen.G.nodes))
    assert len(muphen.G.edges) == 1461016, 'The number of edges in G should be 1461016 not ' + str(len(muphen.G.edges))


def test_single_search():
    muphen = muph.MuPhenS()

    # Test short path, length 3
    # KCNQ2
    source = '<http://purl.uniprot.org/geneid/3785>'
    # Infantile spasms
    target = '<http://purl.obolibrary.org/obo/HP_0012469>'
    path = muphen.single_search(source, target)
    assert len(path) == 3, 'path should be length 3'

    # Test path no found
    # DEAF1
    source = '<http://purl.uniprot.org/geneid/10522>'
    # Encephalopathy
    target = '<http://purl.obolibrary.org/obo/HP_0012469>'
    found = False
    path = None
    try:
        path = muphen.single_search(source, target)
        found = True
    except nx.exception.NetworkXNoPath:
        found = False
    assert not found, 'path from ' + source + ' to ' + target + ' should not have been found'



if __name__ == "__main__":
    test_init()
    test_single_search()
