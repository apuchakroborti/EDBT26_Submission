import requests
from bs4 import BeautifulSoup

# Replace with your real credentials
API_KEY = "AIzaSyAm82CvCNatMHNCJ2cz0ikFUkKLaA2ovXw"
# CSE_ID = "a422c7508ffb644e0"
CSE_ID = "107465684461199516578"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def search_google_cse(query, num_results=1):
    """Search using Google Custom Search Engine and return top result URLs."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": num_results
    }

    response = requests.get(url, params=params)

    # Debugging response if error occurs
    print("🔁 API Request URL:", response.url)
    print("📥 Status Code:", response.status_code)

    try:
        if not response.ok:
            raise ValueError(f"Request failed: {response.text}")

        if not response.headers.get("Content-Type", "").startswith("application/json"):
            raise ValueError("Expected JSON, but received non-JSON content.")

        results = response.json().get("items", [])
        return [item["link"] for item in results]

    except Exception as e:
        print("❌ Error:", e)
        return []


def extract_description_and_code(url):
    """Extracts description and first code block from a page."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Get first 2 non-empty paragraphs as description
        paragraphs = [p.get_text().strip() for p in soup.find_all("p")]
        description = "\n".join(p for p in paragraphs if p)[:500]

        # Get code block
        pre = soup.find("pre")
        code = pre.get_text().strip() if pre else ""

        return description.strip(), code.strip()

    except Exception as e:
        print(f"⚠️ Failed to extract from {url}: {e}")
        return "No description available.", "No code snippet found."


def get_solution(query):
    print(f"\n🔍 Searching for: {query}")
    urls = search_google_cse(query)

    if not urls:
        print("❌ No relevant search results found.")
        return

    print(f"\n✅ Top result from: {urls[0]}")
    desc, code = extract_description_and_code(urls[0])

    print("\n📝 Description:\n", desc or "No description found.")
    print("\n📌 Code Example:\n", code or "No code found.")


# 🔧 Run this script
if __name__ == "__main__":
    user_query = input("Enter your programming query: ").strip()
    if user_query:
        get_solution(user_query)
    else:
        print("❗Please provide a valid query.")
