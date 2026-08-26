# Ireland Employment Permits 2025 — Data Analysis

An exploratory analysis of Ireland's 2025 employment permit statistics —
who's coming, where they're working, which sectors depend most on the
scheme, and how concentrated that reliance is among sponsoring employers.

Built entirely from four official statistical breakdowns published by
Ireland's **Department of Enterprise, Trade & Employment (DETE)**.

![Top nationalities](outputs/figures/top_nationalities.png)

## Key findings

- **India dominates**, accounting for **32%** of all permits issued in
  2025 — more than the next five nationalities combined.
- **Refusal rates cluster around the 10.0% national average** (roughly
  4–19%) across higher-volume nationalities; no nationality is a dramatic
  outlier once low-sample noise is filtered out.
- **Dublin absorbs 47% of all permits nationally**; Cork, Limerick, Meath
  and Kildare form a distant second tier.
- **Health & Social Work Activities is the single largest sector** at
  25.6% of all permits — well ahead of tech (Information & Communication)
  and Accommodation & Food Services.
- **Sponsorship is a long tail with a concentrated core**: no single
  company dominates (the top sponsor is ~1% of the total), but the busiest
  20% of ~8,300 sponsoring companies still account for 71% of permits,
  while 57% of companies sponsored exactly one permit all year.

Full write-up, methodology and all charts: **[`notebooks/employment_permits_2025_analysis.ipynb`](notebooks/employment_permits_2025_analysis.ipynb)**

## Project structure

```
.
├── data/
│   ├── raw/                     # original DETE workbooks, unmodified
│   └── processed/                # cleaned, tidy CSVs (output of clean_data.py)
├── notebooks/
│   └── employment_permits_2025_analysis.ipynb
├── outputs/
│   └── figures/                  # chart PNGs exported from the notebook
├── src/
│   ├── clean_data.py              # raw .xlsx -> tidy CSVs
│   ├── build_notebook.py          # notebook-assembly helper
│   ├── build_cells.py             # actual analysis/chart code (notebook content)
│   └── run_build.py               # entry point: rebuilds the .ipynb
├── requirements.txt
└── README.md
```

## Reproducing this

```bash
git clone <this-repo>
cd ie-employment-permits-2025
pip install -r requirements.txt

# raw .xlsx -> tidy CSVs in data/processed/
python src/clean_data.py

# open and run notebooks/employment_permits_2025_analysis.ipynb, or
# regenerate the ipynb headlessly (bakes fresh chart outputs into the file)
python src/run_build.py
```

## Data source

Employment Permits Statistics 2025, Department of Enterprise, Trade &
Employment (Ireland) — https://enterprise.gov.ie/. Four breakdowns are
combined here: by nationality, by county, by economic sector (monthly), and
by sponsoring company (monthly). All totals reconcile to **31,044 permits
issued / 3,432 refused** across every file.

## License

Code in this repository is MIT licensed (see [`LICENSE`](LICENSE)). The
underlying data is published by DETE under Ireland's
[Open Data / PSI re-use terms](https://data.gov.ie/pages/licence) — refer to
the original publisher for data licensing terms.
