"""
PHASE 2 — Company Cleaning

Cleans and normalizes company data generated from Open Supply Hub (synthetic).
"""

import pandas as pd
import re
import logging
import hashlib
from pathlib import Path
from datetime import datetime
from unidecode import unidecode
import pycountry
from rapidfuzz import fuzz

# =====================
# Logging
# =====================
logger = logging.getLogger(__name__)

# =====================
# Cleaner Class
# =====================
class CompanyCleaner:

    LEGAL_SUFFIXES = [
        "inc", "llc", "ltd", "limited", "sa", "sarl", "sas",
        "plc", "corp", "corporation", "co", "company", "group", "holding"
    ]

    def __init__(self, input_path="data/raw/oar_companies_raw.csv"):
        self.input_path = Path(input_path)
        self.df = None
        self.cleaned_df = None

    # =====================
    # Load
    # =====================
    def load_data(self):
        logger.info(f"Loading raw data: {self.input_path}")
        self.df = pd.read_csv(self.input_path)
        logger.info(f"Loaded {len(self.df)} rows")

    # =====================
    # Cleaning Functions
    # =====================
    def clean_company_name(self, name: str) -> str:
        if pd.isna(name):
            return ""
        name = unidecode(str(name).lower().strip())
        name = re.sub(r"\s+", " ", name)

        suffix_pattern = r"\b(" + "|".join(self.LEGAL_SUFFIXES) + r")\b"
        name = re.sub(suffix_pattern, "", name, flags=re.IGNORECASE)

        name = re.sub(r"[^\w\s\-&]", " ", name)
        name = re.sub(r"\s+", " ", name).strip()
        return name.title()

    def normalize_country(self, country: str) -> str:
        if pd.isna(country):
            return "Unknown"
        try:
            c = pycountry.countries.lookup(country.strip())
            return c.name
        except LookupError:
            return country.strip().title()

    def generate_company_id(self, name: str, country: str) -> str:
        key = f"{name.lower()}|{country.lower()}"
        hash_id = hashlib.md5(key.encode()).hexdigest()[:10].upper()
        return f"CMP_{hash_id}"

    # =====================
    # Deduplication with fuzzy matching
    # =====================
    def deduplicate_companies(self, records):
        unique_companies = []
        seen_keys = []

        for record in records:
            name = record["company_name"]
            country = record["country"]
            is_duplicate = False

            for key in seen_keys:
                # fuzzy match > 90% considered same company
                if fuzz.token_sort_ratio(name, key["company_name"]) > 90 and country == key["country"]:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_companies.append(record)
                seen_keys.append({"company_name": name, "country": country})

        return unique_companies

    # =====================
    # Main Processing
    # =====================
    def process(self):
        self.load_data()
        logger.info("Cleaning company records...")

        rows = []

        for _, row in self.df.iterrows():
            clean_name = self.clean_company_name(row["company_name"])
            country = self.normalize_country(row["country"])

            record = {
                "company_id": self.generate_company_id(clean_name, country),
                "company_name": clean_name,
                "country": country,
                "industry": row.get("industry", ""),
                "description": row.get("description", ""),
                "website": row.get("website", ""),
                "facility_count": row.get("facility_count", 0),
                "first_seen": datetime.utcnow().date().isoformat()
            }
            rows.append(record)

        # Deduplicate with fuzzy matching
        deduped_records = self.deduplicate_companies(rows)
        self.cleaned_df = pd.DataFrame(deduped_records)
        logger.info(f"Unique companies after cleaning: {len(self.cleaned_df)}")

    # =====================
    # Save
    # =====================
    def save(self, output_dir="data/processed"):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        csv_path = f"{output_dir}/companies_cleaned_{ts}.csv"
        json_path = f"{output_dir}/companies_cleaned_{ts}.json"

        self.cleaned_df.to_csv(csv_path, index=False)
        self.cleaned_df.to_json(json_path, orient="records", indent=2)

        logger.info(f"Saved cleaned CSV: {csv_path}")
        logger.info(f"Saved cleaned JSON: {json_path}")

    # =====================
    # Runner
    # =====================
    def run(self):
        logger.info("=== PHASE 2: COMPANY CLEANING START ===")
        self.process()
        self.save()
        logger.info("=== PHASE 2: COMPANY CLEANING COMPLETE ===")


# =====================
# Entry Point
# =====================
if __name__ == "__main__":
    cleaner = CompanyCleaner()
    cleaner.run()
