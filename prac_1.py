import requests
import csv
import re

# Define the GitHub API endpoint
api_endpoint = "https://api.github.com/repos/{owner}/{repo}/contents"

# Replace the placeholders with your own values
repos = [
    {"owner": "tensorflow", "repo": "tensorflow"},
    {"owner": "apache", "repo": "spark"},
    {"owner": "pandas-dev", "repo": "pandas"},
]

# Define the categories and their regular expressions
categories = {
    "data preprocessing": r"import pandas|from pandas",
    "machine learning": r"import tensorflow|from tensorflow|import sklearn|from sklearn",
    "data visualization": r"import matplotlib|from matplotlib|import seaborn|from seaborn",
}

# Set up the request headers
headers = {"User-Agent": "Mozilla/5.0"}

# Initialize the data list
data = []

# Retrieve the code from each repository
for repo in repos:
    url = api_endpoint.format(**repo)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        files = response.json()
        for file in files:
            if file["type"] == "file":
                # Classify the code based on its category
                code_url = file["download_url"]
                response = requests.get(code_url, headers=headers)
                if response.status_code == 200:
                    code = response.text
                    for category, pattern in categories.items():
                        if re.search(pattern, code):
                            data.append({"category": category, "code": code})
                            break

# Write the data to a CSV file
with open("code_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["category", "code"])
    writer.writeheader()
    for row in data:
        writer.writerow(row)
