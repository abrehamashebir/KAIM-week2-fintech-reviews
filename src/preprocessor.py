# src/preprocessor.py
import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from tqdm import tqdm
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
AMHARIC_STOPWORDS = [
    "እና", "የ", "ነው", "እንደ", "ላይ", "አለ", "ውስጥ", "ከ", "በ", "ለ",
    "እሱ", "እሷ", "እንደዚህ", "እንዲሁ", "ይህ", "ይህን", "ይህንን"
]

def preprocess_text(text, language='en'):
    """Clean and tokenize text based on language"""
    text = str(text).strip()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)

    if language == 'en':
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [w for w in tokens if w not in stopwords.words('english')]
    else:
        tokens = text.split()
        tokens = [w for w in tokens if w not in AMHARIC_STOPWORDS]

    return ' '.join(tokens)

def preprocess_reviews(raw_df):
    """Clean and process reviews dataframe"""
    df = raw_df[['content', 'score', 'at', 'bank', 'language']].copy()
    df.columns = ['review', 'rating', 'date', 'bank', 'language']

    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df.drop_duplicates(subset=['review', 'bank'], inplace=True)
    df.dropna(subset=['review'], inplace=True)

    tqdm.pandas(desc="Preprocessing text")
    df['processed_review'] = df.progress_apply(
        lambda x: preprocess_text(x['review'], x['language']), axis=1
    )
    return df


def get_sentiment_scores(df):
    """Calculate sentiment scores for reviews"""
    nltk.download('vader_lexicon', quiet=True)
    sia = SentimentIntensityAnalyzer()

    tqdm.pandas(desc="Calculating sentiment scores")
    df['sentiment'] = df['processed_review'].progress_apply(lambda x: sia.polarity_scores(x)['compound'])
    
    return df

def label_sentiment(df):
    """Label sentiment based on scores"""
    df['label'] = df['sentiment'].apply(
        lambda x: 'positive' if x > 0.05 else ('negative' if x < -0.05 else 'neutral')
    )
    return df