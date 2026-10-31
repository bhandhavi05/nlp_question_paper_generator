# PaperCraft AI

PaperCraft AI is a Streamlit app that turns textbook PDFs into study material. It extracts selectable text from a PDF, then lets you generate summaries, extract keyphrases, create practice questions, and assemble a question paper for download.

## Features

- Upload a text-based PDF and view its page count and extracted content.
- Split document text into segments for processing.
- Generate and download summaries.
- Extract and download important keyphrases.
- Generate practice questions and download them.
- Preview a question paper with a subject, exam title, duration, marks, and instructions, then download it.

## Requirements

- Python 3.10 or newer
- The packages listed in [`requirements.txt`](requirements.txt)
- An internet connection the first time models are used, so Hugging Face model files can be downloaded

## Setup

From the project directory, create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the app

```bash
streamlit run app.py
```

Streamlit will print a local URL to open in your browser. Upload a PDF with selectable text, then use the tabs to create summaries, keyphrases, and questions. Generated questions can be customized and exported from the Question Paper Studio tab.

## Models and first run

The app loads these pretrained Hugging Face models when their features are first used:

- `sshleifer/distilbart-cnn-12-6` for summarization
- `all-MiniLM-L6-v2` through KeyBERT for keyphrase extraction
- `valhalla/t5-small-e2e-qg` for question generation

Model downloads can take time and need disk space. Processing runs locally after the models are downloaded; performance depends on your available memory and hardware.

NLTK tokenizer resources are requested by the preprocessing module when the app starts. PDFs that contain only scanned images do not provide selectable text and need OCR before they can be processed by this app.

## Project layout

```text
.
├── app.py
├── requirements.txt
└── modules/
    ├── keyphrase_extractor.py
    ├── preprocessing.py
    ├── question_generator.py
    ├── summarizer.py
    └── text_chunker.py
```
