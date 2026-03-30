# Clinical Variant Analysis Pipeline

A bioinformatics pipeline that parses, filters, and annotates 
genetic variants from VCF files using ClinVar.

## Pipeline Steps
1. **Parse** VCF files using Python + pandas
2. **Filter** variants by read depth (DP ≥ 100)
3. **Annotate** variants using the ClinVar API (NCBI E-utilities)
4. **Visualize** results using R + ggplot2
5. **Report** findings in an HTML R Markdown report

## Tools Used
- Python (pandas, requests)
- R (ggplot2, dplyr, rmarkdown)
- ClinVar / NCBI E-utilities API
- 1000 Genomes Project data

## Output
- Filtered variant CSV
- ClinVar annotated CSV
- Pathogenic variant list
- HTML clinical report with visualizations

## How to Run
```bash
python parse_vcf.py
python clinvar_annotate.py
python pathogenic_filter.py
```
Then in RStudio knit `clinical_report.Rmd`
