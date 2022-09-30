from collections import defaultdict

from graph import DWM_ModularityGraphClustering


# config one does not rely on transitive closure and clusters the graph of pairs after applying mu as a threshold
def configuration1(logFile, refList, pairList, implementation):
    print('\n>>Starting DWM91 Modularity Graph Clustering\n')
    print('\n>>Starting DWM91 Modularity Graph Clustering\n', file=logFile)
    # 1- Find single records that were not clustered
    all_references = []
    all_clustered_references = []
    refList.sort(key=lambda x: x[1])
    for r in refList:
        all_references.append(r[1])
    for c1 in pairList:
        all_clustered_references.append(c1[1])
    single_records = [elem for elem in all_references if elem not in all_clustered_references]
    # 2- Initialize node clusters
    nodes = {}
    com = 0
    for c1 in refList:
        nodes[str(c1[1])] = com
        com = com + 1
    initial_my_modularity = DWM_ModularityGraphClustering.compute_network_modularity(nodes, pairList)
    # 3- Create graph and compute networkX louvain partitions
    node_clusters = {}
    if implementation == "louvain":
        # https://github.com/taynaud/python-louvain
        node_clusters = DWM_ModularityGraphClustering.networkx_modularity_graph_clustering(nodes, pairList)
    if implementation == "modularity_graph_clustering":
        # my implementation
        node_clusters = DWM_ModularityGraphClustering.akef_modularity_graph_clustering(nodes, pairList)
    # 4- Get the difference between the final clusters and the new clusters
    single_records = [elem for elem in all_references if elem not in list(node_clusters.keys())]
    for c2 in single_records:
        node_clusters[c2] = int(max(list(node_clusters.values())) + 1)
    final_my_modularity = DWM_ModularityGraphClustering.compute_network_modularity(node_clusters, pairList)
    # 5- Create link index from the result of the louvain method.
    # https://www.geeksforgeeks.org/python-grouping-dictionary-keys-by-value/
    grouped_by_partitions = defaultdict(list)
    for key, val in sorted(node_clusters.items()):
        grouped_by_partitions[val].append(key)
    grouped_by_partitions = dict(grouped_by_partitions)
    linkIndex = []
    for key, value in grouped_by_partitions.items():
        cluster_id = min(value)
        for r in value:
            linkIndex.append((cluster_id, r))
    linkIndex.sort()
    return linkIndex, round(final_my_modularity, 3), round(initial_my_modularity, 3)


def configuration2(logFile, clusterList, refList, compareCache, implementation):
    print('\n>>Starting DWM91 Modularity Graph Clustering\n')
    print('\n>>Starting DWM91 Modularity Graph Clustering\n', file=logFile)
    clusterDict = {}
    for tup in clusterList:
        clusterDict[tup[1]] = tup[0]
    grouped_by_cluster = defaultdict(list)
    for key, val in sorted(clusterDict.items()):
        grouped_by_cluster[val].append(key)
    grouped_by_cluster = dict(grouped_by_cluster)
    rearranged_compare_cache = []
    for p, sim in compareCache.items():
        ids = p.split(":")
        rearranged_compare_cache.append((ids[0], ids[1], sim))
    linkIndex = []
    cluster_modularities = {}
    for key2, val2 in grouped_by_cluster.items():
        # each value is a cluster
        # initialize edges
        edges = []
        val2.sort()
        for n1 in val2:
            for n2 in val2:
                if n1 != n2:
                    if n1 < n2:
                        key = str(str(n1) + ":" + str(n2))
                        if key in compareCache:
                            w = compareCache[key]
                            edges.append((n1, n2, w))
                    if n2 < n1:
                        key = str(str(n2) + ":" + str(n1))
                        if key in compareCache:
                            w = compareCache[key]
                            edges.append((n2, n1, w))
        # initialize nodes
        nodes = {}
        com = 0
        for n in val2:
            nodes[n] = com
            com = com + 1
        if len(edges) >= 1:
            if implementation == "louvain":
                # compute initial network modularity
                initial_my_modularity = DWM_ModularityGraphClustering.compute_network_modularity_networkx(nodes, edges)
                # create edges and compute networkX louvain partitions implementation of louvain based on Blondel et al., 1996 without any modifications
                # https://github.com/taynaud/python-louvain
                node_clusters = DWM_ModularityGraphClustering.networkx_modularity_graph_clustering(nodes, edges)
                single_records = [elem for elem in val2 if elem not in list(node_clusters.keys())]
                for c2 in single_records:
                    node_clusters[c2] = int(max(list(node_clusters.values())) + 1)
                final_my_modularity = DWM_ModularityGraphClustering.compute_network_modularity_networkx(node_clusters,
                                                                                                        edges)
                if final_my_modularity <= 0:
                    node_clusters = {}
                    for n3 in val2:
                        node_clusters[n3] = 0
                grouped_by_partitions = defaultdict(list)
                for key, val in sorted(node_clusters.items()):
                    grouped_by_partitions[val].append(key)
                grouped_by_partitions = dict(grouped_by_partitions)
                for key, value in grouped_by_partitions.items():
                    cluster_id = min(value)
                    for r in value:
                        linkIndex.append((cluster_id, r))
                cluster_modularities[str(key2)] = {"initial": round(initial_my_modularity, 3),
                                                   "final": round(final_my_modularity, 3)}
            if implementation == "modularity_graph_clustering":
                # compute initial network modularity
                initial_my_modularity = DWM_ModularityGraphClustering.compute_network_modularity(nodes, edges)
                # my implementation with some modifications to fit our problem of small networks
                node_clusters = DWM_ModularityGraphClustering.akef_modularity_graph_clustering(nodes, edges)
                single_records = [elem for elem in val2 if elem not in list(node_clusters.keys())]
                for c2 in single_records:
                    node_clusters[c2] = int(max(list(node_clusters.values())) + 1)
                final_my_modularity = DWM_ModularityGraphClustering.compute_network_modularity(node_clusters, edges)
                if final_my_modularity <= 0:
                    node_clusters = {}
                    for n3 in val2:
                        node_clusters[n3] = 0
                grouped_by_partitions = defaultdict(list)
                for key, val in sorted(node_clusters.items()):
                    grouped_by_partitions[val].append(key)
                grouped_by_partitions = dict(grouped_by_partitions)
                for key, value in grouped_by_partitions.items():
                    cluster_id = min(value)
                    for r in value:
                        linkIndex.append((cluster_id, r))
                cluster_modularities[str(key2)] = {"initial": round(initial_my_modularity, 3),
                                                   "final": round(final_my_modularity, 3)}
        else:
            for i, n in nodes.items():
                linkIndex.append((i, i))
    linkIndex.sort()
    return linkIndex, cluster_modularities
