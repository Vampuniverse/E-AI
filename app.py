import streamlit as st
import google.generativeai as genai
import pandas as pd

# 1. SETUP PAGE CONFIG (Must be at the very top of Streamlit commands)
st.set_page_config(page_title="Ethio-AI Master", page_icon="🇪🇹")

# 2. CHOOSE LANGUAGE (Sidebar)
st.sidebar.title("Configuration")
language = st.sidebar.radio("Select Language / ቋንቋ ይምረጡ", ["Amharic", "Tigrigna"])

# 3. THE SAFETY GATE (Check for Key)
# Make sure you have added GOOGLE_API_KEY in Streamlit Cloud Settings > Secrets
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ API Key is missing! Go to Streamlit Settings > Secrets and add 'GOOGLE_API_KEY'.")
    st.stop() 

# 4. CONFIGURE AI BRAIN
# We use the key from secrets, NOT the hardcoded "AIza..." string
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Use the dynamic choice in instructions
instruction = f"Respond ONLY in {language} using the correct Fidel script. Maintain a professional tone."

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=instruction
)

# 5. MAIN INTERFACE
st.title("🇪🇹 Ethio-AI: Heritage & Humanitarian Portal")
mode = st.sidebar.selectbox("Choose Mode", ["📊 Statistics & Solutions", "📜 Ancient Ge'ez Translator"])

# --- MODE 1: HUMANITARIAN SOLUTIONS ---
if mode == "📊 Statistics & Solutions":
    st.header("Humanitarian Data Analyst")
    uploaded_file = st.file_uploader("Upload Stats (CSV or Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        # Check if it's CSV or Excel
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.write("Data Preview:", df.head())
        
        user_ask = st.text_input("Ask a question about these stats:")
        if user_ask:
            # We tell the AI to look at the data and the user question
            prompt = f"Data: {df.to_string()} \nQuestion: {user_ask}"
            response = model.generate_content(prompt)
            st.markdown("### 🤖 Analysis & Solutions")
            st.write(response.text)

# --- MODE 2: GE'EZ TRANSLATOR ---
else:
    st.header("Ancient Ge'ez Transcript Decoder")
    transcript = st.text_area("Paste Ancient Transcript Text:", height=200)
    
    if st.button("Translate & Explain Context"):
        translate_prompt = f"Translate this Ge'ez text into modern {language} and explain its historical context: {transcript}"
        result = model.generate_content(translate_prompt)
        st.markdown("### 🕊️ Decoded Meaning")
        st.write(result.text)
