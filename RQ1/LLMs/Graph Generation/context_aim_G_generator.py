import json
import os
import networkx as nx
import random


def generate_directed_er_graph():
    while True:
        G = nx.DiGraph()
        nodes = list(range(5))
        G.add_nodes_from(nodes)

        # Save all edges as quadruples (u, v, c, w)
        edge_tuples = []
        for i in range(5):
            for j in range(5):
                if i != j and random.random() < 0.3:  # 30% probability to add an edge
                    w1 = random.randint(1, 4)  # Scenario c=1 corresponds to weight w1
                    w2 = random.randint(5, 9)  # Scenario c=2 corresponds to weight w2

                    G.add_edge(i, j)
                    # Each edge is stored as two quadruples, containing weights for two scenarios
                    edge_tuples.append((i, j, 1, w1))  # Scenario c=1, weight w1
                    edge_tuples.append((i, j, 2, w2))  # Scenario c=2, weight w2

        # Randomly select two nodes
        special_nodes = random.sample(nodes, 2)
        src, dst = special_nodes

        # Check if there is only one unique path and it is directly connected
        if G.has_edge(src, dst):
            # Get all simple paths from src to dst
            all_paths = list(nx.all_simple_paths(G, src, dst))

            # If there is only one path and it is a direct connection
            if len(all_paths) == 1 and len(all_paths[0]) == 2:
                # Get the weight w corresponding to c=2
                w_c1 = None
                for edge in edge_tuples:
                    if edge[0] == src and edge[1] == dst and edge[2] == 2:  # Scenario c=2
                        w_c1 = edge[3]
                        break

                print(f"Special node pair: ({src}, {dst}), c=2, w={w_c1}")

                return edge_tuples, special_nodes, w_c1


def save_graph_to_json(edge_tuples, special_nodes, w, filename):
    os.makedirs("save_graphs", exist_ok=True)  # Create save folder
    filepath = os.path.join("save_graphs", filename)  # Build the file path

    # Convert tuples to list format so that it can be stored in standard JSON format
    graph_data = {
        "edges": edge_tuples,  # Directly use tuples as array elements
        "special_nodes": special_nodes,
        "c": 2,
        "w": w
    }

    with open(filepath, "w") as f:
        json.dump(graph_data, f, indent=4)


# Loop to generate multiple graphs and save them
for i in range(100):
    G, special_nodes, w = generate_directed_er_graph()
    save_graph_to_json(G, special_nodes, w, f"graph_{i}.json")
    print(f"Graph {i} saved in 'save_graphs/' with special nodes {special_nodes}")
