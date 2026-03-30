library(ggplot2)
library(dplyr)

# ── 1. Load annotated variants ────────────────────────────────────
df <- read.csv("annotated_variants.csv")

# Clean up: simplify long ClinVar labels
df$ClinVar_Significance <- case_when(
  grepl("athogenic", df$ClinVar_Significance) ~ "Pathogenic",
  grepl("enign",     df$ClinVar_Significance) ~ "Benign",
  grepl("ncertain",  df$ClinVar_Significance) ~ "Uncertain",
  TRUE                                         ~ "Not in ClinVar"
)

cat("Total variants:", nrow(df), "\n")
print(table(df$ClinVar_Significance))

# ── 2. Plot 1: ClinVar Significance Bar Chart ─────────────────────
ggplot(df, aes(x = ClinVar_Significance, fill = ClinVar_Significance)) +
  geom_bar() +
  scale_fill_manual(values = c(
    "Pathogenic"     = "#e74c3c",   # red
    "Benign"         = "#2ecc71",   # green
    "Uncertain"      = "#f39c12",   # orange
    "Not in ClinVar" = "#95a5a6"    # grey
  )) +
  labs(
    title = "Variant Classification by ClinVar Significance",
    x     = "Clinical Significance",
    y     = "Number of Variants"
  ) +
  theme_minimal() +
  theme(legend.position = "none")

ggsave("clinvar_barplot.png", width = 7, height = 5)
cat("✅ Saved clinvar_barplot.png\n")

# ── 3. Plot 2: Read Depth by Clinical Significance ────────────────
ggplot(df, aes(x = ClinVar_Significance, y = DP, fill = ClinVar_Significance)) +
  geom_boxplot(alpha = 0.7) +
  scale_fill_manual(values = c(
    "Pathogenic"     = "#e74c3c",
    "Benign"         = "#2ecc71",
    "Uncertain"      = "#f39c12",
    "Not in ClinVar" = "#95a5a6"
  )) +
  labs(
    title = "Read Depth Distribution by Clinical Significance",
    x     = "Clinical Significance",
    y     = "Read Depth (DP)"
  ) +
  theme_minimal() +
  theme(legend.position = "none")

ggsave("depth_by_significance.png", width = 7, height = 5)
cat("✅ Saved depth_by_significance.png\n")

# ── 4. Plot 3: Chromosome Distribution of Pathogenic Variants ─────
pathogenic <- df[df$ClinVar_Significance == "Pathogenic", ]

if (nrow(pathogenic) > 0) {
  ggplot(pathogenic, aes(x = factor(CHROM))) +
    geom_bar(fill = "#e74c3c") +
    labs(
      title = "Pathogenic Variants per Chromosome",
      x     = "Chromosome",
      y     = "Count"
    ) +
    theme_minimal()
  
  ggsave("pathogenic_by_chrom.png", width = 8, height = 5)
  cat("✅ Saved pathogenic_by_chrom.png\n")
} else {
  cat("⚠️  No pathogenic variants found for chromosome plot\n")
}

cat("\n🎉 All plots saved successfully!\n")