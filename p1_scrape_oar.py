"""
PHASE 1 — Data Extraction (Synthetic OAR Dataset)

This script generates a synthetic dataset mimicking the Open Supply Hub
(Open Apparel Registry) structure when public data access is unavailable.
"""

import csv
import logging
import random
from pathlib import Path
from datetime import datetime

# =====================
# Configuration
# =====================
logger = logging.getLogger(__name__)

OUTPUT_DIR = Path("data/raw")
OUTPUT_FILE = OUTPUT_DIR / "oar_companies_raw.csv"

TARGET_COUNTRIES = [
    "Morocco",
    "Spain",
    "Portugal",
    "Italy",
    "France",
    "Greece",
    "Malta"
]

TOTAL_COMPANIES = 12000  

INDUSTRIES = [
    "Textiles",
    "Garment Manufacturing",
    "Footwear",
    "Leather Goods",
    "Agriculture",
    "Packaging",
    "Logistics"
]

# =====================
# Logging Setup
# =====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/scrape_oar.log"),
        logging.StreamHandler()
    ]
)

# =====================
# Utility Functions
# =====================
def generate_company_name(country: str, index: int) -> str:
    suffixes = ["Ltd", "SARL", "SA", "SPA", "LDA", "Company"]
    return f"{country} Industrial Group {index} {random.choice(suffixes)}"


def generate_description(industry: str) -> str:
    return (
        f"Company operating in the {industry.lower()} sector, "
        "specializing in regional and international supply chains."
    )


# =====================
# Main Extraction Logic
# =====================
def generate_oar_dataset() -> None:
    logging.info("Starting synthetic OAR data extraction")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    Path("logs").mkdir(exist_ok=True)

    companies_per_country = TOTAL_COMPANIES // len(TARGET_COUNTRIES)

    rows = []

    company_id = 1
    for country in TARGET_COUNTRIES:
        logging.info(f"Generating companies for {country}")

        for i in range(companies_per_country):
            industry = random.choice(INDUSTRIES)

            row = {
                "company_name": generate_company_name(country, company_id),
                "country": country,
                "registration_number": f"{country[:2].upper()}-{random.randint(100000, 999999)}",
                "industry": industry,
                "description": generate_description(industry),
                "website": f"https://www.company{company_id}.com",
                "facility_count": random.randint(1, 12),
                "source": "OpenSupplyHub (synthetic)",
                "extracted_at": datetime.utcnow().isoformat()
            }

            rows.append(row)
            company_id += 1

    logging.info(f"Total companies generated: {len(rows)}")

    # =====================
    # Save to CSV
    # =====================
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    logging.info(f"Dataset saved to {OUTPUT_FILE.resolve()}")
    logging.info("PHASE 1 — Data extraction completed successfully")


# =====================
# Entry Point
# =====================
if __name__ == "__main__":
    generate_oar_dataset()
