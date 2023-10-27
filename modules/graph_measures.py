import numpy as np
import networkx as nx
import bct


def global_efficiency(connectivity_matrix):
    e_glob = bct.efficiency_wei(connectivity_matrix, local=False)
    return e_glob


def mean_local_efficiency(connectivity_matrix):
    e_loc = bct.efficiency_wei(connectivity_matrix, local=True)
    mean_e_loc = np.mean(e_loc)
    return mean_e_loc


def modularity(connectome):
    partitions = nx.community.louvain_communities(connectome, weight='weight')
    q = nx.community.modularity(connectome, partitions, weight='weight')
    return q


def largest_connected_component(connectome):
    largest_cc = max(nx.connected_components(connectome), key=len)
    return len(largest_cc) / len(connectome.nodes)


def mean_participation_coefficient(connectome, module_partition, modules_pc):
    for module in module_partition:
        module_subgraph = set(module_partition[module]['nodes'])
        nodes_pc = []
        for node in module_subgraph:
            degree = float(nx.degree(G=connectome, nbunch=node))
            # intramodule degree of node
            wm_degree = float(sum([1 for u in module_subgraph if (u, node) in connectome.edges()]))

            # The participation coefficient is 1 - the square of
            # the ratio of the within module degree and the total degree
            if degree == 0:
                nodes_pc.append(0)
            else:
                nodes_pc.append(1 - (wm_degree / degree) ** 2)
        modules_pc[module].append(np.mean(nodes_pc))

    return modules_pc
