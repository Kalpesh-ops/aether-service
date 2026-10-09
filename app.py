import os
from flask import Flask, jsonify, request
import vertexai
from vertexai.generative_models import GenerativeModel

app = Flask(__name__)
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

# Initialize Vertex AI with the newer model
vertexai.init(project=project_id, location="us-central1")
model = GenerativeModel("gemini-2.5-flash")

@app.route("/", methods=["GET"])
def index():
    return """<!DOCTYPE html><html><head><script src="https://cdn.tailwindcss.com"></script></head><body class="bg-slate-50 flex items-center justify-center min-h-screen p-4"><div class="bg-white p-8 rounded-xl shadow-lg w-full max-w-2xl"><h1 class="text-3xl font-bold mb-2">Aether Agent</h1><p class="text-slate-500 mb-6">Enter text below to have the Gemini AI summarize it.</p><textarea id="txt" class="w-full h-40 border border-slate-300 p-3 rounded-lg mb-4 text-slate-700" placeholder="Paste a long article or text here..."></textarea><button onclick="run()" id="btn" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold p-3 rounded-lg w-full mb-6 transition-colors">Summarize Text</button><div class="bg-blue-50 border border-blue-100 p-4 rounded-lg"><h3 class="text-xs font-bold text-blue-800 uppercase tracking-wider mb-2">Agent Summary</h3><div id="out" class="text-blue-900 text-sm">Waiting for input...</div></div></div><script>async function run(){const b=document.getElementById('btn');b.innerText='Summarizing...';try{const r=await fetch('/api/summarize',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:document.getElementById('txt').value})});const d=await r.json();document.getElementById('out').innerText=d.summary || d.error;}catch(e){document.getElementById('out').innerText='Error connecting to backend.';}b.innerText='Summarize Text';}</script></body></html>"""

@app.route("/api/summarize", methods=["POST"])
def summarize():
    try:
        text = request.json.get("text", "")
        if not text:
            return jsonify({"summary": "Please provide some text to summarize."})
        
        prompt = f"Provide a concise, highly accurate summary of the following text:\n\n{text}"
        response = model.generate_content(prompt)
        return jsonify({"summary": response.text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
