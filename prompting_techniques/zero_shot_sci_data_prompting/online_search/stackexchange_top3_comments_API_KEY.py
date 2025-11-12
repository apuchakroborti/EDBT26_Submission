import requests
import html
from bs4 import BeautifulSoup


API_KEY = "rl_CZtcfs8jjNSvhTFY7pKJHwoxZ"

def search_stackoverflow_questions(query, max_results=1):
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

def fetch_top_answers(question_id, top_n=3):
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
    return response.json().get("items", [])[:top_n]

def fetch_comments_on_answer(answer_id):
    url = f"https://api.stackexchange.com/2.3/answers/{answer_id}/comments"
    params = {
        "order": "desc",
        "sort": "creation",
        "site": "stackoverflow",
        "filter": "withbody",
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return [html.unescape(comment['body']) for comment in response.json().get("items", [])]

def extract_text_and_code_from_html(html_body):
    soup = BeautifulSoup(html_body, "html.parser")
    paragraphs = [p.get_text() for p in soup.find_all("p")]
    code_blocks = [code.get_text() for code in soup.find_all("code")]
    return "\n".join(paragraphs), "\n\n".join(code_blocks)

def search_and_fetch_top_answers(query):
    print(f"\n🔍 Searching for: {query}")
    questions = search_stackoverflow_questions(query)
    if not questions:
        print("❌ No matching questions found.")
        return ''

    top_question = questions[0]
    title = top_question["title"]
    link = top_question["link"]
    qid = top_question["question_id"]

    print(f"\n✅ Top Question: {title}\n🔗 {link}")

    answers = fetch_top_answers(qid, top_n=3)
    
    description_and_code_example = ''
    
    for i, ans in enumerate(answers, 1):
        print(f"\n--- 🟩 Answer #{i} ---")
        text, code = extract_text_and_code_from_html(ans["body"])
        print(f"\n📝 Description:\n{text.strip()}")
        description_and_code_example+=text.strip()+'\n'
        if code:
            print(f"\n📌 Code:\n{code.strip()}")
            description_and_code_example+=f'Example code:\n{code}'
        else:
            print("\n(No code block found.)")

        # 🔽 Fetch comments for this answer
        comments = fetch_comments_on_answer(ans["answer_id"])
        if comments:
            print("\n💬 Comments:")
            for c in comments:
                print(f"• {c.strip()}")
        else:
            print("\n(No comments found.)")
    return description_and_code_example

# 🔧 Run script
if __name__ == "__main__":
    user_query = input("Enter your query (e.g., 'vtk render to png'): ")
    search_and_fetch_top_answers(user_query)
