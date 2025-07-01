# app/interface.py

import streamlit as st
from app.search_engine import search_query

st.set_page_config(page_title="Diagnostic Navigator", layout="wide")

st.title("🧠 Diagnostic Navigator")
st.markdown("Ask anything about your uploaded PDF.")

# Query box
query = st.text_input("Ask a question", placeholder="E.g., What is serial 23 used for?")

if query:
    with st.spinner("Thinking..."):
        result = search_query(query)
        st.markdown(f"### 📝 Answer (Page {result['page']}):")
        st.write(result["text"])

        if result.get("images"):
            if st.button("🔍 View Related Visual Flowchart"):
                for img in result["images"]:
                    st.image(f"data/images/{img}", caption=img, use_column_width=True)
