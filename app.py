import time

import streamlit as st

from utils.extract_text import extract_text_from_pdf
from utils.clause_utils import split_into_clauses, classify_clause
from utils.clause_glossary import load_glossary, generate_summary

if "contract_text" not in st.session_state:
    st.session_state["contract_text"] = ""

if "pause_classification" not in st.session_state:
    st.session_state["pause_classification"] = False

if "current_clause_index" not in st.session_state:
    st.session_state["current_clause_index"] = 0

if "classified_clauses" not in st.session_state:
    st.session_state["classified_clauses"] = []

if "summary" not in st.session_state:
    st.session_state["summary"] = ""

st.title("AutoLegal - Your Legal AI Assistant")
tab1, tab2, tab3 = st.tabs(["📄 Contract Analyzer", "📘 Legal Glossary", "📑 Summary"])

with tab1:
    uploaded_file = st.file_uploader("Upload Contract for detection", type = ["pdf"])
    if uploaded_file:
        contract_text = extract_text_from_pdf(uploaded_file)
        st.session_state["contract_text"] = contract_text
        clauses = split_into_clauses(st.session_state["contract_text"])

        
        st.title("🧠 AutoLegal Contract Analyzer")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Pause Clause Detection"):
                st.session_state["pause_classification"] = True

        with col2:
            if st.button("Resume Clause Detection"):
                st.session_state["pause_classification"] = False

        st.subheader("Detected Clauses")
        for clause, clause_type in st.session_state["classified_clauses"]:
                st.markdown(f"**Clause:** {clause} \n\n **Type of clause:** *{clause_type}*")
            
        idx = st.session_state["current_clause_index"]
        if idx < len(clauses) and not st.session_state["pause_classification"]:
            with st.spinner("Detecting legal clauses... please hold while the court is in session."):
                clause = clauses[idx]
                clause_type = classify_clause(clause)
                st.session_state["classified_clauses"].append((clause, clause_type))
                st.session_state["current_clause_index"] +=1 
                time.sleep(3)
                st.rerun()
    else:
        st.session_state["pause_classification"] = False
        st.session_state["classified_clauses"] = []
        st.session_state["current_clause_index"] = 0
        st.session_state["contract_text"] = ""
        st.session_state["summary"] = ""

    st.markdown("Please consult a Lawyer for deep understanding.")

with tab2:
    st.title("📘 Legal Glossary")
    glossary = load_glossary()

    search = st.text_input("Search legal term")
    if search:
        search_terms = {
            term: meaning for term, meaning in glossary.items() if search.lower() in term.lower()
        }
        for Sterm in search_terms:
            with st.expander(Sterm, expanded=False):
                st.markdown(f"{glossary[Sterm]}")


    st.markdown("&nbsp;")

    for term in sorted(glossary):
        with st.expander(term, expanded=False):
            st.markdown(f"{glossary[term]}")

    st.markdown("Please consult a Lawyer for deep understanding.")


with tab3:
    st.subheader("📑 Contract Summary")
    if st.session_state["contract_text"] == "":
        st.info("Upload a contract to generate summary.")

    else:
        if st.button("Generate Summary"):
            with st.spinner("Summarizing contract..."):
                st.session_state["pause_classification"] = True
                summary = generate_summary(contract_text)
                st.session_state["pause_classification"] = False
                st.session_state["summary"] = summary

        st.write(st.session_state["summary"])

    st.markdown("Please consult a Lawyer for deep understanding.")
