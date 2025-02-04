import requests
import xml.etree.ElementTree as ET
import json
import time

# JVN API Endpoint
BASE_URL = "https://jvndb.jvn.jp/myjvn"

# Function to fetch and parse vulnerabilities
def fetch_latest_vulnerabilities():
    params = {
        'method': 'getVulnOverviewList',
        'feed': 'hnd',  
        'startItem': 1,
        'maxCount': 5,
        'datePublished': '2025-01-01'
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        # Print the raw XML response for debugging
        print("Raw XML Response:", response.text[:500])  # Print first 500 chars

        # Parse XML response with namespaces
        root = ET.fromstring(response.text)

        # Find all <item> elements in the XML
        vulnerabilities = []
        for item in root.findall(".//{http://purl.org/rss/1.0/}item"):
            title = item.find("{http://purl.org/rss/1.0/}title")
            link = item.find("{http://purl.org/rss/1.0/}link")
            description = item.find("{http://purl.org/rss/1.0/}description")
            date = item.find("{http://jvndb.jvn.jp/rss/}date")

            vuln = {
                "title": title.text if title is not None else "N/A",
                "link": link.text if link is not None else "N/A",
                "description": description.text if description is not None else "N/A",
                "date": date.text if date is not None else "N/A",
            }
            vulnerabilities.append(vuln)

        return vulnerabilities

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Function to save data to JSON file
def save_to_json(data, filename="jvn_data.json"):
    with open(filename, "w", encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    while True:
        print("\nFetching latest vulnerabilities from JVN...")
        vuln_data = fetch_latest_vulnerabilities()
        if vuln_data:
            save_to_json(vuln_data)
            print(f"Data saved to jvn_data.json")
        else:
            print("No new data fetched.")
        print("\nWaiting for the next update...\n")
        time.sleep(3600)  # Wait 1 hour before the next fetch
