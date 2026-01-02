from google import genai
import json 

# method to load glossary JSON file
def load_glossary():
    try:
        with open("utils/legal_glossary.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
 
# method to generate summary of uploaded contract
def generate_summary(contract_text):
    client = genai.Client(api_key = "your_gemini_api_key")

    prompt = f"""
    Summarize the following contract into plain English for a non-lawyer. Just return the summary.
    Focus on:
    - Main purpose of the contract
    - Responsibilities of each party
    - Payment Terms
    - Duration
    - Termination conditions
    - Any unusual or risky clauses

    Contract:
    {contract_text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= {prompt})
    return response.text
