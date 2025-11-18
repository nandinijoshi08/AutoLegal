import re
from google import genai


def split_into_clauses(text: str) -> list:
    text = re.sub(r'\n+', '\n', text) #replaces multiple line breaks with a single one (\n+ to \n)
    text = text.replace('\n', ' ') #flatten to one line

    patterns = [
            r'(?<!\w)([0-9]{1,2}\.)(?=\s)', #numbered pattern - Matches "1.", "2.", etc.
            r'(?<!\w)(\([a-zA-Z]\))(?=\s)', #lettered pattern - Matches "(a)", "(B)", etc.
            r'(?<!\w)((?:[A-Z][A-Z ]{2,}))(?!\w)' #caps heading pattern - Matches all caps like "TERMINATION"
    ]

    for pattern in patterns:
        text = re.sub(pattern, r'\n\1', text)
        
    chunks = [clause.strip() for clause in text.split('\n') if len(clause.strip()) > 30]

    return chunks


def classify_clause(clause_text: str) -> str:
    client = genai.Client(api_key = "your_gemini_api_key")
    prompt = f"You are a legal assistant. Your task is to identify the type of legal clause provided.\n Please respond with only the clause type, such as 'Confidentiality Clause' or 'Indemnity Clause'.\n\n Clause: {clause_text}."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents= {prompt}
        )
        return response.text
    except Exception as e:
        if "429" in str(e):
            return "Rate limit reached. Please wait a few minutes."
        return f" Error: {str(e)}"
