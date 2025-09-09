import requests
import time
from typing import List, Dict

class ArtExtractor:

    def __init__(self, delay: float = 0.2):
        self.delay = delay
        self.session = requests.Session()

    def extract_artworks(self, fields )-> List[Dict]:

        if not fields:
            fields = ['id', 'title', 'artist_display', 'medium_display', 'date_display']

        search_url = "https://api.artic.edu/api/v1/artworks/search"
        all_oil_paintings = []
        from_offset = 0
        max_results = 1000  # testing
        # max_results = 10000  # API hard limit

        while from_offset < max_results:
            query_data = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "bool":{
                                "should": [
                                    {"match": {"classification_titles.keyword": "painting"}},
                                    {"match": {"artwork_type_title": "painting"}}
                                ],
                                "minimum_should_match": 1
                                }
                            },
                            { "match": {"medium_display": "oil"} }
                        ]
                    }
                },
                "from": from_offset,
                "size": 100, # max alllowed per request
                "fields": fields
            }

            response = requests.post(search_url, json=query_data)

            if response.status_code == 200:
                data = response.json()
                artworks = data['data']

                if not artworks:
                    break

                all_oil_paintings.extend(artworks)

                if len(artworks) < 100:
                    break
            
                from_offset += 100
                time.sleep(0.2)
            else:
                print(f"API Error: {response.status_code}")
                break
            
        return all_oil_paintings