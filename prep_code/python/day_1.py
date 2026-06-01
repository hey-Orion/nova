import requests
from typing import Any


def fetch_transactions(url: str, timeout: int = 5) -> list[dict[str, Any]]:
    """
    Fetch raw transaction data from an API.

    Parameters
    ----------
    url : str
        API endpoint returning JSON transaction records.
    timeout : int
        Request timeout in seconds.

    Returns
    -------
    list[dict]
        Raw transaction records.
    """

    try:
        response = requests.get(url, timeout=timeout)

        # Raise exception for 4xx/5xx responses
        response.raise_for_status()

        data = response.json()

        if not isinstance(data, list):
            raise ValueError("Expected API to return a list of records")

        return data

    except requests.exceptions.Timeout:
        print("Request timed out")
        raise

    except requests.exceptions.ConnectionError:
        print("Failed to connect to API")
        raise

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        raise

    except ValueError as e:
        print(f"Invalid JSON response: {e}")
        raise

