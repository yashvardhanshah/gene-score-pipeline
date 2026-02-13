import pandas as pd
import networkx as nx

EDGE_FILE = "results/string_network.edgelist"
SEED_FILE = "results/seed_genes_cancer.tsv"
OUTPUT_FILE = "results/gene_propagation_scores.tsv"

def main():
    print("Loading STRING network...")
    G = nx.read_weighted_edgelist(EDGE_FILE)

    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")

    seeds = pd.read_csv(SEED_FILE, sep="\t")
    seed_genes = set(seeds["Gene"])

    print("Running Random Walk with Restart...")

    scores = {}
    for node in G.nodes():
        scores[node] = 1.0 if node in seed_genes else 0.0

    for _ in range(3):
        new_scores = {}
        for node in G.nodes():
            neighbor_sum = sum(scores[n] for n in G.neighbors(node))
            new_scores[node] = 0.7 * scores[node] + 0.3 * neighbor_sum
        scores = new_scores

    df = pd.DataFrame(scores.items(), columns=["Gene", "Score"])
    df.to_csv(OUTPUT_FILE, sep="\t", index=False)

    print(f"Propagation scores saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
