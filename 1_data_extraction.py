# Section 1: API & Python Tools
import requests # This is how we talk to the API
import pandas as pd # This is how we handle data - organizing it into tables

# Section 2: Building the requests
BASE_URL = "https://api.doge.gov/savings/contracts" #The menu of the data we can get from the API
PARAMS = {
    "sort_by": "savings", # We want the biggest savings first
    "sort_order": "desc", # "desc" means biggest to smallest
    "per_page": 500, # We want to see 500 contracts (MAX) at a time"
}

# Section 3: Fetching the data
all_data = [] # This is where we will store the data we get from the API - Empty shopping cart

for page in range(1, 16): # We want to get 15 pages of data (500 contracts per page)
    PARAMS["page"] = page # We tell the API which page we want to see, page 1, then 2, then 3, etc.
    response = requests.get(BASE_URL, params=PARAMS) # We ask the API for the data - Place the order
    if response.status_code != 200: # If the API doesn't like our order, we get an error message
        print(f"Failed on page {page}... Error: {response.status_code}")

    data = response.json() # We get the data in JSON format
    all_data.extend(data["result"]["contracts"]) # We add the data to our shopping cart

# Section 4: Cleaning/Organizing the data
df = pd.DataFrame(all_data) # We put the raw data into a table (DataFrame)

print(df.describe()) # This gives us a summary of the data - like a menu of what we have in our shopping cart
print(df.head()) # This shows us the first 5 rows of the data - like a sneak peek at our shopping cart 

# Fix data types
df["savings"] = pd.to_numeric(df["savings"], errors="coerce") # We want the savings to be a number, not a string
df["deleted_date"] = pd.to_datetime(df["deleted_date"], errors="coerce") # We want the date to be a date, not a string
df = df.dropna(subset=["savings", "deleted_date"]) # We want to get rid of any rows that don't have savings or date

# Section 5: Saving the data
df.to_csv("DoGE_contracts_savings.csv", index=False) # We save the data to a CSV file - 
# This is our final Excel-friendly product