import streamlit as st
import cv2
import pytesseract
import numpy as np
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz  # PyMuPDF

# Set the path for Tesseract OCR (adjust this according to your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.title("Document Verifier App")

# Upload the original document
st.header("Upload the Original Document")
original_file = st.file_uploader("Choose the original document", type=["png", "jpg", "jpeg", "pdf"])

# Upload the document to compare
st.header("Upload the Document to Compare")
compare_file = st.file_uploader("Choose the document to compare", type=["png", "jpg", "jpeg", "pdf"])

def extract_text(image):
    try:
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding if necessary
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Use Tesseract to extract text
        text = pytesseract.image_to_string(binary)
        return text
    except pytesseract.TesseractNotFoundError:
        st.error("Tesseract is not installed or not found. Please install Tesseract OCR and ensure it's in your PATH.")
        return ""
    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return ""

def pdf_to_images(pdf_file):
    try:
        document = fitz.open(stream=pdf_file.read(), filetype="pdf")
        images = []
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(np.array(img))
        return images
    except Exception as e:
        st.error(f"Error converting PDF to images: {e}")
        return []

def compare_texts(text1, text2):
    try:
        # Use TF-IDF Vectorizer and Cosine Similarity for comparison
        vectorizer = TfidfVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()
        cosine_sim = cosine_similarity(vectors)
        similarity_score = cosine_sim[0, 1]

        return f"The similarity score between the documents is: {similarity_score:.2f}", similarity_score
    except Exception as e:
        st.error(f"Error comparing texts: {e}")
        return "Error in comparison", 0.0

if original_file and compare_file:
    try:
        if original_file.type == "application/pdf":
            original_images = pdf_to_images(original_file)
        else:
            original_images = [np.array(Image.open(original_file))]

        if compare_file.type == "application/pdf":
            compare_images = pdf_to_images(compare_file)
        else:
            compare_images = [np.array(Image.open(compare_file))]

        st.write("Processing documents...")

        # Extract text from the images
        original_texts = [extract_text(img) for img in original_images]
        compared_texts = [extract_text(img) for img in compare_images]

        original_text = " ".join(original_texts)
        compared_text = " ".join(compared_texts)

        if original_text and compared_text:
            st.subheader("Extracted Text from Original Document")
            st.text_area("Original Text", original_text, height=200)

            st.subheader("Extracted Text from Document to Compare")
            st.text_area("Compare Text", compared_text, height=200)

            # Compare texts
            comparison_result, similarity_score = compare_texts(original_text, compared_text)
            st.subheader("Comparison Result")
            st.write(comparison_result)

            # Add more detailed analysis if needed
            if similarity_score < 0.8:
                st.warning("The documents show low similarity. There might be significant differences.")
            else:
                st.success("The documents are highly similar.")
        else:
            st.error("Could not extract text from one or both documents. Please ensure the images are clear and text is legible.")

    except Exception as e:
        st.error(f"An error occurred while processing the documents: {e}")
else:
    st.info("Please upload both the original document and the document to compare.")
