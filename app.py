import os
import re
import json
import pickle
import string
import numpy as np
import pandas as pd 
import tensorflow as tf
from scipy.sparse import load_npz
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, jsonify, render_template

# --- 1. INISIALISASI & MEMUAT ARTEFAK ---
app = Flask(__name__)

# Tentukan path ke folder artefak
ARTIFACT_DIR = 'artifacts'

# Muat model
model = tf.keras.models.load_model(os.path.join(ARTIFACT_DIR, "pln_intent_bilstm.h5"))

# Muat tokenizer sebagai string, bukan dictionary
with open(os.path.join(ARTIFACT_DIR, "pln_tokenizer.json"), 'r') as f:
    tokenizer_json_string = f.read()
tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_json_string)

# Muat label encoder
with open(os.path.join(ARTIFACT_DIR, "pln_intent_label_encoder.pkl"), 'rb') as f:
    le_intent = pickle.load(f)

# Muat kamus intent-jawaban
with open(os.path.join(ARTIFACT_DIR, "pln_intent2answer.json"), 'r', encoding='utf-8') as f:
    intent2answer = json.load(f)

# Muat TF-IDF vectorizer dan matrix
with open(os.path.join(ARTIFACT_DIR, "pln_tfidf.pkl"), 'rb') as f:
    tfidf = pickle.load(f)
tfidf_matrix = load_npz(os.path.join(ARTIFACT_DIR, "pln_tfidf_matrix.npz"))


# Muat dataset untuk retrieval hanya sekali saat aplikasi dimulai
df = pd.read_csv("dataset.csv")

# Konfigurasi dari notebook
MAX_LEN = 21
CONF_THRESH = 0.60
RETRIEVAL_THRESH = 0.35
DEFAULT_MSG = "Maaf, saya belum memahami pertanyaan Anda. Silakan coba dengan kalimat lain atau hubungi PLN 123."

# --- 2. FUNGSI HELPER ---
SLANG_MAP = {
    "gimana": "bagaimana", "gmn": "bagaimana",
    "ga": "tidak", "gak": "tidak", "nggak": "tidak", "ngga": "tidak",
    "klo": "kalau", "kl": "kalau",
    "dgn": "dengan", "yg": "yang", "utk": "untuk", "sdh": "sudah", "udh": "sudah",
    "bgt": "sangat", "banget": "sangat",
    "min": "admin", "bos": "admin", "bro": "admin",
    "pengen": "ingin",
    "sih": "", "deh": "", "dong": "", "ya": "", "yah": "", "nih": "", "lah": ""
}

def normalize_indonesian(text: str) -> str:
    """Normalisasi teks bahasa Indonesia: lower, hapus punctuation/digit, slang, spasi."""
    text = text.lower()
    text = re.sub(r"[%s]" % re.escape(string.punctuation), " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = []
    for w in text.split():
        if w in SLANG_MAP:
            rep = SLANG_MAP[w]
            if rep:
                tokens.append(rep)
        else:
            tokens.append(w)
    text = " ".join(tokens)
    text = re.sub(r"\s+", " ", text).strip()
    return text

## <<< PERBAIKAN 2.3: Modifikasi fungsi agar menerima 'df' sebagai argumen
def tfidf_retrieve(user_text, df, topk=1):
    q = normalize_indonesian(user_text)
    vec = tfidf.transform([q])
    sims = cosine_similarity(vec, tfidf_matrix)[0]
    
    # Dapatkan intent dari pertanyaan yang paling mirip berdasarkan indeksnya di DataFrame
    sim_indices = sims.argsort()[::-1]
    
    unique_answers = []
    seen_intents = set()
    
    # Iterasi melalui indeks yang paling mirip
    for idx in sim_indices:
        intent = df.iloc[idx]['intent']
        if intent not in seen_intents:
            # Dapatkan skor similarity dari indeks yang sama
            score = sims[idx]
            # Tambahkan jawaban dan skornya
            unique_answers.append((intent2answer[intent], score))
            seen_intents.add(intent)
            if len(unique_answers) >= topk:
                break
                
    return unique_answers

# --- 3. LOGIKA INTI CHATBOT ---
def chatbot_response(user_text):
    # 1) Intent classifier
    t = normalize_indonesian(user_text)
    seq = tokenizer.texts_to_sequences([t])
    pad = pad_sequences(seq, maxlen=MAX_LEN, padding="post")
    prob = model.predict(pad, verbose=0)[0]
    idx = int(np.argmax(prob))
    conf = float(np.max(prob))

    if conf >= CONF_THRESH:
        intent_label = le_intent.inverse_transform([idx])[0]
        return intent2answer.get(intent_label, DEFAULT_MSG)

    # 2) Retrieval fallback
    # Panggil fungsi dengan memberikan 'df'
    # Tidak perlu lagi membaca CSV di sini
    cand = tfidf_retrieve(user_text, df, topk=1) 
    if cand and cand[0][1] >= RETRIEVAL_THRESH:
        return cand[0][0]

    # 3) Default
    return DEFAULT_MSG

# --- 4. ROUTE / ENDPOINT FLASK ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_bot_response():
    user_text = request.form["msg"]
    response = chatbot_response(user_text)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)