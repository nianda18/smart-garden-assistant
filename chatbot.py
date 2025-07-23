import streamlit as st
import google.generativeai as genai
import os

# 🔧 Konfigurasi API Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyAZ7bQA6g6dz3Zn-ZK63KZUkcELOMVZRqo"
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    available = True
except Exception as e:
    available = False
    error_message = str(e)

# ✅ Inisialisasi Session State
def init_session_state():
    defaults = {
        "chat": [
            {"role": "user", "parts": ["Kamu adalah asisten penyuluh pertanian khusus tanaman labu butternut."]}
        ],
        # "voice_input": "", # Keep commented or remove
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# 💬 UI Chatbot
def render():
    init_session_state()  # penting agar semua state aman

    st.title("💬 Chatbot Smart Garden")

    if not available:
        st.error(f"Chatbot tidak tersedia: {error_message}")
        return

    st.markdown("Tanyakan apa saja seputar budidaya labu butternut!")
    user_input = st.chat_input("Tulis pertanyaan Anda di sini...", key="chatbox_input")

    # Proses input pengguna
    if user_input: # Line 40 in your chatbot.py
        st.session_state.chat.append({"role": "user", "parts": [user_input]})
        with st.spinner("Menjawab..."):
            try:
                response = model.generate_content(st.session_state.chat)
                reply = response.text
                st.session_state.chat.append({"role": "model", "parts": [reply]})
            except Exception as e:
                reply = f"Terjadi kesalahan saat menjawab: {str(e)}"
                st.session_state.chat.append({"role": "model", "parts": [reply]})

    # 💬 Tampilkan riwayat chat
    for msg in st.session_state.chat[1:]:
        role = "👩‍🌾 Kamu" if msg["role"] == "user" else "🤖 Asisten"
        with st.chat_message(role):
            st.markdown("\n".join(msg["parts"]))