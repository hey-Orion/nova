import json
from pathlib import Path

from nova.src.ingestion import fetch_transactions
from nova.src.validation import validate_transactions


URL = "https://jsonplaceholder.typicode.com/posts"


def save_json(data: list, file_path: Path) -> None:
    """
    Save data to a JSON file.
    """

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def run_pipeline() -> None:
    """
    Run the ETL pipeline.
    """

    print("Fetching data...")

    records = fetch_transactions(URL)

    print(f"Fetched {len(records)} records")

    valid_records, invalid_records = validate_transactions(records)

    print(f"Valid Records: {len(valid_records)}")
    print(f"Invalid Records: {len(invalid_records)}")

    save_json(
        valid_records,
        Path("nova/data/validated/transactions.json")
    )

    save_json(
        invalid_records,
        Path("nova/data/rejected/rejected_transactions.json")
    )

    print("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()

    