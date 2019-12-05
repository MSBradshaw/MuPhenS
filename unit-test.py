import PheGe as pg
import networkx as nx

def test_init():
    p = pg.PheGe()

    # validate that all variables are initialized as expected
    assert len(p.source_ids) == 0, 'length of PheGe.source_ids should be 0'
    assert len(p.source_labels) == 0, 'length of PheGe.source_labels should be 0'
    assert len(p.target_ids) == 0, 'length of PheGe.target_ids should be 0'
    assert len(p.target_labels) == 0, 'length of PheGe.target_labels should be 0'
    assert p.paths is None, 'PheGe.paths should be None'
    assert p.small_graph is None, 'PheGe.small_graph should be None'
    assert p.webweb is None, 'PheGe.webweb should be None'
    assert p.outputfile == 'network-plot.png', 'PheGe.outputfile should be "network-plot.png"'

    # validate that the network read in correctly
    assert p.G is not None, 'PheGe.G should be a networkx object, not None'

    # validate number of nodes and edges in G
    assert len(p.G.nodes) == 109272, 'The number of nodes in G should be 109272 not ' + str(len(p.G.nodes))
    assert len(p.G.edges) == 1461016, 'The number of edges in G should be 1461016 not ' + str(len(p.G.edges))


def test_single_search():
    p = pg.PheGe()

    # Test short path, length 3
    # KCNQ2
    source = '<http://purl.uniprot.org/geneid/3785>'
    # Infantile spasms
    target = '<http://purl.obolibrary.org/obo/HP_0012469>'
    path = p.single_search(source, target)
    assert len(path) == 3, 'path should be length 3'

    # Test path no found
    # DEAF1
    source = '<http://purl.uniprot.org/geneid/10522>'
    # Encephalopathy
    target = '<http://purl.obolibrary.org/obo/HP_0012469>'
    found = False
    path = None
    try:
        path = p.single_search(source, target)
        found = True
    except nx.exception.NetworkXNoPath:
        found = False
    assert not found, 'path from ' + source + ' to ' + target + ' should not have been found'



if __name__ == "__main__":
    test_init()
    test_single_search()
