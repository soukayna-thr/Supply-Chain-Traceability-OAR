"""
PHASE 3 — Facility Processing

Generates facility records from cleaned company data and
builds company–facility relationships.
"""

import pandas as pd
import logging
import hashlib
from pathlib import Path
from datetime import datetime

# =====================
# Logging
# =====================
logger = logging.getLogger(__name__)

# =====================
# Processor
# =====================
class FacilityProcessor:

    def __init__(self, company_file=None):
        self.company_file = company_file
        self.company_df = None
        self.facilities_df = None
        self.link_df = None

    # =====================
    # Load
    # =====================
    def load_companies(self):
        if not self.company_file:
            processed_dir = Path("data/processed")
            files = sorted(processed_dir.glob("companies_cleaned_*.csv"), reverse=True)
            if not files:
                raise FileNotFoundError("No cleaned company file found")
            self.company_file = files[0]

        logger.info(f"Loading companies from {self.company_file}")
        self.company_df = pd.read_csv(self.company_file)
        logger.info(f"Loaded {len(self.company_df)} companies")

    # =====================
    # Helpers
    # =====================
    def generate_facility_name(self, company_name: str, index: int) -> str:
        return f"{company_name} Facility {index}"

    def generate_facility_id(self, company_id: str, index: int) -> str:
        key = f"{company_id}|{index}"
        hash_id = hashlib.md5(key.encode()).hexdigest()[:10].upper()
        return f"FAC_{hash_id}"

    # =====================
    # Main Logic
    # =====================
    def process(self):
        self.load_companies()
        logger.info("Generating facilities from company data...")

        facilities = []
        links = []

        for _, row in self.company_df.iterrows():
            company_id = row["company_id"]
            company_name = row["company_name"]
            country = row["country"]
            facility_count = int(row.get("facility_count", 1))

            for i in range(1, facility_count + 1):
                facility_name = self.generate_facility_name(company_name, i)
                facility_id = self.generate_facility_id(company_id, i)

                facilities.append({
                    "facility_id": facility_id,
                    "facility_name": facility_name,
                    "country": country,
                    "created_at": datetime.utcnow().date().isoformat()
                })

                links.append({
                    "company_id": company_id,
                    "facility_id": facility_id
                })

        self.facilities_df = pd.DataFrame(facilities)
        self.link_df = pd.DataFrame(links)

        logger.info(f"Generated {len(self.facilities_df)} facilities")
        logger.info(f"Generated {len(self.link_df)} company–facility links")

    # =====================
    # Save
    # =====================
    def save(self, output_dir="data/processed"):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        facilities_path = f"{output_dir}/facilities_cleaned_{ts}.csv"
        links_path = f"{output_dir}/company_facilities_{ts}.csv"

        self.facilities_df.to_csv(facilities_path, index=False)
        self.link_df.to_csv(links_path, index=False)

        logger.info(f"Facilities saved to {facilities_path}")
        logger.info(f"Company-facility links saved to {links_path}")

    # =====================
    # Runner
    # =====================
    def run(self):
        logger.info("=== PHASE 3: FACILITY PROCESSING START ===")
        self.process()
        self.save()
        logger.info("=== PHASE 3: FACILITY PROCESSING COMPLETE ===")


# =====================
# Entry Point
# =====================
if __name__ == "__main__":
    processor = FacilityProcessor()
    processor.run()
