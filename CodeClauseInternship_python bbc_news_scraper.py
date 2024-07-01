import requests
from bs4 import BeautifulSoup

def scrape_bbc_news():
    """Scrape the titles of the latest news articles from BBC News."""
    url = 'https://www.bbc.com/news'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = soup.find_all('h3', class_='gs-c-promo-heading__title')

    print("Latest BBC News Headlines:")
    for i, headline in enumerate(headlines, start=1):
        print(f"{i}. {headline.get_text()}")

if __name__ == "__main__":
    scrape_bbc_news()
