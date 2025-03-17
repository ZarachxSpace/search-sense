import requests

def fetch_google_suggestions(query: str):
    """Fetch related search queries from Google Autocomplete API."""
    url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={query}"
    response = requests.get(url)
    suggestions = response.json()[1] if response.status_code == 200 else []
    return suggestions

def fetch_duckduckgo_suggestions(query: str):
    """Fetch related search queries from DuckDuckGo Instant Answers API."""
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
    response = requests.get(url)
    data = response.json()
    return [topic["Text"] for topic in data.get("RelatedTopics", []) if "Text" in topic]