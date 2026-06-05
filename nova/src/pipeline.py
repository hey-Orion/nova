import os
import json
from pathlib import Path

from nova.src.ingestion import fetch_data
from nova.src.validation import validate_records
from nova.src.logger import get_logger
from dotenv import load_dotenv
from nova.config.settings import config

load_dotenv()

logger = get_logger(__name__)

URL = os.getenv("API_URL")


def save_json(data: list, file_path: Path) -> None:

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def run_pipeline() -> None:

    logger.info("Pipeline started")

    logger.info("Fetching data...")

    records = fetch_data(URL)

    logger.info(f"Fetched {len(records)} records")

    valid_records, invalid_records = validate_records(records)

    logger.info(f"Valid Records: {len(valid_records)}")
    logger.info(f"Invalid Records: {len(invalid_records)}")

    save_json(
        valid_records,
        config["paths"]["VALIDATED_DATA"]
    )

    save_json(
        invalid_records,
        config["paths"]["REJECTED_DATA"]
    )

    logger.info("Saved validated records")
    logger.info("Saved rejected records")

    logger.info("pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()