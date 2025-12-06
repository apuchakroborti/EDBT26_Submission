import requests
import html
import time

def search_stackoverflow_questions(query, max_results=1):
    """Searches Stack Overflow for a query and returns the top question(s)."""
    url = "https://api.stackexchange.com/2.3/search/advanced"
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
        "accepted": True,
        "answers": 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    items = response.json().get("items", [])
    return items[:max_results]

def fetch_top_answer(question_id):
    """Fetches the top-voted answer for a question."""
    url = f"https://api.stackexchange.com/2.3/questions/{question_id}/answers"
    params = {
        "order": "desc",
        "sort": "votes",
        "site": "stackoverflow",
        "filter": "withbody"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    answers = response.json().get("items", [])
    if answers:
        return html.unescape(answers[0]["body"])
    return None

def extract_text_and_code_from_html(body_html):
    """Very simple text/code extractor from Stack Overflow HTML answer."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(body_html, "html.parser")

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

# 🔧 Example usage
if __name__ == "__main__":
    # query = "'int' object is not subscriptable"
    # search_and_fetch_answer(query)

    query = "vtk render to png"
    search_and_fetch_answer(query)

    # for the basemap
    print('---------BaseMap----------')
    query = "plot map with basemap"
    search_and_fetch_answer(query)


