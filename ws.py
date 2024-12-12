import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urljoin, urlparse

def is_valid_url(url):
  
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def web_scraper(url, iteration_depth=1):

    scraped_urls = set()
    all_scraped_data = []

    def scrape_single_url(current_url, current_depth):
        if current_url in scraped_urls or not is_valid_url(current_url):
            return []
        
        scraped_urls.add(current_url)
        
        try:
            headers = {
            }
            response = requests.get(current_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            page_data = {
                'url': current_url,
                'title': soup.title.string if soup.title else 'No Title',
                'headings': [h.text.strip() for h in soup.find_all(['h1', 'h2', 'h3'])],
                'depth': current_depth
            }
            
            links = []
            if current_depth < iteration_depth:
                links = [urljoin(current_url, a.get('href')) 
                         for a in soup.find_all('a', href=True) 
                         if urljoin(current_url, a.get('href')) not in scraped_urls]
            
            return [page_data] + [
                sub_data 
                for link in links 
                for sub_data in scrape_single_url(link, current_depth + 1)
            ]
        
        except requests.RequestException as e:
            print(f"Error scraping {current_url}: {e}")
            return []

    all_scraped_data = scrape_single_url(url, 0)
    return all_scraped_data

def save_to_csv(data, filename='scraped_data.csv'):
 
    if not data:
        print("No data to save!")
        return
    
    os.makedirs('output', exist_ok=True)
    
    filepath = os.path.join('output', filename)
    
    keys = set().union(*[d.keys() for d in data])
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=list(keys))
            
            writer.writeheader()
            
            writer.writerows(data)
        
        print(f"Data saved successfully to {filepath}")
    
    except IOError as e:
        print(f"Error saving CSV: {e}")

def main():
    url = input("Enter the starting URL to scrape: ")
    iteration_depth = int(input("Enter the number of link iteration depths (1-5): "))
    
    iteration_depth = max(1, min(iteration_depth, 5))
    
    scraped_data = web_scraper(url, iteration_depth)
    
    if iteration_depth > 1:
        save_to_csv(scraped_data)
    
    print(f"\nTotal pages scraped: {len(scraped_data)}")
    
    print("\nFirst few scraped pages:")
    for item in scraped_data[:5]:
        print(f"URL: {item['url']}")
        print(f"Title: {item['title']}")
        print(f"Depth: {item['depth']}")
        print("-" * 50)

if __name__ == '__main__':
    main()