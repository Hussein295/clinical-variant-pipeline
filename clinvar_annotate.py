import pandas as pd
import requests
import time

# ── 1. Load filtered variants ─────────────────────────────────────
df = pd.read_csv("filtered_variants.csv")

# Keep only rows that have a real rsID (skip rows where ID is ".")
df_with_ids = df[df["ID"] != "."].head(250).copy()
print(f"Variants with rsID: {len(df_with_ids)} out of {len(df)}")

# ── 2. Function to query ClinVar ──────────────────────────────────
def query_clinvar(rsid):
    """Query ClinVar for a given rsID and return clinical significance."""
    try:
        # Step 1: Search ClinVar for the rsID
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        search_params = {
            "db": "clinvar",
            "term": rsid,
            "retmode": "json"
        }
        search_resp = requests.get(search_url, params=search_params, timeout=10)
        search_data = search_resp.json()

        ids = search_data["esearchresult"]["idlist"]

        # If no results found
        if not ids:
            return "Not in ClinVar"

        # Step 2: Fetch the details using the first ID
        summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        summary_params = {
            "db": "clinvar",
            "id": ids[0],
            "retmode": "json"
        }
        summary_resp = requests.get(summary_url, params=summary_params, timeout=10)
        summary_data = summary_resp.json()

        # Extract clinical significance
        result = summary_data["result"][ids[0]]
        clnsig = result.get("clinical_significance", {}).get("description", "Unknown")
        return clnsig

    except Exception as e:
        return f"Error: {str(e)}"

# ── 3. Annotate each variant ──────────────────────────────────────
print("\nQuerying ClinVar... (this may take a minute)\n")

clinvar_results = []

for i, row in df_with_ids.iterrows():
    rsid = row["ID"]
    significance = query_clinvar(rsid)
    clinvar_results.append(significance)
    print(f"  {rsid} → {significance}")

    # Be polite to the API - wait 0.4s between requests
    time.sleep(0.4)

# ── 4. Add results as a new column ───────────────────────────────
df_with_ids["ClinVar_Significance"] = clinvar_results

# ── 5. Save annotated CSV ─────────────────────────────────────────
df_with_ids.to_csv("annotated_variants.csv", index=False)
print("\n✅ Saved annotated_variants.csv")

# ── 6. Summary ────────────────────────────────────────────────────
print("\n── ClinVar Significance Summary ──")
print(df_with_ids["ClinVar_Significance"].value_counts())
     