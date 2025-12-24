"""
PHASE 4 — Relational Structuring

Validates and exports the relational dataset:
- companies
- facilities
- company_facilities
"""

import pandas as pd
import logging
from pathlib import Path
from datetime import datetime

# =====================
# Logging
# =====================
logger = logging.getLogger(__name__)


class RelationalBuilder:

    def __init__(self):
        self.companies = None
        self.facilities = None
        self.links = None

    # =====================
    # Load
    # =====================
    def load_data(self):
        processed = Path("data/processed")

        companies_file = sorted(processed.glob("companies_cleaned_*.csv"), reverse=True)[0]
        facilities_file = sorted(processed.glob("facilities_cleaned_*.csv"), reverse=True)[0]
        links_file = sorted(processed.glob("company_facilities_*.csv"), reverse=True)[0]

        logger.info("Loading relational datasets")
        self.companies = pd.read_csv(companies_file)
        self.facilities = pd.read_csv(facilities_file)
        self.links = pd.read_csv(links_file)

        logger.info(
            f"Loaded {len(self.companies)} companies, "
            f"{len(self.facilities)} facilities, "
            f"{len(self.links)} links"
        )

    # =====================
    # Validation
    # =====================
    def validate(self) -> dict:
        logger.info("Validating relational integrity")

        results = {}

        company_ids = set(self.companies["company_id"])
        facility_ids = set(self.facilities["facility_id"])

        link_company_ids = set(self.links["company_id"])
        link_facility_ids = set(self.links["facility_id"])

        results["missing_companies"] = list(link_company_ids - company_ids)
        results["missing_facilities"] = list(link_facility_ids - facility_ids)

        results["orphan_companies"] = list(company_ids - link_company_ids)
        results["orphan_facilities"] = list(facility_ids - link_facility_ids)

        results["duplicate_company_ids"] = not self.companies["company_id"].is_unique
        results["duplicate_facility_ids"] = not self.facilities["facility_id"].is_unique
        results["duplicate_links"] = self.links.duplicated().any()

        # Logging
        if results["missing_companies"] or results["missing_facilities"]:
            logger.warning(" Foreign key issues detected")
        else:
            logger.info(" Foreign keys valid")

        if results["orphan_companies"] or results["orphan_facilities"]:
            logger.warning(" Orphan records detected")
        else:
            logger.info(" No orphan records")

        return results

    # =====================
    # Save
    # =====================
    def save(self):
        output_dir = Path("data/relational")
        output_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        companies_path = output_dir / f"companies_{ts}.csv"
        facilities_path = output_dir / f"facilities_{ts}.csv"
        links_path = output_dir / f"company_facilities_{ts}.csv"

        self.companies.to_csv(companies_path, index=False)
        self.facilities.to_csv(facilities_path, index=False)
        self.links.to_csv(links_path, index=False)

        logger.info("Relational datasets saved")
        logger.info(f"- {companies_path}")
        logger.info(f"- {facilities_path}")
        logger.info(f"- {links_path}")

    # =====================
    # Runner
    # =====================
    def run(self):
        logger.info("=== PHASE 4: RELATIONAL STRUCTURING START ===")
        self.load_data()
        validation = self.validate()
        self.save()
        logger.info("=== PHASE 4: RELATIONAL STRUCTURING COMPLETE ===")

        print("\nRELATIONAL VALIDATION SUMMARY")
        print("-" * 40)
        for k, v in validation.items():
            print(f"{k}: {len(v) if isinstance(v, list) else v}")


# =====================
# Entry Point
# =====================
if __name__ == "__main__":
    builder = RelationalBuilder()
    builder.run()
