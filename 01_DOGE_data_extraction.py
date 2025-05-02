import requests
import pandas as pd

def fetch_doge_data(total_pages=15, per_page=500):
    """
    Fetches data from the DoGE API and returns it as a pandas DataFrame.

    Parameters:
    total_pages (int): Total number of pages to fetch from the API.
    per_page (int): Number of records per page.

    Returns:
    pd.DataFrame: DataFrame containing the fetched data.
    """
    base_url = "https://api.doge.gov/savings/contracts"
    all_data = []

    for page in range(1, total_pages + 1):
        params = {
            "sort_by": "savings",
            "sort_order": "desc",
            "page": page,
            "per_page": per_page
        }
        try:
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            all_data.extend(data["result"]["contracts"])
            print(f"Fetched page {page}/{total_pages}.")
        except Exception as e:
            print(f"Error fetching page {page}: {e}")

    return pd.DataFrame(all_data)

df = fetch_doge_data()
df['savings'] = pd.to_numeric(df['savings'], errors='coerce')
df['deleted_date'] = pd.to_datetime(df['deleted_date'])

df.to_csv("DOGE_contracts.csv", index=False)
