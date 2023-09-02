import streamlit as st
import os
from os import listdir
from os.path import isfile, join

from ingest import ingestPrivateGPT


st.title("Karsa Knowledge Base")

uploaded_file = st.file_uploader("Upload your txt file", type=['txt'])
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type} 

    with open(os.path.join("source_documents", uploaded_file.name),"wb") as f: 
        f.write(uploaded_file.getbuffer())
    
    with st.status("Running..."):
        ingestPrivateGPT()
        st.success("Saved File")



onlyfiles = [f for f in listdir("source_documents") if isfile(join("source_documents", f))]
for file in onlyfiles:
    with open(os.path.join("source_documents", file),"r") as f: 
        st.text(file)
