class SpyGexController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def research(self, url):
        try:
            self.model.get_all_links(url, regex)
            print(self.model.visited_urls)
            print(self.model.matched_results)
            #self.view.show_results(self.model.visited_urls)
            #self.view.show_matched_results(self.matched_results)
        except requests.RequestException as e:
            print(f"Erreur de requête HTTP pour l'URL {url}: {e}")
        except Exception as e:
            print(f"Erreur lors du traitement de l'URL {url}: {e}")