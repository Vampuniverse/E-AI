import streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. Setup the AI "Brain"
# Get your key from: https://aistudio.google.com/
genai.configure(api_key="AIzaSyApJcDbeEyNVFOGFOWJz7XxsZ798SlfBI8")
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Ethio-AI Master", page_icon="🇪🇹")
st.title("🇪🇹 Ethio-AI: Heritage & Humanitarian Portal")

# Sidebar for choosing the mode
mode = st.sidebar.selectbox("Choose Mode", ["📊 Statistics & Solutions", "📜 Ancient Ge'ez Translator"])

# --- MODE 1: HUMANITARIAN SOLUTIONS ---
if mode == "📊 Statistics & Solutions":
    st.header("Humanitarian Data Analyst")
    uploaded_file = st.file_uploader("Upload Stats (CSV or Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:", df.head())
        
        user_ask = st.text_input("Ask a question about these stats (Amharic/Tigrigna/English):")
        if user_ask:
            prompt = f"Data: {df.to_string()} \nQuestion: {user_ask} \nAssistant: Analyze these stats and suggest 3 practical humanitarian solutions."
            response = model.generate_content(prompt)
            st.markdown("### 🤖 Analysis & Solutions")
            st.write(response.text)

# --- MODE 2: GE'EZ TRANSLATOR ---
else:
    st.header("Ancient Ge'ez Transcript Decoder")
    transcript = st.text_area("Paste Ancient Transcript Text:", height=200)
    target = st.radio("Translate to:", ["Amharic (አማርኛ)", "Tigrigna (ትግርኛ)"])
    
    if st.button("Translate & Explain Context"):
        translate_prompt = f"""
        Act as a Professor of Ge'ez. 
        Translate this text into modern {target}.
        Provide:
        1. Literal Translation.
        2. Spiritual/Historical meaning.
        3. Explain any archaic Fidel characters used.
        Text: {transcript}
        """
        result = model.generate_content(translate_prompt)
        st.markdown("### 🕊️ Decoded Meaning")
        st.write(result.text)
