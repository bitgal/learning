from typing import List, Dict, Tuple

class DataTransform:

    def __init__(self):
        pass

    def clean_oil_paintings(self, raw_paintings):
        cleaned_paintings = []
        
        for painting in raw_paintings:
            # clean text fields
            title = painting.get('title', 'Untitled').replace('\n', ' ').replace('\r', ' ').strip()
            artist = painting.get('artist_title', 'Unknown Artist').replace('\n', ' ').replace('\r', ' ').strip()
            
            # standardize missing data
            if not title or title.lower() in ['', 'untitled', 'unknown']:
                title = 'Untitled'
            
            cleaned_painting = {
                'id': painting.get('id'),
                'title': title,
                'artist': artist,
                'medium': painting.get('medium_display', ''),
                'year': painting.get('date_display', '')
            }
            
            cleaned_paintings.append(cleaned_painting)
        
        return cleaned_paintings

    def validate_paintings(clean_paintings):
        valid_paintings = []
        errors = []

        for p in clean_paintings:
            if not p.get('id'):
                errors.append(f"Missing ID: {p}")
                continue

            valid_paintings.append(p)
        return valid_paintings    

