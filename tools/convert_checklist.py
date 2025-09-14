#!/usr/bin/env python3
"""
convert_checklist.py
Convert the original “Web Application Checklist_To Transform.xlsx” into the
new schema defined in README.md.

Usage:
    python convert_checklist.py input.xlsx output_prefix
Outputs:
    output_prefix.csv             # flat CSV
    output_prefix.json            # flat JSON
    output_prefix_nested.json     # nested JSON matching schema.json
"""
import json
from pathlib import Path

import pandas as pd

PLACEHOLDER = {
    "Subtask": "Todo: Subtask",
    "Description": "Todo: Description",
    "Tools": "Todo: Tools",
    "Links": "Todo: Links",
    "Applicability": "Todo: Applicability",
    "Sources": "Todo: Sources",
    "Tags": "Todo: Tags",
    "Subcategory Notes": ""
}

def to_bool(val: str) -> bool:
    return str(val).strip().lower() in {"yes", "true", "1"}

def convert(input_xlsx: str, output_prefix: str) -> None:
    df = pd.read_excel(input_xlsx)
    df.columns = [c.strip() for c in df.columns]

    # Propagate hierarchy values
    df["Category"].ffill(inplace=True)
    df["Sub Category"].ffill(inplace=True)

    # Map old columns to new names
    df["Item"]      = df["Check Name"].fillna("Todo: Item")
    df["Done"]      = df["Completed"].apply(to_bool).map({True: "TRUE", False: "FALSE"})
    df["Hidden"]    = df["Hide By Default"].apply(to_bool).map({True: "TRUE", False: "FALSE"})
    df["Priority"]  = df["Priority"].fillna(0).astype(int)
    df["ASVS"]      = df["AVSS Mapping"].fillna("")
    df["Description"]   = df["Description of Issue"].fillna(PLACEHOLDER["Description"])
    df["Tools"]         = df["Tools"].fillna(PLACEHOLDER["Tools"])
    df["Links"]         = df["Links to Tools or how to run"].fillna(PLACEHOLDER["Links"])
    df["Applicability"] = df["Applicability / N/A"].fillna(PLACEHOLDER["Applicability"])
    df["Sources"]       = df["Sources"].fillna(PLACEHOLDER["Sources"])
    df["Tags"]          = PLACEHOLDER["Tags"]

    # Add new schema columns
    df["Subtask"]        = PLACEHOLDER["Subtask"]
    df["Subtask Done"]   = "FALSE"
    df["Subtask Hidden"] = "FALSE"
    df["Subcategory Notes"] = PLACEHOLDER["Subcategory Notes"]

    cols = [
        "Category", "Sub Category", "Item", "Done",
        "Subtask", "Subtask Done", "Subtask Hidden",
        "ASVS", "Description", "Tools", "Links",
        "Applicability", "Sources", "Tags",
        "Priority", "Hidden", "Subcategory Notes"
    ]
    flat = df[cols]
    flat.to_csv(f"{output_prefix}.csv", index=False)
    flat.to_json(f"{output_prefix}.json", orient="records", indent=2)

    # Build nested JSON
    nested = []
    for (cat, sub), rows in flat.groupby(["Category", "Sub Category"]):
        cat_obj = next((c for c in nested if c["category"] == cat), None)
        if not cat_obj:
            cat_obj = {"category": cat, "subcats": []}
            nested.append(cat_obj)

        sub_obj = {
            "name": sub,
            "notes": rows["Subcategory Notes"].iloc[0],
            "items": []
        }
        for _, r in rows.iterrows():
            item = {
                "title": r["Item"],
                "done": r["Done"] == "TRUE",
                "hidden": r["Hidden"] == "TRUE",
                "priority": int(r["Priority"]),
                "tags": [t.strip() for t in r["Tags"].split(",") if t.strip()],
                "asvs": r["ASVS"],
                "desc": r["Description"],
                "tools": r["Tools"],
                "links": r["Links"],
                "applic": r["Applicability"],
                "sources": r["Sources"],
                "subtasks": []
            }
            if r["Subtask"] != PLACEHOLDER["Subtask"]:
                item["subtasks"].append({
                    "text": r["Subtask"],
                    "done": r["Subtask Done"] == "TRUE",
                    "hidden": r["Subtask Hidden"] == "TRUE"
                })
            sub_obj["items"].append(item)
        cat_obj["subcats"].append(sub_obj)

    Path(f"{output_prefix}_nested.json").write_text(json.dumps(nested, indent=2))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: convert_checklist.py input.xlsx output_prefix")
        raise SystemExit(1)
    convert(sys.argv[1], sys.argv[2])
