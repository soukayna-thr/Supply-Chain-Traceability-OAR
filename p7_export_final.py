"""
PHASE 7 — Final Export (export_final.py)

1. Export the final cleaned dataset in CSV or JSON format.
2. Produce summary statistics:
   - total companies
   - total facilities
   - facilities per company
3. Save logs or reports summarizing the pipeline execution.
"""

import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
import json

# ----------------------------
# Logging
# ----------------------------
logger = logging.getLogger(__name__)

class FinalExporter:

    def __init__(self, relational_dir="data/relational", ai_dir="data/ai"):
        self.relational_dir = Path(relational_dir)
        self.ai_dir = Path(ai_dir)
        self.companies_df = None
        self.facilities_df = None
        self.links_df = None
        self.ai_results_df = None
        self.summary_stats = {}

    # ----------------------------
    # Load relational & AI data
    # ----------------------------
    def load_data(self):
        # Load latest relational files
        companies_file = sorted(self.relational_dir.glob("companies_*.csv"), reverse=True)[0]
        facilities_file = sorted(self.relational_dir.glob("facilities_*.csv"), reverse=True)[0]
        links_file = sorted(self.relational_dir.glob("company_facilities_*.csv"), reverse=True)[0]

        self.companies_df = pd.read_csv(companies_file)
        self.facilities_df = pd.read_csv(facilities_file)
        self.links_df = pd.read_csv(links_file)

        logger.info(f"Loaded {len(self.companies_df)} companies, "
                    f"{len(self.facilities_df)} facilities, "
                    f"{len(self.links_df)} company–facility links")

        # Load latest AI results if available
        if self.ai_dir.exists():
            ai_files = sorted(self.ai_dir.glob("*.csv"), reverse=True)
            if ai_files:
                self.ai_results_df = pd.read_csv(ai_files[0])
                logger.info(f"Loaded AI results: {len(self.ai_results_df)} rows")
            else:
                logger.info("No AI results found")
        else:
            logger.info("AI directory does not exist")

    # ----------------------------
    # Generate summary statistics
    # ----------------------------
    def compute_summary_stats(self):
        total_companies = len(self.companies_df)
        total_facilities = len(self.facilities_df)
        facilities_per_company = self.links_df.groupby("company_id")["facility_id"].count().mean()

        self.summary_stats = {
            "total_companies": total_companies,
            "total_facilities": total_facilities,
            "average_facilities_per_company": round(facilities_per_company, 2)
        }

        logger.info("Summary statistics computed:")
        for k, v in self.summary_stats.items():
            logger.info(f"- {k}: {v}")

    # ----------------------------
    # Export final datasets
    # ----------------------------
    def export_final(self, output_dir="data/final"):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        # Export companies, facilities, links
        self.companies_df.to_csv(f"{output_dir}/companies_final_{ts}.csv", index=False)
        self.companies_df.to_json(f"{output_dir}/companies_final_{ts}.json", orient="records", indent=2)

        self.facilities_df.to_csv(f"{output_dir}/facilities_final_{ts}.csv", index=False)
        self.facilities_df.to_json(f"{output_dir}/facilities_final_{ts}.json", orient="records", indent=2)

        self.links_df.to_csv(f"{output_dir}/company_facilities_final_{ts}.csv", index=False)
        self.links_df.to_json(f"{output_dir}/company_facilities_final_{ts}.json", orient="records", indent=2)

        # Export AI results if available
        if self.ai_results_df is not None:
            self.ai_results_df.to_csv(f"{output_dir}/ai_results_final_{ts}.csv", index=False)
            self.ai_results_df.to_json(f"{output_dir}/ai_results_final_{ts}.json", orient="records", indent=2)

        # Save summary statistics as JSON
        with open(f"{output_dir}/summary_stats_{ts}.json", "w") as f:
            json.dump(self.summary_stats, f, indent=2)

        logger.info(f"Final datasets and summary statistics exported to {output_dir}")

    # ----------------------------
    # Runner
    # ----------------------------
    def run(self):
        logger.info("=== PHASE 7: FINAL EXPORT START ===")
        self.load_data()
        self.compute_summary_stats()
        self.export_final()
        logger.info("=== PHASE 7: FINAL EXPORT COMPLETE ===")

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    exporter = FinalExporter()
    exporter.run()
