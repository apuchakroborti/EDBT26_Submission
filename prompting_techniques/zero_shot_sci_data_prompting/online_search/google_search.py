import requests
from bs4 import BeautifulSoup
import re

# Replace with your credentials
API_KEY = "AIzaSyAm82CvCNatMHNCJ2cz0ikFUkKLaA2ovXw"
CSE_ID = "a422c7508ffb644e0"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_google_cse(query, num_results=1):
    """Search Google CSE and return top result URL."""
    # url = "https://www.googleapis.com/customsearch/v1"
    url = "https://cse.google.com/cse?cx=a422c7508ffb644e0"
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": num_results,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    items = response.json().get("items", [])
    return [item["link"] for item in items]

def extract_description_and_code(url):
    """Extract description and code from a given page."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Grab top 1–2 paragraphs and first code block
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text() for p in paragraphs[:2]).strip()

        # Find first code block
        code = ""
        pre = soup.find("pre")
        if pre:
            code = pre.get_text()
        else:
            code_tags = soup.find_all("code")
            if code_tags:
                code = code_tags[0].get_text()

        return text.strip(), code.strip()

    except Exception as e:
        return "Could not fetch description.", "No code found."

def get_solution(query):
    print(f"🔍 Searching: {query}")
    urls = search_google_cse(query)
    if not urls:
        print("❌ No results found.")
        return

    for url in urls:
        print(f"\n📄 Extracting from: {url}")
        desc, code = extract_description_and_code(url)
        print("\n📝 Description:\n", desc)
        print("\n📌 Code Example:\n", code)
        break  # Only fetch from top result

# 🔧 Run
if __name__ == "__main__":
    user_query = input("Enter your problem description: ")
    get_solution(user_query)
