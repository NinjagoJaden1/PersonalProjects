import requests

API_KEY = "9df1a841-76f7-4aab-93f4-ef92a6b0abc1"
HEADERS = {"Authorization": API_KEY}
url = "https://api.balldontlie.io/v1/games?start_date=2024-06-01&end_date=2024-06-30&per_page=1"

resp = requests.get(url, headers=HEADERS)
print("Status:", resp.status_code)
print("Body:", resp.text)
