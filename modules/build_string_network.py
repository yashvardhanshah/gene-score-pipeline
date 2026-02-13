import pandas as pd
import gzip
import os

INPUT_FILE = "data_manifests/9606.protein.links.detailed.v12.0.txt.gz"
OUTPUT_FILE = "results/string_network.edgelist"

CONFIDENCE_THRESHOLD = 700  # STRING uses 0–1000 scale


def main():
    print("Reading STRING network...")

    # Read compressed STRING file
    with gzip.open(INPUT_FILE, 'rt') as f:
        df = pd.read_csv(f, sep=" ")

    print("Total interactions:", len(df))

    # Filter by confidence
    df_filtered = df[df["combined_score"] >= CONFIDENCE_THRESHOLD]

    print("Interactions after filtering:", len(df_filtered))

    # Extract gene IDs
    edges = df_filtered[["protein1", "protein2", "combined_score"]]

    # Normalize score to 0–1
    edges["combined_score"] = edges["combined_score"] / 1000.0

    # Ensure results folder exists
    os.makedirs("results", exist_ok=True)

    # Save edgelist
    edges.to_csv(OUTPUT_FILE, sep="\t", index=False, header=False)

    print("STRING network saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
