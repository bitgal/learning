"""
A learning project
Subjects: Data science, ETL
Theme: Visualisation of artwork data from the Chicago Art Institute API
Objectives: 
 - Build a Python pipeline that extracts data from a public API, transforms it, and loads into SQLite/PostgreSQL
 - Use pandas, requests, and schedule for automation
 - Show data quality checks and error handling
"""
import pandas as pd

def load_data(paintings):
    for p in paintings:
        print(f"{p['title']} by {p['artist']}, {p['year']}")
    
    df = pd.DataFrame(paintings)
    df.to_csv('oil_paintings.csv', index=False)
    return pd.read_csv('oil_paintings.csv')

def extract_and_transform_data():
    transform_functions = [clean_oil_paintings, validate_paintings ]
    paintings_to_transform = extract_data()
    for f in transform_functions:
        paintings_to_transform = f(paintings_to_transform)
    return paintings_to_transform

def clean_oil_paintings(raw_paintings):
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

clean_data = extract_and_transform_data()
load_data(clean_data)
