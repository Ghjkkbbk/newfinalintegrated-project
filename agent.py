import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# ✅ FIXED API KEY
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🌐 WEB SEARCH (STABLE VERSION)
def web_search(query):
    try:
        from duckduckgo_search import DDGS

        results = []
        with DDGS() as ddgs:
            data = list(ddgs.text(query, max_results=3))

            for r in data:
                results.append(r.get("title", "") + " " + r.get("body", ""))

        return " ".join(results)

    except Exception as e:
        print("❌ WEB SEARCH ERROR:", e)
        return ""


# 🤖 AI RESPONSE
def ask_llm(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ WORKING MODEL
            messages=[
                {"role": "system", "content": "You are a helpful research assistant."},
                {"role": "user", "content": prompt[:2000]}  # prevent token error
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ LLM ERROR:", e)
        return f"❌ AI Error: {str(e)}"


# 🚀 MAIN RESEARCH AGENT
def research_agent(query):
    try:
        query = query[:200]  # prevent long input

        # STEP 1: SEARCH WEB
        web_data = web_search(query)

        # 🔥 FALLBACK (IMPORTANT)
        if not web_data:
            web_data = "No web data found. Answer using general knowledge."

        # STEP 2: CREATE PROMPT
        prompt = f"""
You are an AI Research Agent.

Use the information below:

{web_data[:1200]}

Question:
{query}

Give response in this format:

🔹 Introduction  
🔹 Key Points  
🔹 Insights  
🔹 Conclusion  

Keep it clear and short.
"""

        # STEP 3: GENERATE ANSWER
        return ask_llm(prompt)

    except Exception as e:
        print("❌ RESEARCH ERROR:", e)
        return f"❌ Error: {str(e)}"