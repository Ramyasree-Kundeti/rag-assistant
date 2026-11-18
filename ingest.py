from pathlib import Path
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

#Load one document per PDF page
pdf_path = Path(__file__).parent/"sample_data"/"StVO.pdf"
reader = PdfReader(pdf_path)
docs =[
    Document(page_content=page.extract_text() or "",
             metadata={"source":pdf_path.name,"page":i+1}) for i, page in enumerate(reader.pages)
]
print(f"Loaded {len(docs)} docs from PDF")

#split into overlapping chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"split into {len(chunks)} chunks")

#Look at first chunks
for chunk in chunks[:3]:
    print("_"*40)
    print(chunk.metadata)
    print(chunk.page_content)






