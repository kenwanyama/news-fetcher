from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"

def summarize_text(text, max_length=130, min_length=30):
    if not text or len(text) < min_length:
        return text

    if len(text) <= max_length:
        return text

    try:
        parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        summary_sentences = summarizer(parser.document, min(3, len(parser.document.sentences)))
        summary = " ".join([str(s) for s in summary_sentences])
        if len(summary) > max_length:
            summary = summary[:max_length].rsplit(' ', 1)[0] + "..."
        return summary
    except:
        return " ".join(text.split('.')[:2]) + "..."
