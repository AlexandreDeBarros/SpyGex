import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

class SpyGexModel:

    def __init__(self,regex,url) :
        self.regex = regex
        self.url = url
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

    def get_all_links():
        success, visited_url = self.model.get_all_links(url)
        if success:
            self.view.show_results(visited_url)

            soup = self.model.url_to_soup(visited_url)
            matched_content = self.model.match_regex_page(self.regex, soup)
            
            response = requests.get(visited_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a')

            for link in links:
                href = link.get('href')
                if href and href.startswith('http'):
                    self.research(href)
    
    def export_csv(self):
        return

    
