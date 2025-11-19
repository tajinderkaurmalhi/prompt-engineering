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


# 📄 Extract and format text from one PDF file
def extract_text_from_pdf(path):
    doc = fitz.open(path)
    raw_text = "\n".join(page.get_text() for page in doc)
    # Add paragraph breaks after sentence endings
    formatted = re.sub(r"(?<=[.?!])\s+", "\n\n", raw_text)
    return formatted.strip()


# 🔗 Chunk into word-based segments
def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return [textwrap.fill(chunk, width=100) for chunk in chunks]  # Wrap each chunk


# 🧠 Dummy embedding function
def dummy_embed(text):
    return np.array(
        [hash(w) % 1000 / 1000.0 for w in text.split()[:300]] +
        [0.0] * max(0, 300 - len(text.split()))
    )


# 🧱 Build FAISS index from all chunks
def build_faiss_index(all_chunks):
    vectors = [dummy_embed(c["text"]) for c in all_chunks]
    dim = len(vectors[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(vectors).astype('float32'))
    return index


# 🔍 Retrieve top-k relevant chunks
def retrieve_chunks(query, all_chunks, index, k=4):
    query_vector = np.array([dummy_embed(query)]).astype('float32')
    _, I = index.search(query_vector, k)
    return [all_chunks[i] for i in I[0]]


# 💬 Ask Gemini using retrieved chunks
def ask_gemini(query, retrieved_chunks):
    context = "\n\n".join(f"[{chunk['source']}] {chunk['text']}" for chunk in retrieved_chunks)
    prompt = (
        f"You are an assistant answering based on the following documents.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\nAnswer:"
    )
    response = model.generate_content(prompt)
    wrapped_answer = textwrap.fill(response.text.strip(), width=100)
    return wrapped_answer


# === MAIN FLOW ===
if __name__ == "__main__":
    # Select multiple PDF files
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])

    if not file_paths:
        print("❌ No files selected. Exiting.")
        exit()

    all_chunks = []

    print("\n📂 Processing selected PDF files...")
    for path in file_paths:
        filename = path.split("/")[-1]
        print(f"📄 Reading: {filename}")
        text = extract_text_from_pdf(path)
        chunks = chunk_text(text)
        for chunk in chunks:
            all_chunks.append({"text": chunk, "source": filename})

    print("🔗 Building combined FAISS index...")
    index = build_faiss_index(all_chunks)

    # ✅ Preview first few chunks as clean paragraphs
    print("\n📚 Preview of Combined Context (first 3 chunks):\n" + "-" * 80)
    for i, c in enumerate(all_chunks[:3]):
        print(f"\n🔹 From {c['source']}:\n{textwrap.fill(c['text'], width=100)}\n")

    # Q&A loop
    while True:
        query = input("\n🧠 Ask a question (or type 'exit' to quit): ")
        if query.strip().lower() == "exit":
            print("\n👋 Goodbye! Thanks for using Multi-PDF Chat with Gemini.")
            break
        retrieved = retrieve_chunks(query, all_chunks, index)
        answer = ask_gemini(query, retrieved)
        print("\n💬 Gemini Answer:\n" + "-" * 80)
        print(answer)