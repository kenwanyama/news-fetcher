from functools import lru_cache
from transformers import pipeline

@lru_cache(maxsize=1)
def get_summarizer():
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn"
    )

def summarize_text(text, max_length=130):
    if len(text.split()) < 50:
        return text  # skip short text
    summarizer = get_summarizer()
    summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return summary[0]['summary_text']
