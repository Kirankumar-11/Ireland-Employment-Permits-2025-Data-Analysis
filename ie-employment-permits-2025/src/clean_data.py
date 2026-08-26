"""
clean_data.py
--------------
Cleans the four raw Employment Permits Statistics 2025 workbooks
(published by Ireland's Dept. of Enterprise, Trade & Employment) and
writes tidy CSVs to data/processed/.

Run from the project root:
    python src/clean_data.py
"""

from pathlib import Path
import pandas as pd

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def clean_nationality() -> pd.DataFrame:
    """Permits issued & refused by nationality."""
    df = pd.read_excel(RAW_DIR / "permits-by-nationality-2025.xlsx")
    df.columns = ["nationality", "issued", "refused"]
    df = df[df["nationality"] != "Grand Total"]          # drop summary row
    df["issued"] = pd.to_numeric(df["issued"], errors="coerce").fillna(0).astype(int)
    df["refused"] = pd.to_numeric(df["refused"], errors="coerce").fillna(0).astype(int)
    df["applications"] = df["issued"] + df["refused"]
    df["refusal_rate"] = (df["refused"] / df["applications"]).round(4)
    df = df.sort_values("issued", ascending=False).reset_index(drop=True)
    return df


def clean_county() -> pd.DataFrame:
    """Permits issued & refused by county."""
    df = pd.read_excel(RAW_DIR / "permits-by-county-2025.xlsx")
    df.columns = ["county", "issued", "refused"]
    df = df[df["county"].notna() & (df["county"] != "Grand Total")]
    df["issued"] = pd.to_numeric(df["issued"], errors="coerce").fillna(0).astype(int)
    df["refused"] = pd.to_numeric(df["refused"], errors="coerce").fillna(0).astype(int)
    df["applications"] = df["issued"] + df["refused"]
    df["refusal_rate"] = (df["refused"] / df["applications"]).round(4)
    df = df.sort_values("issued", ascending=False).reset_index(drop=True)
    return df


def clean_sector() -> pd.DataFrame:
    """Permits issued by sector, wide (one column per month) -> tidy long format."""
    df = pd.read_excel(RAW_DIR / "permits-by-sector-2025.xlsx")
    df = df.rename(columns={"Unnamed: 0": "sector"})
    df = df[df["sector"] != "Grand Total"]
    for m in MONTHS + ["Grand Total"]:
        df[m] = pd.to_numeric(df[m], errors="coerce").fillna(0).astype(int)
    df = df.rename(columns={"Grand Total": "total_issued"})

    # split the "A - Agriculture..." style codes into a letter + label
    split = df["sector"].str.extract(r"^([A-Z])\s*-\s*(.*)$")
    df["sector_code"] = split[0]
    df["sector_label"] = split[1].fillna(df["sector"])

    wide = df.sort_values("total_issued", ascending=False).reset_index(drop=True)

    long = wide.melt(
        id_vars=["sector", "sector_code", "sector_label"],
        value_vars=MONTHS,
        var_name="month",
        value_name="issued",
    )
    long["month"] = pd.Categorical(long["month"], categories=MONTHS, ordered=True)

    return wide, long


def clean_companies() -> pd.DataFrame:
    """Permits issued per sponsoring company, wide -> tidy long format."""
    df = pd.read_excel(RAW_DIR / "permits-by-company-2025.xlsx")
    df = df.rename(columns={"Unnamed: 0": "company"})
    df = df[df["company"].notna() & (df["company"] != "Grand Total")]
    for m in MONTHS + ["Grand Total"]:
        df[m] = pd.to_numeric(df[m], errors="coerce").fillna(0).astype(int)
    df = df.rename(columns={"Grand Total": "total_issued"})
    wide = df.sort_values("total_issued", ascending=False).reset_index(drop=True)

    long = wide.melt(
        id_vars=["company"],
        value_vars=MONTHS,
        var_name="month",
        value_name="issued",
    )
    long["month"] = pd.Categorical(long["month"], categories=MONTHS, ordered=True)
    return wide, long


def main():
    nat = clean_nationality()
    nat.to_csv(PROCESSED_DIR / "permits_by_nationality.csv", index=False)

    county = clean_county()
    county.to_csv(PROCESSED_DIR / "permits_by_county.csv", index=False)

    sector_wide, sector_long = clean_sector()
    sector_wide.to_csv(PROCESSED_DIR / "permits_by_sector_wide.csv", index=False)
    sector_long.to_csv(PROCESSED_DIR / "permits_by_sector_monthly.csv", index=False)

    comp_wide, comp_long = clean_companies()
    comp_wide.to_csv(PROCESSED_DIR / "permits_by_company_wide.csv", index=False)
    comp_long.to_csv(PROCESSED_DIR / "permits_by_company_monthly.csv", index=False)

    print("Cleaned files written to:", PROCESSED_DIR)
    for f in sorted(PROCESSED_DIR.glob("*.csv")):
        print(" -", f.name)


if __name__ == "__main__":
    main()
