import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests

class SpyGexModel:

    def __init__(self,regex,url,matched_results) :
        self.regex = regex
        self.url = url
        self.matched_results = matched_results
        self.visited_urls = set()

    def match_regex_page(self, regex, soup):
        matched_content = soup.find_all(string=re.compile(regex))
        self.matched_results.extend(matched_content)
        return matched_content

    def url_to_soup(self, url):
        return BeautifulSoup(requests.get(url).content, "html.parser")
    
    def is_same_domain(self, url):
        return urlparse(url).netloc == urlparse(self.url).netloc
    
    def export_csv(self):
        return

    
