## This function helps to reduce any white noise or unnecessary vocabulary to allow for a consistent structure for the ML.

import re

def clean_text(text):
    text = text.lower()

    # Remove URLs in parentheses (e.g., (https://...))
    text = re.sub(r'\(https?://[^\s)]+\)', '', text)

    # Remove any remaining URLs not in parentheses
    text = re.sub(r'https?://\S+', '', text)

    # Remove any instances of non-alphabetic characters but keep spaces
    text = re.sub(r'[^a-z\s]', '', text)

    # Remove extra whitespace
    text = ' '.join(text.split())

    # Remove simple stopwords manually
    stopwords = {'the', 'is', 'in', 'and', 'to', 'a', 'of', 'it', 'for', 'on', 'with', 'as', 'at', 'by'}
    words = [word for word in text.split() if word not in stopwords]
    
    cleaned_text = ' '.join(words)
    
    return cleaned_text