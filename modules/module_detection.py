import pandas as pd
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities

EDGE_FILE = "results/string_network.edgelist"
SCORE_FILE = "results/gene_propagation_scores.tsv"
OUTPUT_FILE = "results/gene_modules.tsv"

TOP_N = 1000

def main():
    scores = pd.read_csv(SCORE_FILE, sep="\t")
    top_genes = scores.sort_values("Score", ascending=False).head(TOP_N)["Gene"]

    print(f"Top genes selected: {len(top_genes)}")

    G = nx.read_weighted_edgelist(EDGE_FILE)
    subG = G.subgraph(top_genes)

    print(f"Subgraph nodes: {subG.number_of_nodes()}")
    print(f"Subgraph edges: {subG.number_of_edges()}")

    print("Detecting modules...")
    communities = list(greedy_modularity_communities(subG))

    rows = []
    for i, comm in enumerate(communities):
        for gene in comm:
            rows.append((gene, i))

    df = pd.DataFrame(rows, columns=["Gene", "Module"])
    df.to_csv(OUTPUT_FILE, sep="\t", index=False)

    print(f"Gene modules saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
