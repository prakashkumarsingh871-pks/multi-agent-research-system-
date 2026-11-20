import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    """Search the web for information and return titles, URLs, and snippets."""
    try:
        result = tavily.search(query=query, max_results=2)
        out = []
        for r in result.get("results", []):
            out.append(
                f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
            )
        return "\n".join(out) if out else "No search results found."
    except Exception as e:
        return f"Web search failed: {str(e)}"


# print(web_search.invoke("what are the recent news of war?"))


@tool
def scrape_url(url: str) -> str:
    """Scrape a webpage URL and return cleaned plain text."""
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:2000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"

#print(scrape_url.invoke("https://en.wikipedia.org/wiki/Moonshot_AI"))


    




