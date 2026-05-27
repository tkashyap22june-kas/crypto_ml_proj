
import sys
import os

# 🔥 CRITICAL FIX: add src to path
sys.path.insert(0, os.path.abspath("src"))

from crypto.pipeline.train_pipeline import TrainPipeline
from crypto.logger import logging
import traceback


def main():
    try:
        logging.info("🚀 Starting Crypto ML Pipeline...")

        pipeline = TrainPipeline()
        pipeline.run_pipeline()

        logging.info("✅ Pipeline Completed Successfully")
        print("✅ Pipeline Completed Successfully")

    except Exception as e:
        print("\n❌ PIPELINE FAILED\n")
        print(str(e))
        traceback.print_exc()


if __name__ == "__main__":
    main()
   