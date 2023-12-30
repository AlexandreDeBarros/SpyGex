import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup


class SpyGexModel:

    def __init__(self):
        self.regex = ''
        self.url = ''
        self.visited_urls = set()
        self.df_result = pd.DataFrame(columns=['Match', 'Line', 'Url'])
        self.session = requests.Session()
        self.regex_patterns = self.load_regex_patterns()

    def match_regex_page(self, soup):
        # Find content matching the regex
        matched_content = soup.find_all(string=re.compile(self.regex))
        for match in matched_content:
            new_row = pd.DataFrame(
                {'Match': [match], 'Line': [match.parent], 'Url': [self.url]})
            self.df_result = pd.concat(
                [self.df_result, new_row], ignore_index=True)
        return matched_content

    def url_to_soup(self, url):
        # Convert URL to BeautifulSoup object
        response = self.session.get(url)
        return BeautifulSoup(response.content, "lxml")

    def is_same_domain(self, url, base_url):
        # Check if the URL is from the same domain
        return urlparse(url).netloc == urlparse(base_url).netloc

    def start_crawling(self):
        # Begin crawling from the specified URL
        if self.url:  # : and self.url not in self.visited_urls:
            self.crawl(self.url)

    def crawl(self, url):
        # Recursive crawling method
        if True:  # url not in self.visited_urls:
            self.visited_urls.add(url)
            print("Visiting:", url)

            soup = self.url_to_soup(url)
            self.match_regex_page(soup)

            # Extract all links from the page
            links = [link.get('href')
                     for link in soup.find_all('a') if link.get('href')]

            # Filter valid links
            valid_links = [href for href in links if href.startswith(
                'http') and href not in self.visited_urls and self.is_same_domain(href, url)]

            # Use ThreadPoolExecutor for concurrent requests
            # Adjust the number of workers as needed
            with ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(self.crawl, valid_links)

    def export_file(self, file_path):
        if file_path.endswith('.csv'):
            # Write custom header with self.url and self.regex
            with open(file_path, 'w', newline='') as file:
                file.write(f'Url: {self.url}, Regex: {self.regex}\n')

            # Write DataFrame data to CSV
            self.df_result.to_csv(file_path, mode='a',
                                  index=False, header=True)

        elif file_path.endswith('.json'):
            # Write DataFrame data to JSON
            self.df_result.to_json(file_path, orient='records')

        elif file_path.endswith('.xlsx'):
            # Write DataFrame data to Excel
            self.df_result.to_excel(file_path, index=False)

    def load_regex_patterns(self):
        # Load regex patterns from a configuration file
        try:
            config_path = os.path.join(os.path.dirname(
                __file__), '..\\..\\config\\config.json')
            with open(config_path, 'r') as file:
                data = json.load(file)
                return data.get('regex_patterns', {})
        except FileNotFoundError:
            return {}

    def get_regex_patterns(self):
        # Return the loaded regex patterns
        return self.regex_patterns
