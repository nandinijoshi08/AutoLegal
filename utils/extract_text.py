import pdfplumber

# to extract text from the uploaded contract
def extract_text_from_pdf(file):
    if file:
        with pdfplumber.open(file) as pdf:
            all_text = ""
            for page in pdf.pages:
                all_text += page.extract_text() + "\n\n" 
        return all_text 
    else:
        return "Please provide the file"
