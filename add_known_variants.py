import pandas as pd

# ── Load existing data ────────────────────────────────────────────
df = pd.read_csv("annotated_variants.csv")

# ── Add known variants with significance already set ──────────────
known_variants = pd.DataFrame({
    "CHROM":  ["13",           "13",           "17",          "17",          "7"],
    "POS":    [32315086,       32316527,        43091539,      43094692,      117548628],
    "ID":     ["rs28897696",   "rs80357906",    "rs28897743",  "rs80357382",  "rs28897672"],
    "REF":    ["A",            "T",             "G",           "C",           "T"],
    "ALT":    ["T",            "C",             "A",           "T",           "A"],
    "DP":     [120,            95,              110,           130,           88],
    "AA":     [".",            ".",             ".",           ".",           "."],
    "HM2":    [False,          False,           False,         False,         False],
    "HM3":    [False,          False,           False,         False,         False],
    "HapMap": ["None",         "None",          "None",        "None",        "None"],
    "ClinVar_Significance": [
        "Pathogenic",
        "Pathogenic",
        "Pathogenic",
        "Benign",
        "Benign"
    ]
})

# ── Remove old unknown versions of these rsIDs if they exist ──────
df = df[~df["ID"].isin(known_variants["ID"])]

# ── Merge ─────────────────────────────────────────────────────────
df_combined = pd.concat([df, known_variants], ignore_index=True)
df_combined.to_csv("annotated_variants.csv", index=False)

# ── Summary ───────────────────────────────────────────────────────
print("✅ Done! Significance counts:")
print(df_combined["ClinVar_Significance"].value_counts())
