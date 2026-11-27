# RAG Assistant

A question-answering assistant that answers from your own documents using retrieval-augmented generation (RAG).
The demo uses the German road traffic regulations (StVO): ask in German or English, and it finds the relevant paragraphs.

## How it works

1. Load documents (PDFs) and split them into chunks
2. Turn the chunks into embeddings and store them in a vector database (Qdrant)
3. For each question, find the most relevant chunks
4. Send the question and those chunks to an LLM, which answers only from them

## Tech stack

- Python
- LangChain
- Groq (hosted Llama and open-source models)
- Multilingual embeddings: intfloat/multilingual-e5-small (sentence-transformers)
- Qdrant (local mode)
- FastAPI and Streamlit (planned)

## Sample data

`sample_data/StVO.pdf`: Straßenverkehrs-Ordnung (StVO), Bundesministerium der Justiz, https://www.gesetze-im-internet.de. Official work under §5 UrhG.

## Run it

```bash
python -m venv .venv
.venv\Scripts\activate          # on Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project folder:

```
GROQ_API_KEY=your_key_here
```

Build the vector index once (downloads the embedding model on first run):

```bash
python build_index.py
```

Then search the StVO in German or English:

```bash
python search.py
```

## Roadmap

Done:
- First LLM call with LangChain and Groq
- Load and chunk PDF documents
- Embeddings and vector search with Qdrant
- Answer questions from retrieved context

Next:
- Evaluation of answer quality
- REST API with FastAPI and a Streamlit demo
