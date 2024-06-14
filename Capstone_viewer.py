import streamlit as st
import pdfplumber
import requests
import io

# Custom styles
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Function to download and return the PDF file
def download_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        return io.BytesIO(response.content)
    return None

# Function to extract pages from PDF
def extract_pages(file_stream, page_start, page_end=None):
    text = ""
    with pdfplumber.open(file_stream) as pdf:
        # If page_end is not provided, extract until the end
        if page_end is None:
            page_end = len(pdf.pages)
        pages = pdf.pages[page_start-1:page_end]  # Adjusting for zero-index
        for page in pages:
            text += page.extract_text() + "\n\n"
    return text

# Apply custom styles
local_css("style.css")

# User Interface
st.title('Capstone Project Document Viewer')

st.markdown("""
    This app allows you to view different sections of the Capstone Project on Predicting Students' Progression and Enrolment.
""")

# Define sections and their page ranges, including a section from page 77 to the end.
sections = {
    "Abstract": (2, 2),
    "Introduction": (9, 18),
    "Data Processing and Analysis": (18, 22),
    "Modeling": (37, 39),
    "Conclusion": (71, 71),
    "Code and Additional Content": (77, None)  # None implies till the end of the document
}

# PDF URL
pdf_url = 'https://github.com/AnanyaThyagarajan/Predicting-Students-Progression-and-Enrolment-using-Python/raw/main/A%20Capstone%20Project%20on%20Predicting%20Students%E2%80%99%20Progression%20and%20Enrolment%20using%20Python%20by%20Ananya%20Krithika%20Thyagarajan_massey.pdf'

# Dropdown to select the section to view
section = st.selectbox("Choose a section to view", options=list(sections.keys()), index=0)

# Button to display the section
if st.button('Show Section'):
    pdf_stream = download_pdf(pdf_url)
    if pdf_stream:
        pages = sections[section]
        extracted_text = extract_pages(pdf_stream, *pages)
        st.markdown(extracted_text)
    else:
        st.error("Failed to download PDF file.")

