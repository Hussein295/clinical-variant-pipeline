import pandas as pd
import requests
import time

df = pd.read_csv("annotated_variants.csv")

# Only re-query the ones that are still Unknown
unknown = df[df["ClinVar_Significance"] == "Unknown"].copy()
print(f"Re-querying {len(unknown)} variants...\n")

def query_clinvar(rsid):
    try:
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        search_resp = requests.get(search_url, params={
            "db": "clinvar", "term": rsid, "retmode": "json"
        }, timeout=10)
        ids = search_resp.json()["esearchresult"]["idlist"]
        if not ids:
            return "Not in ClinVar"
        summary_resp = requests.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
            params={"db": "clinvar", "id": ids[0], "retmode": "json"},
            timeout=10
        )
        result = summary_resp.json()["result"][ids[0]]
        return result.get("clinical_significance", {}).get("description", "Unknown")
    except:
        return "Error"

for i, row in unknown.iterrows():
    sig = query_clinvar(row["ID"])
    df.at[i, "ClinVar_Significance"] = sig
    print(f"  {row['ID']} → {sig}")
    time.sleep(0.4)

df.to_csv("annotated_variants.csv", index=False)
print("\n✅ Re-annotation complete!")
print(df["ClinVar_Significance"].value_counts())
