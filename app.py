import streamlit as st
from doc_writer import generate_ai_response, write_to_google_doc

st.set_page_config(page_title="📝 Gemini AI Doc Writer", page_icon="🧠")

st.title("📝 Gemini AI Google Doc Writer")
st.markdown("Use this tool to generate and type AI content into a Google Doc in real time.")

prompt = st.text_area("Enter your prompt:", height=200)

typing_speed = st.slider("Typing delay (seconds)", 0.1, 2.0, 1.0, 0.1)

if st.button("Generate and Write to Google Doc"):
    with st.spinner("Working..."):
        try:
            response = generate_ai_response(prompt)
            write_to_google_doc(response, typing_delay=typing_speed)
            st.success("✅ Text added to Google Doc!")
        except Exception as e:
            st.error(f"❌ Error: {e}")
