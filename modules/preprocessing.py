
import re
import nltk

# Download the tokenizer data needed by NLTK
nltk.download("punkt")
nltk.download("punkt_tab")


def clean_text(text):
    # Replace multiple spaces and line breaks
    text = re.sub(r"\s+", " ", text)

    # Remove spaces at the beginning and end
    text = text.strip()

    return text


def split_into_sentences(text):
    # Divide text into individual sentences
    sentences = nltk.sent_tokenize(text)

    return sentences


if __name__ == "__main__":
    sample_text = """
    Machine Learning is a branch of AI.


    It enables computers to learn from data.
    """

    cleaned_text = clean_text(sample_text)
    sentences = split_into_sentences(cleaned_text)

    print("Cleaned Text:")
    print(cleaned_text)

    print("\nSentences:")
    for sentence in sentences:
        print(sentence)
