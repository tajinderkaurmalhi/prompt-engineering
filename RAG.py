import fitz  # PyMuPDF
import google.generativeai as genai
import faiss
import numpy as np
import tkinter as tk
from tkinter import filedialog
import textwrap
import re

# 🔐 Gemini API key
API_KEY = "AIzaSyCAeQD2Z5B3cI-_c30m3KFUAzpbrxCKRS0"

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Extract text from PDF
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    raw_text = "\n".join(page.get_text() for page in doc)
    # Force paragraphs on sentence endings
    formatted = re.sub(r"(?<=[.?!])\s+", "\n\n", raw_text)
    return formatted.strip()

# Chunk text into word groups
def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return [textwrap.fill(chunk, width=100) for chunk in chunks]  # Wrap lines

# Dummy embed function
def dummy_embed(text):
    return np.array(
        [hash(w) % 1000 / 1000.0 for w in text.split()[:300]] +
        [0.0] * max(0, 300 - len(text.split()))
    )

# Build FAISS index
def build_faiss_index(chunks):
    vectors = [dummy_embed(c) for c in chunks]
    dim = len(vectors[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(vectors).astype('float32'))
    return index

# Retrieve top-k relevant chunks
def retrieve_chunks(query, chunks, index, k=3):
    query_vector = np.array([dummy_embed(query)]).astype('float32')
    _, I = index.search(query_vector, k)
    return [chunks[i] for i in I[0]]

# Ask Gemini using retrieved chunks
def ask_gemini(query, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = (
        f"You are an assistant answering based on the following document content.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\nAnswer:"
    )
    response = model.generate_content(prompt)
    return response.text.strip()

# === MAIN FLOW ===
if __name__ == "__main__":
    # File picker
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

    if not file_path:
        print("❌ No file selected. Exiting.")
        exit()

    print(f"\n📄 Selected File: {file_path}")
    print("📤 Extracting and formatting text...")
    full_text = extract_text_from_pdf(file_path)

    print("🔗 Chunking and indexing the document...")
    chunks = chunk_text(full_text)
    index = build_faiss_index(chunks)

    # Display all chunks as properly wrapped paragraphs
    print("\n📚 Full Document Context (in Paragraphs):\n" + "-" * 80)
    print("\n\n".join(chunks[:5]))  # You can increase if needed

    # Q&A loop
    while True:
        query = input("\n🧠 Ask a question (or type 'exit' to quit): ")
        if query.strip().lower() == "exit":
            print("\n👋 Goodbye! Thanks for using PDF Chat with Gemini.")
            break
        relevant_chunks = retrieve_chunks(query, chunks, index)
        answer = ask_gemini(query, relevant_chunks)
        print("\n💬 Gemini Answer:\n" + "-" * 80)
        print(answer)