import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

class SpyGexModel:

    def __init__(self) :
        self.regex
        self.url
        self.matched_results
        self.visited_urls = set()

    def match_regex_page(self, soup):
        matched_content = soup.find_all(string=re.compile(self.regex))
        self.matched_results.extend(matched_content)
        return matched_content

    def url_to_soup(self, url):
        return BeautifulSoup(requests.get(url).content, "html.parser")
    
    def is_same_domain(self, url):
        return urlparse(url).netloc == urlparse(self.url).netloc

    def get_all_links(url):
        self.visited_urls.add(url)  
        print("Visiting:", url)
    
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
    
        for link in links:
            href = link.get('href')
            if href and href.startswith('http') and (href not in visited_urls) and is_same_domain(href):
                get_all_links(href)  
    
    def export_csv(self):
        return

    
