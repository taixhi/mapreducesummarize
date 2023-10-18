# Standard Library Imports
import os
import uuid

# Third-Party Imports
import openai
import streamlit as st

# Langchain Imports
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI

# Helper Functions
def save_pdf_to_disk(pdf_file):
    # Create a unique folder name
    folder_name = str(uuid.uuid4())
    os.makedirs(folder_name, exist_ok=True)
    
    # Define the path to save the PDF file
    pdf_path = os.path.join(folder_name, 'document.pdf')
    
    # Write the PDF file to disk
    with open(pdf_path, 'wb') as file:
        file.write(pdf_file.read())
    
    return pdf_path
def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

st.title("PDF Summarizer")

# Get the PDF file from the user
pdf_file = st.file_uploader("Choose a PDF file", type="pdf")

# Check if a file was uploaded
if pdf_file is not None:
    # Save the PDF file to disk
    saved_pdf_path = save_pdf_to_disk(pdf_file)

    st.write("Loading and splitting PDF...")
    # Load the PDF file
    loader = PyPDFLoader(saved_pdf_path)
    docs = loader.load_and_split(
        CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=12000, 
            chunk_overlap=0
            ))
    for doc in docs:
        st.write(doc.page_content)
    
    st.write("Loading and running LLM...")
    # Initialize the LLM
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")

    # Map
    map_template = """The following is a set of documents
    {docs}
    Based on this list of docs, please identify the main themes 
    Helpful Answer:"""
    map_prompt = PromptTemplate.from_template(map_template)
    map_chain = LLMChain(llm=llm, prompt=map_prompt, verbose=True)

    # Reduce
    reduce_template = """The following is set of summaries:
    {doc_summaries}
    Take these and distill it into a final, consolidated summary of the main themes. 
    Helpful Answer:"""
    reduce_prompt = PromptTemplate.from_template(reduce_template)

    # Run chain
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt, verbose=True)

    # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain, document_variable_name="doc_summaries"
    )

    # Combines and iteravely reduces the mapped documents
    reduce_documents_chain = ReduceDocumentsChain(
        # This is final chain that is called.
        combine_documents_chain=combine_documents_chain,
        # If documents exceed context for `StuffDocumentsChain`
        collapse_documents_chain=combine_documents_chain,
        # The maximum number of tokens to group documents into.
        token_max=16000,
        verbose=True,
    )

    # Combining documents by mapping a chain over them, then combining results
    map_reduce_chain = MapReduceDocumentsChain(
        # Map chain
        llm_chain=map_chain,
        # Reduce chain
        reduce_documents_chain=reduce_documents_chain,
        # The variable name in the llm_chain to put the documents in
        document_variable_name="docs",
        # Return the results of the map steps in the output
        return_intermediate_steps=False,
        # Print out the results of the map steps
        verbose=True,
    )

    # Summarize
    st.write(map_reduce_chain.run(docs))
