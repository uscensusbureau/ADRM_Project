import copy
import time

import community as louvain
import networkx as nx
import numpy as np
from tqdm import tqdm


# Louvain method of commnuity detection using modularity optimization based on:
# Blondel, V. D., Guillaume, J. L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large
# networks. Journal of statistical mechanics: theory and experiment, 2008(10), P10008.
# I am using cluster, partition, community interchangeably to refer to the same thing


# entry point
def networkx_modularity_graph_clustering(nodes, edges):
    g = nx.Graph()
    g.add_weighted_edges_from(edges)
    final_clusters = louvain.best_partition(g, partition=nodes)
    return final_clusters


def akef_modularity_graph_clustering(nodes, edges):
    final_clusters = optimize_modularity(nodes, edges)
    return final_clusters


# network initialization
def simple_network_init(cluster, compareCache):
    edges = []
    for s1 in cluster:
        for s2 in cluster:
            if s1 < s2:
                key = s1 + ":" + s2
                if key in compareCache.keys():
                    edges.append((s1, s2,
                                  float(compareCache[key])))
            if s2 < s1:
                key = s2 + ":" + s1
                if key in compareCache.keys():
                    edges.append((s2, s1,
                                  float(compareCache[key])))
    edges = sorted(edges, key=lambda item: item[2], reverse=True)
    unique_nodes = []
    for edge in edges:
        source_node = edge[0]
        target_node = edge[1]
        unique_nodes.append(source_node)
        unique_nodes.append(target_node)
    unique_nodes = list(np.unique(np.array(unique_nodes)))
    # Initialize node partition membership
    nodes = {}
    partition = 0
    for n in unique_nodes:
        nodes[n] = partition
        partition = partition + 1
    return nodes, edges


def initialize_network_block_level(compareCache):
    refid_list = []
    edges = []
    for key, value in compareCache.items():
        refids = key.split(":")
        if refids[0] < refids[1]:
            edges.append((refids[0], refids[1], float(value)))
        if refids[1] < refids[0]:
            edges.append((refids[1], refids[0], float(value)))
        refid_list = refid_list + refids
    unique_nodes = list(np.unique(np.array(refid_list)))
    edges = sorted(edges, key=lambda item: item[2], reverse=True)
    # Initialize node partition membership
    nodes = {}
    partition = 0
    for n in unique_nodes:
        nodes[n] = partition
        partition = partition + 1
    return nodes, edges


def initialize_network(cluster, compareCache):
    cluster_list = cluster
    edges = []
    for s1 in tqdm(range(len(cluster_list))):
        reference_tokenized_1 = cluster_list[s1]["ref"].split()
        ref_id_1 = str(cluster_list[s1]["ref_id"])
        for s2 in range(len(cluster_list)):
            reference_tokenized_2 = cluster_list[s2]["ref"].split()
            ref_id_2 = str(cluster_list[s2]["ref_id"])
            if ref_id_1 < ref_id_2:
                key = ref_id_1 + ":" + ref_id_2
                if key in compareCache.keys():
                    edges.append((ref_id_1, ref_id_2,
                                  float(compareCache[key])))
            if ref_id_2 < ref_id_1:
                key = ref_id_2 + ":" + ref_id_1
                if key in compareCache.keys():
                    edges.append((ref_id_2, ref_id_1,
                                  float(compareCache[key])))
    edges = sorted(edges, key=lambda item: item[2], reverse=True)
    unique_nodes = []
    for edge in edges:
        source_node = edge[0]
        target_node = edge[1]
        unique_nodes.append(source_node)
        unique_nodes.append(target_node)
    unique_nodes = list(np.unique(np.array(unique_nodes)))
    # Initialize node partition membership
    nodes = {}
    partition = 0
    for n in unique_nodes:
        nodes[n] = partition
        partition = partition + 1
    return nodes, edges


def initialize_communities_from_edges(edges):
    unique_nodes = []
    for edge in edges:
        source_node = edge[0]
        target_node = edge[1]
        unique_nodes.append(source_node)
        unique_nodes.append(target_node)
    unique_nodes = list(np.unique(np.array(unique_nodes)))
    # Initialize node partition membership
    nodes = {}
    partition = 0
    for n in unique_nodes:
        nodes[n] = partition
        partition = partition + 1
    return nodes


# graph search functions
def find_involved_edges(node, edges):
    involved_edges = []
    for e in edges:
        source_node = e[0]
        target_node = e[1]
        weight = e[2]
        if (source_node == node) or (target_node == node):
            involved_edges.append((source_node, target_node, weight))
    return involved_edges


def find_shared_nodes_of_partition(partition, edges):
    source_nodes = []
    target_nodes = []
    weights = []
    shared_nodes = []
    for n in partition:
        for e in edges:
            source_node = e[0]
            target_node = e[1]
            weight = e[2]
            if (source_node == n) or (target_node == n):
                source_nodes.append(source_node)
                target_nodes.append(target_node)
                weights.append(weight)
    for s in source_nodes:
        c = source_nodes.count(s)
        if c > 1:
            involved_edges = find_involved_edges(s, edges)
            for ie in involved_edges:
                s_n = ie[0]
                t_n = ie[1]
                w = ie[2]
                if ((s_n == s) and (t_n in partition)) or ((t_n == s) and (s_n in partition)):
                    shared_nodes.append((s, w))
    return shared_nodes


def get_neighborhood(record_node, edges):
    neighborhood_nodes = []
    for edge in edges:
        source_node = edge[0]
        target_node = edge[1]
        if record_node == source_node:
            neighborhood_nodes.append(target_node)
        if record_node == target_node:
            neighborhood_nodes.append(source_node)
    # neighborhood_nodes.append(record_node)
    return list(np.unique(np.array(neighborhood_nodes)))


# clustering functions
def get_cluster_node_reference(cn, ref_list, cluster_index_list):
    good_ref = None
    for k in range(0, len(cluster_index_list)):
        index_val = cluster_index_list[k]
        if index_val == cn:
            good_ref = ref_list[index_val][2].split()
    return good_ref


def form_cluster(cluster_nodes, ref_list, cluster_index_list):
    cluster_list = []
    for cn in cluster_nodes:
        ref = get_cluster_node_reference(cn, ref_list, cluster_index_list)
        cluster_list.append(ref)
    return cluster_list


def get_node_membership(node, nodes):
    return nodes[node]


def set_node_membership(node, nodes, membership):
    nodes[node] = membership


def get_community_members(community_id, nodes):
    nodes_in_community = []
    for n, c in nodes.items():
        if c == community_id:
            nodes_in_community.append(n)
    return nodes_in_community


# graph weights
def find_edge_weight(node1, node2, edges):
    returned_weight = 0
    for e in edges:
        source_node = e[0]
        target_node = e[1]
        weight = e[2]
        if (source_node == node1 or source_node == node2) and (target_node == node1 or target_node == node2):
            returned_weight = weight
    return returned_weight


def get_node_with_highest_weight(node, neighborhood, edges):
    weights = {}
    for n in neighborhood:
        current_weight = find_edge_weight(node, n, edges)
        weights[n] = current_weight
    sorted_weights = dict(sorted(weights.items(), key=lambda item: item[1]))
    return list(sorted_weights.keys())[0], list(sorted_weights.values())[0]


def get_sum_of_weights_of_community(community_id, nodes, edges):
    sum_of_weights = 0
    for n1, c1 in nodes:
        if c1 == community_id:
            for n2, c2 in nodes:
                if c2 == community_id:
                    if n1 != n2:
                        edge_weight = find_edge_weight(n1, n2, edges)
                        if edge_weight != 0:
                            sum_of_weights = sum_of_weights + edge_weight
    return sum_of_weights


def get_sum_of_weights_inside_community(community_id, nodes, edges):
    sum_of_weights = 0
    for n1, c1 in nodes.items():
        if c1 == community_id:
            for n2, c2 in nodes.items():
                if c2 == community_id:
                    if n1 != n2:
                        edge_weight = find_edge_weight(n1, n2, edges)
                        if edge_weight != 0:
                            sum_of_weights = sum_of_weights + edge_weight
    return sum_of_weights


# Assuming that edge weights of zero means that an edge does not exist in the first place
def get_edge_weight(node_1, node_2, edges):
    w = 0.0
    for e in edges:
        if ((node_1 == e[0]) and (node_2 == e[1])) or ((node_1 == e[1]) and (node_2 == e[0])):
            w = e[2]
    return w


def get_edges_in_community(community_id, nodes, edges):
    # identify nodes in community
    nodes_in_community = []
    for n in nodes:
        if community_id == nodes[n]:
            nodes_in_community.append(n)
    # identify edges where nodes of the community are involved in
    all_involved_edges = []
    for n in nodes_in_community:
        involved_edges = find_involved_edges(n, edges)
        all_involved_edges = all_involved_edges + involved_edges
    res = list(set([ele for ele in all_involved_edges if all_involved_edges.count(ele) > 1]))
    for element in res:
        all_involved_edges.remove(element)
    unique_list = all_involved_edges + res
    return unique_list


def get_sum_of_incident_nodes_to_community(community_id, nodes, edges):
    unique_list = get_edges_in_community(community_id, nodes, edges)
    sum_of_weights = 0
    for e_r in unique_list:
        sum_of_weights = sum_of_weights + float(e_r[2])
    return sum_of_weights


def get_sum_of_weights_between_node_and_community(node, j_membership, nodes, edges):
    unique_list = get_edges_in_community(j_membership, nodes, edges)
    sum_of_weights = 0
    for e_r in unique_list:
        if (e_r[0] == node) or (e_r[1] == node):
            sum_of_weights = sum_of_weights + e_r[2]
    return sum_of_weights


def sum_of_neighborhood_weights(node, neighborhood, edges):
    s = 0
    for j in neighborhood:
        s = s + get_edge_weight(node, j, edges)
    return s


def sum_of_neighborhood_weights_general(record_node, edges):
    sum_of_weights = 0
    for edge in edges:
        source_node = edge[0]
        target_node = edge[1]
        edge_weight = edge[2]
        if (record_node == source_node) or (record_node == target_node):
            sum_of_weights = sum_of_weights + edge_weight
    return sum_of_weights


# special modularity functions
def compute_m(nodes, edges):
    s = 0
    for i in nodes.keys():
        for j in nodes.keys():
            a_i_j = get_edge_weight(i, j, edges)
            if i != j and a_i_j != 0:
                s = s + a_i_j
    m = 0.5 * s
    return m


def compute_m_networkx(g):
    s = 0
    for i in g.nodes:
        for j in g.nodes:
            a_i_j = g[i][j]["weight"]
            if i != j and a_i_j != 0:
                s = s + a_i_j
    m = 0.5 * s
    return m


def compute_modularity_networkx(g):
    m = compute_m(g.nodes, g.edges)
    res = 0
    for com in set(g.nodes.values()):
        members = get_community_members(com, g.nodes)
        for i in members:
            for j in members:
                a_i_j = get_edge_weight(i, j, g.edges)
                k_i = sum_of_neighborhood_weights(i, get_neighborhood(i, g.edges), g.edges)
                k_j = sum_of_neighborhood_weights(j, get_neighborhood(j, g.edges), g.edges)
                res = res + (a_i_j - ((k_i * k_j) / (2 * m)))
    modularity = res / (2 * m)
    return modularity


def compute_network_modularity(nodes, edges):
    m = compute_m(nodes, edges)
    res = 0
    for com in set(nodes.values()):
        members = get_community_members(com, nodes)
        for i in members:
            for j in members:
                if i != j:
                    a_i_j = get_edge_weight(i, j, edges)
                    k_i = sum_of_neighborhood_weights(i, get_neighborhood(i, edges), edges)
                    k_j = sum_of_neighborhood_weights(j, get_neighborhood(j, edges), edges)
                    res = res + (a_i_j - ((k_i * k_j) / (2 * m)))
    modularity = res / (2 * m)
    return modularity

def compute_network_modularity_networkx(nodes, edges):
    g = nx.Graph()
    g.add_weighted_edges_from(edges)
    modularity = louvain.modularity(nodes, g)
    return modularity


def compute_delta_modularity(community, node, nodes, edges):
    sigma_in = get_sum_of_weights_inside_community(community, nodes, edges)
    sigma_total = get_sum_of_incident_nodes_to_community(community, nodes, edges)
    k_i_in = get_sum_of_weights_between_node_and_community(node, community, nodes, edges)
    m = compute_m(nodes, edges)
    k_i = sum_of_neighborhood_weights(node, get_neighborhood(node, edges), edges)
    delta_modularity = (((sigma_in + k_i_in) / (2 * m)) - ((sigma_total + k_i) / (2 * m)) ** 2) - (
            (sigma_in / (2 * m)) - ((sigma_total / (2 * m)) ** 2) - ((k_i / (2 * m)) ** 2))
    return delta_modularity


def reduce_graph_edges(edges):
    edge_triples = []
    edge_tuples = []
    for triple in edges:
        if triple[0] <= triple[1]:
            edge_triples.append((triple[0], triple[1], triple[2]))
            edge_tuples.append((triple[0], triple[1]))
        if triple[1] < triple[0]:
            edge_triples.append((triple[1], triple[0], triple[2]))
            edge_tuples.append((triple[1], triple[0]))
    unique_edge_triples = list(set(edge_triples))
    mutable_unique_edge_triples = []
    for t in unique_edge_triples:
        mutable_unique_edge_triples.append([str(t[0]), str(t[1]), float(t[2])])
    repeated_edge_tuples = list(set([ele for ele in edge_tuples if edge_tuples.count(ele) > 1]))
    # final_reduced_edges = []
    for repeated_edge in repeated_edge_tuples:
        sum_of_weights = 0
        for tr in edge_triples:
            if (repeated_edge[0] == tr[0]) and (repeated_edge[1] == tr[1]):
                sum_of_weights = sum_of_weights + tr[2]
        # final_reduced_edges.append([repeated_edge[0],repeated_edge[1],sum_of_weights])
        for ele in mutable_unique_edge_triples:
            if (repeated_edge[0] == ele[0]) and (repeated_edge[1] == ele[1]):
                ele[2] = sum_of_weights
    final_reduced_edges = []
    for ele in mutable_unique_edge_triples:
        final_reduced_edges.append((ele[0], ele[1], ele[2]))
    final_reduced_edges = list(set(final_reduced_edges))
    return final_reduced_edges


def phase_1(nodes, edges):
    # while True:
    #     stagnation = []
    for i in nodes.keys():
        # i = np.random.choice(np.array(list(nodes.keys())),size=1, replace=False)[0]
        i_com = get_node_membership(i, nodes)
        neighborhood = get_neighborhood(i, edges)
        candidate_memberships = {}
        for j in neighborhood:
            j_com = get_node_membership(j, nodes)
            delta_modularity = compute_delta_modularity(i_com, i, nodes, edges) + compute_delta_modularity(j_com, i,
                                                                                                           nodes, edges)
            candidate_memberships[get_node_membership(j, nodes)] = delta_modularity
            # sorted_delta_modularities = dict(sorted(candidate_memberships.items(), key=lambda item: item[1]))
            # largest_delta_modularity_value = list(sorted_delta_modularities.values())[-1]
        max_com = max(candidate_memberships, key=candidate_memberships.get)
        largest_delta_modularity_value = candidate_memberships[max_com]
        if largest_delta_modularity_value > 0:
            # i_membership = list(sorted_delta_modularities.keys())[-1]
            set_node_membership(i, nodes, max_com)
        if largest_delta_modularity_value < 0:
            continue
        if largest_delta_modularity_value == 0:
            set_node_membership(i, nodes, i_com)
    #     if largest_delta_modularity_value <= 0:
    #         stagnation.append(1)
    # if len(stagnation) > 1:
    #     break
    return nodes, edges


def phase_2(nodes, edges, dendogram):
    # collapse nodes
    flipped = {}
    for key, value in nodes.items():
        if value not in flipped:
            flipped[value] = [key]
        else:
            flipped[value].append(key)
    dendogram.append(flipped)
    # rebuild nodes and give them new ids
    rebuilt_nodes = {}
    i = 0
    for k in flipped.keys():
        rebuilt_nodes[str(k)] = i
        i = i + 1
    # figure out new edges and weights
    rebuilt_edges = []
    for e in edges:
        sn = e[0]
        tn = e[1]
        w = e[2]
        for k, v in flipped.items():
            if sn in v:
                sn = k
            if tn in v:
                tn = k
        rebuilt_edges.append((str(sn), str(tn), float(w)))
    # reduce rebuilt edges
    rebuilt_edges = reduce_graph_edges(rebuilt_edges)
    return rebuilt_nodes, rebuilt_edges


def run(nodes, edges):
    initial_global_modularity = compute_network_modularity(nodes, edges)
    break_counter = 0
    dendogram = []
    initial_edges = copy.deepcopy(edges)
    initial_nodes = copy.deepcopy(nodes)
    # for _ in range(2):
    while True:
        print("New pass:")
        # Phase 1
        # Place i in each of the partitions and calculate delta modularity
        nodes, edges = phase_1(nodes, edges)
        print("Phase 1 complete:")
        # print("Phase 1 complete:")
        # print("Nodes:")
        # print("-----")
        # print(nodes)
        # print("-----")
        # print("Edges:")
        # print("-----")
        # print(edges)
        # print("-----")
        # print("Phase 1 modularity: " + str(compute_network_modularity(nodes, edges)))
        # print("-----")
        # Phase 2
        # Convert each community to a node. Rebuild edges. Reassign node community memberships.
        nodes, edges = phase_2(nodes, edges, dendogram)

        print("Phase 2 complete:")
        print("-----")
        print("Nodes:")
        print("-----")
        print(nodes)
        print("-----")
        print("Edges:")
        print("-----")
        print(edges)
        print("-----")
        print("Dendogram:")
        print(dendogram)

        # print("-----")
        # print("Phase 2 modularity: " + str(compute_network_modularity(nodes, edges)))
        # print("-----")
        # Consolidate clusters

        # current_nodes = consolidate_nodes(nodes, dendogram)
        # current_edges = initial_edges
        #
        # current_global_modularity = compute_network_modularity(current_nodes, current_edges)
        # global_delta_modularity = current_global_modularity - initial_global_modularity
        # initial_global_modularity = current_global_modularity
        # if global_delta_modularity == 0:
        #     break_counter = break_counter + 1
        # if break_counter > 1:
        #     break

    edges = initial_edges
    nodes = initial_nodes
    return nodes, edges


def optimize_modularity(nodes, edges):
    nodes_copy = copy.deepcopy(nodes)
    edges_copy = copy.deepcopy(edges)
    global_init_mod = compute_network_modularity(nodes_copy, edges_copy)
    while True:
        nodes, edges = phase_1(nodes_copy, edges_copy)
        global_final_mod = compute_network_modularity(nodes_copy, edges_copy)
        global_delta_modularity = global_final_mod - global_init_mod
        global_init_mod = global_final_mod
        if global_delta_modularity == 0:
            break
    return nodes_copy


def optimize_modularity_networkx(nodes, edges):
    nodes_copy = copy.deepcopy(nodes)
    edges_copy = copy.deepcopy(edges)
    g = nx.Graph()
    g.add_weighted_edges_from(edges)
    global_init_mod = compute_network_modularity(nodes_copy, edges_copy)
    while True:
        nodes, edges = phase_1(nodes_copy, edges_copy)
        global_final_mod = compute_network_modularity(nodes_copy, edges_copy)
        global_delta_modularity = global_final_mod - global_init_mod
        global_init_mod = global_final_mod
        if global_delta_modularity == 0:
            break
    return nodes_copy


# TESTS
def modularity_graph_clustering():
    nodes = {'A824917': 0, 'A830349': 1, 'A875214': 2, 'A956296': 3, 'A956423': 4, 'A985464': 5}
    edges_tuples_2 = [
        ('A956423', 'A985464', 1.0),
        ('A956296', 'A985464', 0.925),
        ('A956296', 'A956423', 0.9423076923076923),
        ('A830349', 'A985464', 1.0),
        ('A830349', 'A956423', 0.9494949494949495),
        ('A830349', 'A956296', 0.8813131313131314),
        ('A830349', 'A875214', 0.7835497835497837),
        ('A875214', 'A985464', 0.8285714285714286),
        ('A875214', 'A956423', 0.6758241758241759),
        ('A824917', 'A985464', 0.8285714285714286),
        ('A824917', 'A956423', 0.6758241758241759),
        ('A824917', 'A830349', 0.7835497835497837),
        ('A824917', 'A875214', 0.989010989010989)
    ]
    edges = copy.deepcopy(edges_tuples_2)
    initial_my_modularity = compute_network_modularity(nodes, edges)
    # initial_my_modularity = compute_netowrk_modularity_networkx(g)
    print("Initial Clusters: " + str(nodes))
    print("Initial Modularity: " + str(round(initial_my_modularity, 3)))
    final_clusters = optimize_modularity(nodes, edges)
    # final_clusters = nodes
    final_my_modularity = compute_network_modularity(final_clusters, edges)
    # final_my_modularity = compute_netowrk_modularity_networkx(final_clusters, edges)
    print("Final Clusters: " + str(final_clusters))
    print("Final Modularity: " + str(round(final_my_modularity, 3)))


def louvain_networkx():
    nodes = {'A824917': 0, 'A830349': 1, 'A875214': 2, 'A956296': 3, 'A956423': 4, 'A985464': 5}
    edges_tuples_2 = [
        ('A956423', 'A985464', 1.0),
        ('A956296', 'A985464', 0.925),
        ('A956296', 'A956423', 0.9423076923076923),
        ('A830349', 'A985464', 1.0),
        ('A830349', 'A956423', 0.9494949494949495),
        ('A830349', 'A956296', 0.8813131313131314),
        ('A830349', 'A875214', 0.7835497835497837),
        ('A875214', 'A985464', 0.8285714285714286),
        ('A875214', 'A956423', 0.6758241758241759),
        ('A824917', 'A985464', 0.8285714285714286),
        ('A824917', 'A956423', 0.6758241758241759),
        ('A824917', 'A830349', 0.7835497835497837),
        ('A824917', 'A875214', 0.989010989010989)
    ]
    edges = copy.deepcopy(edges_tuples_2)
    g = nx.Graph()
    g.add_weighted_edges_from(edges)
    initial_my_modularity = compute_network_modularity(nodes, edges)
    print("Initial Clusters: " + str(nodes))
    print("Initial Modularity: " + str(round(initial_my_modularity, 3)))
    partition_networkx = louvain.best_partition(g, partition=nodes)
    final_my_modularity = compute_network_modularity(partition_networkx, edges)
    print("Final Clusters: " + str(partition_networkx))
    print("Final Modularity: " + str(round(final_my_modularity, 3)))


def louvain_akef():
    nodes = {'A824917': 0, 'A830349': 1, 'A875214': 2, 'A956296': 3, 'A956423': 4, 'A985464': 5}
    edges_1 = [('A956423', 'A985464', {'weight': 1.0}), ('A956296', 'A985464', {'weight': 0.925}),
               ('A956296', 'A956423', {'weight': 0.9423076923076923}),
               ('A830349', 'A985464', {'weight': 1.0}), ('A830349', 'A956423', {'weight': 0.9494949494949495}),
               ('A830349', 'A956296', {'weight': 0.8813131313131314}),
               ('A830349', 'A875214', {'weight': 0.7835497835497837}),
               ('A875214', 'A985464', {'weight': 0.8285714285714286}),
               ('A875214', 'A956423', {'weight': 0.6758241758241759}),
               ('A875214', 'A956296', {'weight': 0.6648351648351648}),
               ('A824917', 'A985464', {'weight': 0.8285714285714286}),
               ('A824917', 'A956423', {'weight': 0.6758241758241759}),
               ('A824917', 'A956296', {'weight': 0.6666666666666666}),
               ('A824917', 'A830349', {'weight': 0.7835497835497837}),
               ('A824917', 'A875214', {'weight': 0.989010989010989})]
    edges_2 = [('A956423', 'A985464', {'weight': 1.0}), ('A956296', 'A985464', {'weight': 0.925}),
               ('A956296', 'A956423', {'weight': 0.9423076923076923}),
               ('A830349', 'A985464', {'weight': 1.0}), ('A830349', 'A956423', {'weight': 0.9494949494949495}),
               ('A830349', 'A956296', {'weight': 0.8813131313131314}),
               ('A830349', 'A875214', {'weight': 0.7835497835497837}),
               ('A875214', 'A985464', {'weight': 0.8285714285714286}),
               ('A824917', 'A985464', {'weight': 0.8285714285714286}),
               ('A824917', 'A830349', {'weight': 0.7835497835497837}),
               ('A824917', 'A875214', {'weight': 0.989010989010989})]
    edges_3 = [('A956423', 'A985464', {'weight': 1.0}), ('A956296', 'A985464', {'weight': 0.925}),
               ('A956296', 'A956423', {'weight': 0.9423076923076923}),
               ('A830349', 'A985464', {'weight': 1.0}), ('A830349', 'A956423', {'weight': 0.9494949494949495}),
               ('A830349', 'A956296', {'weight': 0.8813131313131314}),
               ('A830349', 'A875214', {'weight': 0.7835497835497837}),
               ('A875214', 'A985464', {'weight': 0.8285714285714286}),
               ('A875214', 'A956423', {'weight': 0.6758241758241759}),
               ('A824917', 'A985464', {'weight': 0.8285714285714286}),
               ('A824917', 'A956423', {'weight': 0.6758241758241759}),
               ('A824917', 'A830349', {'weight': 0.7835497835497837}),
               ('A824917', 'A875214', {'weight': 0.989010989010989})]
    edges_tuples = [('A956423', 'A985464', 1.0),
                    ('A956296', 'A985464', 0.925),
                    ('A956296', 'A956423', 0.9423076923076923),
                    ('A830349', 'A985464', 1.0),
                    ('A830349', 'A956423', 0.9494949494949495),
                    ('A830349', 'A956296', 0.8813131313131314),
                    ('A830349', 'A875214', 0.7835497835497837),
                    ('A875214', 'A985464', 0.8285714285714286),
                    ('A875214', 'A956423', 0.6758241758241759),
                    ('A875214', 'A956296', 0.6648351648351648),
                    ('A824917', 'A985464', 0.8285714285714286),
                    ('A824917', 'A956423', 0.6758241758241759),
                    ('A824917', 'A956296', 0.6666666666666666),
                    ('A824917', 'A830349', 0.7835497835497837),
                    ('A824917', 'A875214', 0.989010989010989)]
    edges_tuples_2 = [
        ('A956423', 'A985464', 1.0),
        ('A956296', 'A985464', 0.925),
        ('A956296', 'A956423', 0.9423076923076923),
        ('A830349', 'A985464', 1.0),
        ('A830349', 'A956423', 0.9494949494949495),
        ('A830349', 'A956296', 0.8813131313131314),
        ('A830349', 'A875214', 0.7835497835497837),
        ('A875214', 'A985464', 0.8285714285714286),
        ('A875214', 'A956423', 0.6758241758241759),
        ('A824917', 'A985464', 0.8285714285714286),
        ('A824917', 'A956423', 0.6758241758241759),
        ('A824917', 'A830349', 0.7835497835497837),
        ('A824917', 'A875214', 0.989010989010989)
    ]
    edges_tuples_3 = [
        ('A956423', 'A985464', 1.0),
        ('A956296', 'A985464', 0.925),
        ('A956296', 'A956423', 0.9423076923076923),
        ('A830349', 'A985464', 1.0),
        ('A830349', 'A956423', 0.9494949494949495),
        ('A830349', 'A956296', 0.8813131313131314),
        ('A830349', 'A875214', 0.7835497835497837),
        ('A875214', 'A985464', 0.8285714285714286),
        ('A824917', 'A985464', 0.8285714285714286),
        ('A824917', 'A830349', 0.7835497835497837),
        ('A824917', 'A875214', 0.989010989010989)
    ]
    # {'cluster_id': 'A824917', 'quality': 0.8161164071642083, 'ref_id': 'A985464', 'reference': 'LLOYD AARON DEAN 2475 SPICEWOOD DR WINSTON SALEM NC 27106'}
    # {'cluster_id': 'A824917', 'quality': 0.8161164071642083, 'ref_id': 'A956423', 'reference': 'LLOYD AARON DEAN 2475 SPICEWOOD DR WINSTON SALEM NC 27106 456 18 2098'}
    # {'cluster_id': 'A824917', 'quality': 0.8161164071642083, 'ref_id': 'A956296', 'reference': 'LLOYD AARON D 2475 SPICEWOOD DR WINSTON SALEM NC 27106 456 18 2098'}
    # {'cluster_id': 'A824917', 'quality': 0.8161164071642083, 'ref_id': 'A830349', 'reference': 'LLOYD AARON DEAN 2475 SPICEWOOD DR WINSTON SALEM NC 27106 456182098'}
    # {'cluster_id': 'A824917', 'quality': 0.8161164071642083, 'ref_id': 'A875214', 'reference': 'ANDREEW AARON STEPHEN 2475 SPICEWOOD DR WINSTON SALEM NC 27106 601 70 6106'}
    # {'cluster_id': 'A824917', 'quality': 0.8161164071642083, 'ref_id': 'A824917', 'reference': 'ANDREW AARON STEPHEN 2475 SPICEWOOD DR WINSTON SALEM NC 27106 601 70 6106'}
    edges = copy.deepcopy(edges_tuples_2)
    g = nx.Graph()
    g.add_weighted_edges_from(edges)
    initial_networkx_modularity = louvain.modularity(nodes, g)
    print("----")
    initial_my_modularity = compute_network_modularity(nodes, edges)
    print("################################")
    print("Initial Clusters")
    print(nodes)
    print("Initial Modularity NetworkX: " + str(round(initial_networkx_modularity, 3)))
    print("Initial Modularity Mine: " + str(round(initial_my_modularity, 3)))
    nodes, edges = run(nodes, edges)
    g = nx.Graph()
    g.add_weighted_edges_from(edges)
    final_networkx_modularity = louvain.modularity(nodes, g)
    print("----")
    final_my_modularity = compute_network_modularity(nodes, edges)
    print("################################")
    print("Final Clusters")
    print(nodes)
    print("Final Modularity NetworkX: " + str(round(final_networkx_modularity, 3)))
    print("Final Modularity Mine: " + str(round(final_my_modularity, 3)))
    print("################################")


def check_my_modularity():
    nodes = {'A824917': 0, 'A830349': 1, 'A875214': 2, 'A956296': 3, 'A956423': 4, 'A985464': 5}
    edges_tuples_2 = [
        ('A956423', 'A985464', 1.0),
        ('A956296', 'A985464', 0.925),
        ('A956296', 'A956423', 0.9423076923076923),
        ('A830349', 'A985464', 1.0),
        ('A830349', 'A956423', 0.9494949494949495),
        ('A830349', 'A956296', 0.8813131313131314),
        ('A830349', 'A875214', 0.7835497835497837),
        ('A875214', 'A985464', 0.8285714285714286),
        ('A875214', 'A956423', 0.6758241758241759),
        ('A824917', 'A985464', 0.8285714285714286),
        ('A824917', 'A956423', 0.6758241758241759),
        ('A824917', 'A830349', 0.7835497835497837),
        ('A824917', 'A875214', 0.989010989010989)
    ]
    edges = copy.deepcopy(edges_tuples_2)
    g = nx.Graph()
    g.add_weighted_edges_from(edges)
    initial_my_modularity = compute_modularity_networkx(g)


def check_networkx_modularity():
    nodes = {'A824917': 0, 'A830349': 1, 'A875214': 2, 'A956296': 3, 'A956423': 4, 'A985464': 5}
    edges_tuples_2 = [
        ('A956423', 'A985464', 1.0),
        ('A956296', 'A985464', 0.925),
        ('A956296', 'A956423', 0.9423076923076923),
        ('A830349', 'A985464', 1.0),
        ('A830349', 'A956423', 0.9494949494949495),
        ('A830349', 'A956296', 0.8813131313131314),
        ('A830349', 'A875214', 0.7835497835497837),
        ('A875214', 'A985464', 0.8285714285714286),
        ('A875214', 'A956423', 0.6758241758241759),
        ('A824917', 'A985464', 0.8285714285714286),
        ('A824917', 'A956423', 0.6758241758241759),
        ('A824917', 'A830349', 0.7835497835497837),
        ('A824917', 'A875214', 0.989010989010989)
    ]
    edges = copy.deepcopy(edges_tuples_2)
    g = nx.Graph()
    g.add_weighted_edges_from(edges)
    initial_networkx_modularity = louvain.modularity(nodes, g)


def measure_execution_time(func):
    def wrapper():
        start_time = time.perf_counter()
        func()
        end_time = time.perf_counter()
        print(f"Execution time: {end_time - start_time} seconds")

    return wrapper


@measure_execution_time
def main_louvain():
    print("Modularity Clustering NetowrkX")
    # louvain_networkx()
    check_networkx_modularity()


@measure_execution_time
def main_akef():
    print("Modularity Clustering Akef")
    modularity_graph_clustering()
    check_my_modularity()


if __name__ == '__main__':
    main_louvain()
    print("----------------------------------------------------------")
    main_akef()
