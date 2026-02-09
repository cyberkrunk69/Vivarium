import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def auto_tagging_algorithm(lesson):
    # Tokenize the lesson content
    tokens = word_tokenize(lesson)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Extract keywords
    keywords = [token for token in tokens if token.isalpha()]
    
    # Detect domain
    domain = None
    for keyword in keywords:
        if keyword in ['Claude', 'Groq', 'Spotify', 'GitHub', 'security', 'frontend']:
            domain = keyword.lower()
            break
    
    # Return the detected domain and keywords
    return domain, keywords