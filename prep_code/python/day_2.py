from ingestion import fetch_transactions

URL = "https://jsonplaceholder.typicode.com/posts"

records = fetch_transactions(URL)

print(f"Fetched {len(records)} records")

for record in records[:3]:
    print(record)
