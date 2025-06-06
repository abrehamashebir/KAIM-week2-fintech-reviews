import nltk

def setup_nltk():
    """
    Downloads required NLTK resources.
    Run this once at the beginning of your project or notebook.
    """
    try:
        nltk.download('punkt')
        nltk.download('punkt_tab')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('omw-1.4')
    except Exception as e:
        print(f"Error downloading NLTK resources: {e}")
