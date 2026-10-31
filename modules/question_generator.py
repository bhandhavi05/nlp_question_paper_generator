
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "valhalla/t5-small-e2e-qg"

tokenizer = None
model = None


def load_question_model():
    global tokenizer, model

    if tokenizer is None or model is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

        model = AutoModelForSeq2SeqLM.from_pretrained(
            MODEL_NAME
        )

    return tokenizer, model


def generate_questions(text, max_questions=5):
    if not text or not text.strip():
        return []

    tokenizer, model = load_question_model()

    # Limit input size for the first version
    text = " ".join(text.split()[:150])

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=128,
        num_beams=4,
        do_sample=False
    )

    generated_text = tokenizer.decode(
        outputs[0],
        skip_special_tokens=False
    )

    # Remove special tokens and separate questions
    generated_text = generated_text.replace(
        tokenizer.pad_token or "", ""
    )

    generated_text = generated_text.replace(
        tokenizer.eos_token or "", ""
    )

    questions = [
        question.strip()
        for question in generated_text.split("<sep>")
        if question.strip()
    ]

    # Clean question text
    cleaned_questions = []

    for question in questions:
        question = question.replace("<pad>", "").strip()

        if not question.endswith("?"):
            question += "?"

        if question not in cleaned_questions:
            cleaned_questions.append(question)

    return cleaned_questions[:max_questions]


if __name__ == "__main__":
    sample_text = """
    Wind turbines convert the kinetic energy of wind into
    mechanical power. A generator converts this mechanical
    energy into electricity. The Betz limit states that the
    maximum theoretical fraction of wind power that a turbine
    can extract is approximately 59 percent.
    """

    results = generate_questions(sample_text)

    print("\nGenerated Questions:")

    for number, question in enumerate(results, start=1):
        print(f"{number}. {question}")
