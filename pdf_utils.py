from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# 🌍 Global vector store
vector_store = None


# 📄 Process PDF (Create Vector DB)
def process_pdf(file_path):
    global vector_store

    try:
        reader = PdfReader(file_path)
        text = ""

        # Extract text
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

        if not text.strip():
            return "❌ PDF has no readable text!"

        # Split text into chunks
        splitter = CharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = splitter.split_text(text)

        # Load embedding model
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Create FAISS vector DB
        vector_store = FAISS.from_texts(chunks, embeddings)

        return "✅ PDF processed successfully! You can now ask questions."

    except Exception as e:
        return f"❌ Error processing PDF: {str(e)}"


# 🔍 Search inside PDF
def search_pdf(query):
    global vector_store

    try:
        if vector_store:
            docs = vector_store.similarity_search(query, k=3)
            return " ".join([doc.page_content for doc in docs])

        return None

    except Exception as e:
        return None


# 📄 (Optional Utility) Extract full text (NOT used in main flow)
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""

        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"

        return text

    except:
        return ""