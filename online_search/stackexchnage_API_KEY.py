import requests
import html
from bs4 import BeautifulSoup

# "your_api_key_here"  # ← Replace with your Stack Exchange API key

API_KEY = "rl_CZtcfs8jjNSvhTFY7pKJHwoxZ"
def search_stackoverflow_questions(query, max_results=1):
    """Search for questions related to a query using the Stack Exchange API."""
    url = "https://api.stackexchange.com/2.3/search/advanced"
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
        "accepted": True,
        "answers": 1,
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get("items", [])[:max_results]

def fetch_top_answer(question_id):
    """Fetch the top-voted answer (with full body) for a given question ID."""
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow",
        "filter": "withbody",
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    answers = response.json().get("items", [])
    if answers:
        return html.unescape(answers[0]["body"])
    return None

def extract_text_and_code_from_html(html_body):
    """Extract plain text and code blocks from the HTML body using BeautifulSoup."""
    soup = BeautifulSoup(html_body, "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all("p")]
    code_blocks = [code.get_text() for code in soup.find_all("code")]
    return "\n".join(paragraphs), "\n\n".join(code_blocks)

def search_and_fetch_answer(error_query):
    print(f"🔍 Searching for: {error_query}")
    questions = search_stackoverflow_questions(error_query)
    if not questions:
        print("❌ No matching questions found.")
        return

    top_question = questions[0]
    title = top_question["title"]
    link = top_question["link"]
    qid = top_question["question_id"]

    print(f"\n✅ Top Question: {title}\n🔗 {link}")

    answer_html = fetch_top_answer(qid)
    if answer_html:
        text, code = extract_text_and_code_from_html(answer_html)
        print("\n📝 Description:\n", text.strip())
        if code:
            print("\n📌 Code Example:\n", code.strip())
        else:
            print("\n(No code block found.)")
    else:
        print("\n❌ No answer found.")

# Example usage
if __name__ == "__main__":
    query = input("Enter your query (e.g., 'vtk render to png'): ")
    search_and_fetch_answer(query)
