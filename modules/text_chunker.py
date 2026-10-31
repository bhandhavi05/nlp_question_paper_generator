
def create_chunks(sentences, max_words=180):
    chunks = []
    current_chunk = []
    current_word_count = 0

    for sentence in sentences:
        word_count = len(sentence.split())

        # Keep sentences together when possible
        if current_chunk and current_word_count + word_count > max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_word_count = 0

        current_chunk.append(sentence)
        current_word_count += word_count

    # Add the remaining sentences
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


if __name__ == "__main__":
    sample_sentences = [
        "Machine Learning is a branch of Artificial Intelligence.",
        "It enables computers to learn from data.",
        "Supervised learning uses labeled training data.",
        "Unsupervised learning finds patterns in unlabeled data.",
        "Deep learning uses neural networks with multiple layers."
    ]

    chunks = create_chunks(sample_sentences, max_words=20)

    for i, chunk in enumerate(chunks, start=1):
        print(f"\nChunk {i}:")
        print(chunk)
