from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"

def summarize_text(text, max_length=130, min_length=30):
    """
    Lightweight extractive summarization using LSA algorithm
    """
    if not text or len(text) < min_length:
        return text
    
    # If text is already short, return it
    if len(text) <= max_length:
        return text
    
    try:
        # Parse the text
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
        
        # Use LSA (Latent Semantic Analysis) summarizer
        stemmer = Stemmer(LANGUAGE)
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        
        # Get 2 sentences for summary
        summary_sentences = summarizer(parser.document, 2)
        
       
        summary = " ".join([str(sentence) for sentence in summary_sentences])
        
   
        if len(summary) > max_length:
            summary = summary[:max_length].rsplit(' ', 1)[0] + "..."
        
        return summary
    except:
        # Fallback: just truncate
        return text[:max_length].rsplit(' ', 1)[0] + "..."