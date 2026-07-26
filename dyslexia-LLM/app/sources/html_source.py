import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass

@dataclass
class WebsiteArticle:
    title: str
    url: str
    text: str

def get_website(url: str) -> WebsiteArticle:

    response = requests.get(
        url,
        timeout=10,
        # Header to mimic a real browser request
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac macOS 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
    )
    
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # parse the HTML into title paragraphs and text
    title = soup.title.get_text(strip=True)
    paragraphs = soup.find_all("p")
    text = "\n\n".join(paragraph.get_text(" ", strip=True) for paragraph in paragraphs)
    
    return WebsiteArticle(
        title=title,
        url=url,
        text=text,
    )