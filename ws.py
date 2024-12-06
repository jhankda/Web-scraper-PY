import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """
    Scrape a website and extract basic information.
    
    Args:
        url (str): The URL of the website to scrape
    
    Returns:
        dict: A dictionary containing scraped information
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        
=        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return {
            'title': soup.title.string if soup.title else 'No title found',
            'headings': [h.text for h in soup.find_all(['h1', 'h2', 'h3'])],
            'links': [a.get('href') for a in soup.find_all('a', href=True)]
        }
    
    except requests.RequestException as e:
        print(f"Error occurred while scraping: {e}")
        return None

def main():
    url = 'https://www.google.com'
    scraped_data = scrape_website(url)
    
    if scraped_data:
        print("Website Title:", scraped_data['title'])
        
        print("\nHeadings:")
        for heading in scraped_data['headings']:
            print(f"- {heading}")
        
        print("\nLinks:")
        for link in scraped_data['links'][:10]:
            print(f"- {link}")

if __name__ == '__main__':
    main()