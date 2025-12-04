# download_superstore.py
import urllib.request

url = "https://raw.githubusercontent.com/curran/data/gh-pages/superstoreSales/superstoreSales.csv"
print("Downloading Superstore dataset (8000+ rows)...")
urllib.request.urlretrieve(url, "sales_data.csv")
print("✓ Downloaded 8000+ sales records")