class SpyGexController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def research(self, url):
        success, visited_url = self.model.get_all_links(url)
        if success:
            self.view.show_results(visited_url)

            soup = self.model.url_to_soup(visited_url)
            regex = r"votre_regex"  
            matched_content = self.model.match_regex_page(regex, soup)
            
            response = requests.get(visited_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a')

            for link in links:
                href = link.get('href')
                if href and href.startswith('http'):
                    self.research(href)