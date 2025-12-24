"""
5_analytics_dashboards.py
PHASE 5 — Analytics & Dashboards

Generates simple analytics visualizations:
1. Companies by country
2. Facilities per company
"""

import os
import logging
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------------
# Logging configuration
# ------------------------------------------------------------------
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Analytics Dashboard Class
# ------------------------------------------------------------------
class AnalyticsDashboard:

    def __init__(self):
        self.companies_df = None
        self.facilities_df = None
        self.links_df = None

    # --------------------------------------------------------------
    # Load relational data
    # --------------------------------------------------------------
    def load_relational_data(self):
        base_dir = "data/relational"

        if not os.path.exists(base_dir):
            raise FileNotFoundError(f"Relational directory not found: {base_dir}")

        def find_latest(pattern):
            files = [
                f for f in os.listdir(base_dir)
                if f.endswith(".csv") and pattern in f
            ]
            if not files:
                raise FileNotFoundError(f"No file found for pattern: {pattern}")
            files.sort(reverse=True)
            return os.path.join(base_dir, files[0])

        companies_path = find_latest("companies_")
        facilities_path = find_latest("facilities_")
        links_path = find_latest("company_facilities_")

        logger.info(f"Loading companies: {companies_path}")
        logger.info(f"Loading facilities: {facilities_path}")
        logger.info(f"Loading links: {links_path}")

        self.companies_df = pd.read_csv(companies_path)
        self.facilities_df = pd.read_csv(facilities_path)
        self.links_df = pd.read_csv(links_path)

        logger.info(f"Loaded {len(self.companies_df)} companies")
        logger.info(f"Loaded {len(self.facilities_df)} facilities")
        logger.info(f"Loaded {len(self.links_df)} company–facility links")

    # --------------------------------------------------------------
    # Chart 1 — Companies by Country
    # --------------------------------------------------------------
    def plot_companies_by_country(self, output_dir):
        country_counts = self.companies_df["country"].value_counts()

        plt.figure(figsize=(10, 6))
        country_counts.plot(kind="bar")
        plt.title("Companies by Country")
        plt.xlabel("Country")
        plt.ylabel("Number of Companies")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        path = os.path.join(output_dir, "companies_by_country.png")
        plt.savefig(path, dpi=300)
        plt.close()

        logger.info(f"Saved chart: {path}")

    # --------------------------------------------------------------
    # Chart 2 — Facilities per Company
    # --------------------------------------------------------------
    def plot_facilities_per_company(self, output_dir):
        facilities_per_company = (
            self.links_df.groupby("company_id")["facility_id"]
            .count()
        )

        plt.figure(figsize=(10, 6))
        plt.hist(facilities_per_company, bins=30)
        plt.title("Facilities per Company")
        plt.xlabel("Number of Facilities")
        plt.ylabel("Number of Companies")
        plt.tight_layout()

        path = os.path.join(output_dir, "facilities_per_company.png")
        plt.savefig(path, dpi=300)
        plt.close()

        logger.info(f"Saved chart: {path}")

    # --------------------------------------------------------------
    # Run full analytics pipeline
    # --------------------------------------------------------------
    def run(self):
        logger.info("=" * 50)
        logger.info("STARTING ANALYTICS PHASE")
        logger.info("=" * 50)

        self.load_relational_data()

        output_dir = "data/analytics"
        os.makedirs(output_dir, exist_ok=True)

        self.plot_companies_by_country(output_dir)
        self.plot_facilities_per_company(output_dir)

        logger.info("=" * 50)
        logger.info("ANALYTICS PHASE COMPLETED SUCCESSFULLY")
        logger.info("=" * 50)


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    dashboard = AnalyticsDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
