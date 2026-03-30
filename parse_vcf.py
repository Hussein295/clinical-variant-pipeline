import pandas as pd

# ── 1. Load the VCF ──────────────────────────────────────────────
vcf_path = "CEU.trio.2010_03.sites.vcf"   # ← change this to your actual filename

rows = []

with open(vcf_path, "r") as f:
    for line in f:
        # Skip comment/metadata lines
        if line.startswith("##"):
            continue

        # This is the header line
        if line.startswith("#CHROM"):
            headers = line.strip().lstrip("#").split("\t")
            continue

        # Parse each variant line
        fields = line.strip().split("\t")
        row = dict(zip(headers, fields))

        # ── 2. Parse the INFO column ─────────────────────────────
        info = row["INFO"]
        info_dict = {}

        for item in info.split(";"):
            if "=" in item:
                key, value = item.split("=", 1)
                info_dict[key] = value
            else:
                # Flags like HM2, HM3 have no value
                info_dict[item] = True

        # Add parsed INFO fields as columns
        row["DP"]  = int(info_dict.get("DP", 0))
        row["AA"]  = info_dict.get("AA", ".")
        row["HM2"] = info_dict.get("HM2", False)
        row["HM3"] = info_dict.get("HM3", False)

        rows.append(row)

# ── 3. Build a DataFrame ─────────────────────────────────────────
df = pd.DataFrame(rows)
print("Total variants loaded:", len(df))
print(df[["CHROM", "POS", "ID", "REF", "ALT", "DP", "AA", "HM2", "HM3"]].head(10))

# ── 4. Filter: Keep only variants with DP >= 100 ─────────────────
df_filtered = df[df["DP"] >= 100]
print(f"\nVariants after DP filter (>= 100): {len(df_filtered)}")

# ── 5. Flag HapMap variants ───────────────────────────────────────
df_filtered = df_filtered.copy()
df_filtered["HapMap"] = df_filtered.apply(
    lambda r: "HM3" if r["HM3"] else ("HM2" if r["HM2"] else "None"), axis=1
)

# ── 6. Save to CSV ───────────────────────────────────────────────
df_filtered.to_csv("filtered_variants.csv", index=False)
print("\n✅ Saved filtered_variants.csv")
print(df_filtered[["CHROM", "POS", "ID", "REF", "ALT", "DP", "HapMap"]].head(10))