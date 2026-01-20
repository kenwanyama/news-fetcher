from transformers import pipeline

summarizer = pipeline("summarization",
                      model="facebook/bart-large-cnn")

def summarize_text(text, max_length=130):
    if len(text.split()) < 50:
        return text  # short texts don't need summarization
    summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return summary[0]['summary_text']
