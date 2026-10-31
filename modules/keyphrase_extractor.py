
from keybert import KeyBERT

# Load the pretrained keyword extraction model
keyword_model = None


def load_keyword_model():
    global keyword_model

    if keyword_model is None:
        keyword_model = KeyBERT(
            model="all-MiniLM-L6-v2"
        )

    return keyword_model


def extract_keyphrases(text, top_n=5):
    if not text or not text.strip():
        return []

    model = load_keyword_model()

    keywords = model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words="english",
        top_n=top_n
    )

    return [
        {"phrase": phrase, "score": round(score, 3)}
        for phrase, score in keywords
    ]


if __name__ == "__main__":
    sample_text = """
    Wind turbines convert the kinetic energy of wind into electricity.
    The Betz limit describes the maximum theoretical energy that
    a wind turbine can extract from the wind. Tip speed ratio
    compares blade speed with wind speed.
    """

    results = extract_keyphrases(sample_text)

    print("Extracted Keyphrases:")

    for item in results:
        print(item["phrase"], "-", item["score"])
