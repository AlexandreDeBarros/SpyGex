# Data manipulation modules 
import json
import pandas as pd

# Web scraping modules
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests 

# Parallel processing modules
from concurrent.futures import ThreadPoolExecutor

# Spygex utils modules
from utils import spygex_utils as utils

class SpyGexModel:
    """
    A model for scraping and analyzing web content using regular expressions.
    """

    def __init__(self):
        """
        Initialize the SpyGexModel with default values.
        """

        self.regex = ''
        self.url = ''
        self.visited_urls = set()
        self.df_result = pd.DataFrame(columns=['Match', 'Line', 'Url'])
        self.session = requests.Session()
        self.regex_patterns = self.load_regex_patterns()
        self.workers_number= 1

    def match_regex_page(self, soup):
        """
        Find and store content matching the regex in a BeautifulSoup object.
        
        Args:
            soup (BeautifulSoup): The BeautifulSoup object to search through.

        Returns:
            list: A list of content matching the regex.
        """
        
        matched_content = soup.find_all(string=re.compile(self.regex))
        for match in matched_content:
            new_row = pd.DataFrame(
                {'Match': [match], 'Line': [match.parent], 'Url': [self.url]})
            self.df_result = pd.concat(
                [self.df_result, new_row], ignore_index=True)
        return matched_content

    def url_to_soup(self, url):
        """
        Convert a URL to a BeautifulSoup object.

        Args:
            url (str): The URL to convert.

        Returns:
            BeautifulSoup: The BeautifulSoup object of the URL's content.
        """

        response = self.session.get(url)
        return BeautifulSoup(response.content, "lxml")

    def is_same_domain(self, url, base_url):
        """
        Check if a given URL is from the same domain as the base URL.

        Args:
            url (str): The URL to check.
            base_url (str): The base URL for comparison.

        Returns:
            bool: True if the domains are the same, False otherwise.
        """

        return urlparse(url).netloc == urlparse(base_url).netloc

    def start_crawling(self):
        """
        Begin the web crawling process from the specified starting URL.
        """

        if self.url:
            self.crawl(self.url)

    def crawl(self, url):
        """
        Perform a recursive web crawling starting from a given URL.

        Args:
            url (str): The URL to start crawling from.
        """

        # Recursive crawling method
        if url not in self.visited_urls:
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
            with ThreadPoolExecutor(max_workers=self.workers_number) as executor:
                executor.map(self.crawl, valid_links)

    def export_file(self, file_path):
        """
        Export the scraped data to a file in CSV, JSON, or Excel format.

        Args:
            file_path (str): The path where the file will be saved.
        """

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
        """
        Load regex patterns from a configuration file.

        Returns:
            dict: A dictionary of loaded regex patterns.
        """

        try:
            config_path = utils.resolve_relative_path('../../config/config.json')
            with open(config_path, 'r') as file:
                data = json.load(file)
                return data.get('regex_patterns', {})
        except FileNotFoundError:
            return {}
