"""
PHISHGUARD//NEXUS - Feature Matrix Construction & Domain-Grouped Split
Extracts features and splits using GroupShuffleSplit on registered domain
to strictly prevent data leakage across splits.
"""

import sys
import json
from pathlib import Path
import pandas as pd
from sklearn.model_selection import GroupShuffleSplit

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.ml.features.url_features import extract_url_features

DATA_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("[*] Loading raw dataset...")
    with open(RAW_DIR / "dataset.json", "r", encoding="utf-8") as f:
        records = json.load(f)

    print(f"[*] Extracting features for {len(records)} samples...")
    rows = []
    for r in records:
        feat = extract_url_features(r["url"])
        feat["label"] = r["label"]
        feat["domain"] = r["domain"]
        rows.append(feat)

    df = pd.DataFrame(rows)
    print(f"[+] Feature matrix shape: {df.shape}")

    # Step 1: Train (70%) vs Temp (30%) grouped by domain
    gss1 = GroupShuffleSplit(n_splits=1, train_size=0.70, random_state=42)
    train_idx, temp_idx = next(gss1.split(df, groups=df["domain"]))
    train_df = df.iloc[train_idx]
    temp_df = df.iloc[temp_idx]

    # Step 2: Split Temp into Validation (10% total) and Test (20% total) -> 1/3 and 2/3 of Temp
    gss2 = GroupShuffleSplit(n_splits=1, train_size=0.333, random_state=42)
    val_idx, test_idx = next(gss2.split(temp_df, groups=temp_df["domain"]))
    val_df = temp_df.iloc[val_idx]
    test_df = temp_df.iloc[test_idx]

    print(f"[+] Train set: {len(train_df)} samples ({train_df['domain'].nunique()} unique domains)")
    print(f"[+] Val set:   {len(val_df)} samples ({val_df['domain'].nunique()} unique domains)")
    print(f"[+] Test set:  {len(test_df)} samples ({test_df['domain'].nunique()} unique domains)")

    # Save to processed directory
    train_df.to_csv(PROCESSED_DIR / "train.csv", index=False)
    val_df.to_csv(PROCESSED_DIR / "val.csv", index=False)
    test_df.to_csv(PROCESSED_DIR / "test.csv", index=False)
    print("[+] Saved processed feature CSVs to backend/data/processed/")

if __name__ == "__main__":
    main()
