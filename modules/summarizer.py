
from transformers import pipeline
import streamlit as st

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"


@st.cache_resource(show_spinner=False)
def load_summarizer():
    return pipeline(
        "summarization",
        model=MODEL_NAME
    )


def summarize_text(text):
    if not text or not text.strip():
        return ""

    try:
        model = load_summarizer()

        # Keep the input within a manageable size
        text = text.strip()[:1500]

        result = model(
            text,
            max_length=60,
            min_length=10,
            do_sample=False,
            truncation=True,
            num_beams=2
        )

        return result[0]["summary_text"].strip()

    except Exception as e:
        raise RuntimeError(f"Summary generation failed: {e}") from e


if __name__ == "__main__":
    sample_text = """
    Machine Learning is a branch of Artificial Intelligence.
    It enables computers to learn from data without being
    explicitly programmed for every task. Machine learning
    algorithms identify patterns in data and use them to make
    predictions.
    """

    print(summarize_text(sample_text))
