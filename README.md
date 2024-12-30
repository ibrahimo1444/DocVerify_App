# DocVerify_App
DocVerify ensures document authenticity by comparing them to original versions using advanced OCR and text similarity algorithms. It extracts text from images and PDFs, identifies discrepancies accurately, and provides a user-friendly interface with detailed comparison results to detect potential forgeries.

## Key Components

* Streamlit: Provides a user-friendly interface for uploading and comparing documents.

* OpenCV: Used for image processing to enhance the quality of the documents before text extraction.

* Tesseract OCR: A powerful OCR engine for extracting text from images.

* Scikit-Learn: Utilized for advanced text comparison using TF-IDF Vectorizer and Cosine Similarity.

## How It Works

1. Upload Documents: Users upload the original document and the document to compare.<br/>
2. Text Extraction: The app uses Tesseract OCR to extract text from both documents.<br/>
3. Text Comparison: Extracted texts are compared using TF-IDF and Cosine Similarity to provide a similarity score.<br/>
4. Results and Feedback: The app displays the extracted texts, similarity score, and additional feedback on the potential discrepancies.

## Use Cases

* Legal Document Verification: Ensure that contracts, agreements, and other legal documents have not been altered.<br/>
* Academic Integrity: Check for authenticity of certificates and transcripts.<br/>
* Business Compliance: Verify the originality of business documents such as invoices and receipts.<br/>

The Document Verifier App is a practical tool for anyone needing to verify the authenticity and integrity of important documents quickly and accurately.
