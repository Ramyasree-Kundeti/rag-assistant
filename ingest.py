import re
from bisect import bisect_right
from pathlib import Path
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

#Load one document per PDF page
PDF_PATH = Path(__file__).parent/"sample_data"/"StVO.pdf"

# remove the header lines, page numbers repeated on every page
HEADER_PATTERNS =[
    re.compile(r"Ein Service des Bundesministerium"),
    re.compile(r"Bundesamts für Justiz"),
    re.compile(r"^-\s*Seite \d+ von \d+\s*-$")
]

# Take line that starts a new paragraph, e.g. "§ 8 Vorfahrt" or "Anlage 2 ..."
# (?!Abs) skips references like "§ 8 Absatz 1" inside the text
SECTION_START = re.compile(
    r"^(§\s*\d+[a-z]?\s+(?!Abs)[A-ZÄÖÜ].*|Anlage\s+\d+.*)$",
    re.MULTILINE,
)

def load_chunks(pdf_path=PDF_PATH, chunk_size=500, overlap=50):
    """Old method (baseline): fixed-size chunks, page by page."""
    reader = PdfReader(pdf_path)
    docs = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        docs.append(Document(page_content=text,
                             metadata={"source": str(pdf_path.name), "page": i + 1}))
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_documents(docs)

def _clean(text):
    """Remover header/footer lines from a page"""
    kept =[]
    for line in text.splitlines():
        line = line.replace("\xa0", " ").strip() # remove whitespaces
        if any(p.search(line) for p in HEADER_PATTERNS):
            continue
        kept.append(line)
    return "\n".join(kept)

def load_chunks_by_paragraph(pdf_path=PDF_PATH,max_size=1200,overlap=100):
    """New method one chunk per § (paragraph). Long paragraphs are split further."""
    reader = PdfReader(pdf_path)

    # join all pages into one text and also remember where each page starts
    full_text = ""
    page_starts = []
    for page in reader.pages:
        page_starts.append(len(full_text))
        full_text += _clean(page.extract_text() or "")+"\n"

    # Find where each § starts
    starts = [m.start() for m in SECTION_START.finditer(full_text)]
    starts.append(len(full_text)) # end of last section

    splitter = RecursiveCharacterTextSplitter(chunk_size=max_size,chunk_overlap=overlap)
    chunks = []

    #One section = text from one § start to the next

    for start,end in zip(starts[:-1],starts[1:]):
        section_text = full_text[start:end].strip()
        heading = section_text.splitlines()[0]
        metadata = {
            "source":str(pdf_path.name),
            "page":bisect_right(page_starts,start), # page where the § begins
            "section": heading[:80],
            }
        if len(section_text) <= max_size:
            chunks.append(Document(page_content=section_text, metadata=metadata))
        else:
            # Long section: split it, and put the heading in front of every part
            for j, part in enumerate(splitter.split_text(section_text)):
                text = part if j == 0 else f"{heading}\n{part}"
                chunks.append(Document(page_content=text, metadata=metadata))
    return chunks



if __name__ == "__main__":
    chunks = load_chunks_by_paragraph()
    print(f"Number of chunks: {len(chunks)}")
    print()
    for c in chunks:
        if c.metadata["section"].startswith("§ 8 "):
            print(c.metadata)
            print(c.page_content[:400])
            print("-" * 60)









