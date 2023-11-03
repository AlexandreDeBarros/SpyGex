import requests

class SpyGexController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def research(self):
        try:
            self.model.get_all_links(self.model.url) 
            self.model.match_regex_page(self.model.url_to_soup(self.model.url))  
            print(self.model.visited_urls)
            print(self.model.matched_results)
            #self.view.show_results(self.model.visited_urls)
            #self.view.show_matched_results(self.matched_results)
        except requests.RequestException as e:
            print(f"Erreur de requête HTTP pour l'URL : {e}")
        except Exception as e:
            print(f"Erreur lors du traitement de l'URL : {e}")