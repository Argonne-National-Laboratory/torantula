import os
import sys

import networkx as nx
from networkx.readwrite import json_graph
from networkx.readwrite import gexf
import json

#TODO: Add more error handling

start = os.getcwd()

def get_subdirs(top_level_dir):
    """
    Returns subdirectories from a top-level directory. Thanks Josh McGiff
    :param top_level_dir: The directory within which to find subdirectories
    :return: A list of subdirectories
    """

    return [directory for directory in os.listdir(top_level_dir)
            if os.path.isdir(os.path.join(top_level_dir, directory))]

def get_links(subdir):
    """
    Returns the list of links stored by the scraper within a subdirectory
    :param subdir: A subdirectory within which to locate found_links.txt
    :return: A unique list of links to other domains
    """

    os.chdir(subdir)
    try:
        with open('found_links.txt', 'r') as f:
            readlinks = f.readlines()
            links = [x.strip()[:-6] for x in readlinks]  # Leave out .onion
            return list(set(links))
    except IOError:
        pass

def populate_graph(maindir):
    """
    Iterates through the given Scrape directory, checking each domain
    subdirectory for found_links. Creates a graph, then adds edges if they
    exist and nodes for each subdirectory.
    :param maindir: Scrape directory, with subdirectories for each domain
    :return: A populated networkx graph
    """
    nxgraph = nx.DiGraph()  # Directed graph
    dirs = get_subdirs(maindir)
    for subdir in dirs:

        nxgraph.add_node(subdir)    # Each visited directory is a legit node
        fulldir = maindir + subdir  # Full path to a domain directory
        links = get_links(fulldir)

        if links is not None and links != ['']:
            for link in links:
                nxgraph.add_edge(subdir, link)

    return nxgraph

def write_data(maindir, nxgraph):
    """
    Writes data from networkx graph to .json and .gexf file formats for
    rendering by other apps.
    :param maindir: Scrape directory, with subdirectories for each domain
    :param nxgraph: The networkx graph to be populated
    :return: None
    """
    data = json_graph.node_link_data(nxgraph)   # json formatted data
    filename = maindir.split('/')[-2]  # just the Scrape-directory filename
    os.chdir(start)  # Back to /Grapher
    with open('%s_graph.json' % filename, 'w') as w:
        json.dump(data, w)
    gexf.write_gexf(nxgraph, '%s_graph.gexf' % filename)

def main():
    """
    The main function notes the current directory and the directory of the
    passed-in scrape directory. Call functions to populate a graph, then write
    this data to disk.
    """

    maindir = sys.argv[1]   # Full Scrape directory

    nxgraph = populate_graph(maindir)  # Graph contains connectivity
    write_data(maindir, nxgraph)  # Written to disk in .json, .gexf

if __name__ == '__main__':
    main()
