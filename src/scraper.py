from google_play_scraper import app, Sort, reviews
import pandas as pd
from tqdm import tqdm

def scrape_reviews(bank_apps, languages=['en', 'am'], reviews_per_lang=600):
    """
    Scrape limited reviews (e.g., 400 per bank) in specified languages
    
    Args:
        bank_apps (dict): {bank_name: app_id} mapping
        languages (list): Languages to scrape ('en', 'am')
        reviews_per_lang (int): Reviews per language per bank
    
    Returns:
        pd.DataFrame: Combined reviews dataframe
    """
    all_reviews = []

    for bank, app_id in tqdm(bank_apps.items(), desc="Scraping banks"):
        for lang in languages:
            try:
                result, _ = reviews(
                    app_id,
                    lang=lang,
                    country='et',
                    sort=Sort.NEWEST,
                    count=reviews_per_lang,
                    filter_score_with=None
                )
                df = pd.DataFrame(result)
                df['bank'] = bank
                df['language'] = lang
                all_reviews.append(df)
            except Exception as e:
                print(f"Error scraping {bank} ({lang}): {str(e)}")
                continue

    return pd.concat(all_reviews, ignore_index=True)
