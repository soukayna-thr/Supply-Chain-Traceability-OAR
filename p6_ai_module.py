"""
PHASE 6 — AI Module

Task: Option C
Lightweight duplicate detection using embeddings on a small sample set (20–50 companies).
"""

import pandas as pd
import logging
from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# ----------------------------
# Logging
# ----------------------------
logger = logging.getLogger(__name__)

class DuplicateDetector:

    def __init__(self, input_file=None, sample_size=30, similarity_threshold=0.85):
        self.input_file = input_file
        self.sample_size = sample_size
        self.similarity_threshold = similarity_threshold
        self.df = None
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  
        self.duplicates = []

    # ----------------------------
    # Load data
    # ----------------------------
    def load_data(self):
        if not self.input_file:
            processed_dir = Path("data/processed")
            files = sorted(processed_dir.glob("companies_cleaned_*.csv"), reverse=True)
            if not files:
                raise FileNotFoundError("No cleaned company file found")
            self.input_file = files[0]

        logger.info(f"Loading company data: {self.input_file}")
        self.df = pd.read_csv(self.input_file)
        logger.info(f"Loaded {len(self.df)} companies")

        # Sample small set for lightweight detection
        self.df = self.df.sample(min(self.sample_size, len(self.df)), random_state=42).reset_index(drop=True)
        logger.info(f"Sampled {len(self.df)} companies for duplicate detection")

    # ----------------------------
    # Compute duplicates
    # ----------------------------
    def detect_duplicates(self):
        logger.info("Computing embeddings for duplicate detection...")
        descriptions = self.df["description"].fillna("").tolist()
        embeddings = self.model.encode(descriptions, convert_to_tensor=True)

        logger.info("Calculating pairwise similarities...")
        cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)

        n = len(descriptions)
        duplicates = []

        for i in range(n):
            for j in range(i + 1, n):
                score = float(cosine_scores[i][j])
                if score >= self.similarity_threshold:
                    duplicates.append({
                        "company_1_id": self.df.loc[i, "company_id"],
                        "company_1_name": self.df.loc[i, "company_name"],
                        "company_2_id": self.df.loc[j, "company_id"],
                        "company_2_name": self.df.loc[j, "company_name"],
                        "similarity": round(score, 3)
                    })

        self.duplicates = duplicates
        logger.info(f"Detected {len(duplicates)} potential duplicates")

    # ----------------------------
    # Save results
    # ----------------------------
    def save_results(self, output_dir="data/ai"):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        duplicates_df = pd.DataFrame(self.duplicates)
        csv_path = Path(output_dir) / f"duplicate_companies_{ts}.csv"
        json_path = Path(output_dir) / f"duplicate_companies_{ts}.json"

        duplicates_df.to_csv(csv_path, index=False)
        duplicates_df.to_json(json_path, orient="records", indent=2)

        logger.info(f"Duplicate results saved: {csv_path}")
        logger.info(f"Duplicate results saved: {json_path}")

    # ----------------------------
    # Runner
    # ----------------------------
    def run(self):
        logger.info("=== PHASE 6: DUPLICATE DETECTION START ===")
        self.load_data()
        self.detect_duplicates()
        self.save_results()
        logger.info("=== PHASE 6: DUPLICATE DETECTION COMPLETE ===")

# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    detector = DuplicateDetector(sample_size=30, similarity_threshold=0.85)
    detector.run()
