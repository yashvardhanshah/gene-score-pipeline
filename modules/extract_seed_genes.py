import pandas as pd
import os

# Input file path
INPUT_FILE = "data_manifests/Census_allFri Feb 13 15_21_14 2026.csv"

# Output file path
OUTPUT_FILE = "results/seed_genes_cancer.tsv"

def main():
    # Read the CGC dataset
    df = pd.read_csv(INPUT_FILE)

    # Check column names
    print("Columns in dataset:")
    print(df.columns)

    # Extract gene symbols
    # In CGC, the column is usually named 'Gene Symbol'
    if "Gene Symbol" in df.columns:
        genes = df["Gene Symbol"]
    elif "Gene Symbol " in df.columns:
        genes = df["Gene Symbol "]
    else:
        raise ValueError("Gene Symbol column not found.")

    # Clean and remove duplicates
    genes = genes.dropna().astype(str).str.strip().unique()

    # Convert to DataFrame
    gene_df = pd.DataFrame({"Gene": genes})

    # Ensure results folder exists
    os.makedirs("results", exist_ok=True)

    # Save to file
    gene_df.to_csv(OUTPUT_FILE, sep="\t", index=False)

    print(f"Seed genes saved to: {OUTPUT_FILE}")
    print(f"Total genes: {len(gene_df)}")

if __name__ == "__main__":
    main()
