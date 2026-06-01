import os
import logging
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv

# Initialize environment configurations
load_dotenv()

# Configure logging parameters
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ingestion_engine")

def fetch_upstream_records(url: str, timeout_seconds: int = 10) -> list:
    """
    Fetches raw payload packets from an external REST endpoint.
    Handles network-level disruptions defensively.
    """
    logger.info(f"Initiating connection handshake with: {url}")
    
    try:
        response = requests.get(url, timeout=timeout_seconds)
        
        # Automatically flags 4xx and 5xx status anomalies
        response.raise_for_status()
        
        raw_data = response.json()
        logger.info(f"Ingestion successful. Retrieved {len(raw_data)} raw data elements.")
        return raw_data
        
    except RequestException as e:
        logger.error(f"Transport layer failure encountered during payload capture: {e}")
        # Return an empty list so the downstream pipeline doesn't crash
        return []

if __name__ == "__main__":
    # Test endpoint delivering public mock placeholder structures
    TEST_API_URL = "https://jsonplaceholder.typicode.com/users"
    
    records = fetch_upstream_records(TEST_API_URL)
    print(f"Sample Ingested Record: {records[0] if records else 'No Data'}")