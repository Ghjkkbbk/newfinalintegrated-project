from flask import Flask, request, jsonify, render_template
import os
from groq import Groq

from pdf_utils import process_pdf, search_pdf
from agent import research_agent

# 🔑 Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🌐 Home
@app.route("/")
def home():
    return render_template("index.html")


# 📄 Upload PDF
@app.route("/upload", methods=["POST"])
def upload_pdf():
    try:
        if "file" not in request.files:
            return jsonify({"message": "No file uploaded"})

        file = request.files["file"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        msg = process_pdf(filepath)

        return jsonify({"message": msg})

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})


# 🤖 LLM Call (COMMON)
def generate_answer(prompt):
    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": prompt}
    ]
)

    return response.choices[0].message.content


# 📄 Document Mode
def ask_document(query):
    pdf_data = search_pdf(query)

    if not pdf_data:
        return "❌ Answer not found in document."

    prompt = f"""
Answer ONLY using this document data:

{pdf_data}

Question: {query}

Give short answer.
"""

    return generate_answer(prompt)


# ⚡ Hybrid Mode
def hybrid_answer(query):
    doc = search_pdf(query)
    research = research_agent(query)

    prompt = f"""
Combine both intelligently.

Document:
{doc}

Research:
{research}

Give final clear answer.
"""

    final = generate_answer(prompt)

    return f"""
📄 From Documents:
{doc if doc else "Not found"}

🌐 From Research:
{research}

⚡ Final Answer:
{final}
"""


# 💬 MAIN CHAT API (FINAL)
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        query = data.get("message", "")
        mode = data.get("mode", "chat")

        # 💬 Chat Mode
        if mode == "chat":
            return jsonify({"response": generate_answer(query)})

        # 📄 Document Mode
        elif mode == "doc":
            return jsonify({"response": ask_document(query)})

        # 🌐 Research Mode
        elif mode == "research":
            return jsonify({"response": research_agent(query)})

        # ⚡ Hybrid Mode
        elif mode == "hybrid":
            return jsonify({"response": hybrid_answer(query)})

        else:
            return jsonify({"response": "Invalid mode"})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})


# ▶️ Run
if __name__ == "__main__":
    app.run(debug=True)