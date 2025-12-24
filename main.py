from pathlib import Path
import logging

# --------------------------------------------------------------
# Setup — Logging
# --------------------------------------------------------------
Path("logs").mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("PIPELINE")

# --------------------------------------------------------------
# Imports — Pipeline Phases
# --------------------------------------------------------------
from p1_scrape_oar import generate_oar_dataset as phase1_main
from p2_clean_companies import CompanyCleaner as Phase2
from p3_clean_facilities import FacilityProcessor as Phase3
from p4_relational_builder import RelationalBuilder as Phase4
from p5_analytics_dashboards import AnalyticsDashboard as Phase5
from p6_ai_module import DuplicateDetector as Phase6
from p7_export_final import FinalExporter as Phase7

# --------------------------------------------------------------
# Main Pipeline
# --------------------------------------------------------------

def main():
    try:
        logger.info("=== PHASE 1: DATA EXTRACTION START ===")
        phase1_main()
        logger.info("=== PHASE 1 COMPLETE ===\n")

        logger.info("=== PHASE 2: COMPANY CLEANING START ===")
        Phase2().run()
        logger.info("=== PHASE 2 COMPLETE ===\n")

        logger.info("=== PHASE 3: FACILITY PROCESSING START ===")
        Phase3().run()
        logger.info("=== PHASE 3 COMPLETE ===\n")

        logger.info("=== PHASE 4: RELATIONAL STRUCTURING START ===")
        Phase4().run()
        logger.info("=== PHASE 4 COMPLETE ===\n")

        logger.info("=== PHASE 5: ANALYTICS DASHBOARDS START ===")
        Phase5().run()
        logger.info("=== PHASE 5 COMPLETE ===\n")

        logger.info("=== PHASE 6: AI DUPLICATE DETECTION START ===")
        Phase6().run()
        logger.info("=== PHASE 6 COMPLETE ===\n")

        logger.info("=== PHASE 7: FINAL EXPORT START ===")
        Phase7().run()
        logger.info("=== PHASE 7 COMPLETE ===\n")

        logger.info("=== PIPELINE EXECUTED SUCCESSFULLY ===")

    except Exception as e:
        logger.exception("Pipeline failed: %s", e)

if __name__ == "__main__":
    main()
