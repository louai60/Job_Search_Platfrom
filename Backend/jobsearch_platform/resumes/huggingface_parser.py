import requests
import logging
import re
from django.conf import settings

# Initialize logger
logger = logging.getLogger(__name__)

# HuggingFace API URL and Token
HF_API_URL = "https://api-inference.huggingface.co/models/dbmdz/bert-large-cased-finetuned-conll03-english"
HF_API_TOKEN = settings.HUGGINGFACE_API_TOKEN  

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

def preprocess_resume(text):
    """Preprocess resume to remove noise like emails and links."""
    text = re.sub(r'\S+@\S+', '', text)  # Remove emails
    text = re.sub(r'http[s]?://\S+', '', text)  # Remove URLs
    text = re.sub(r'[|]', '', text)  # Remove unnecessary symbols like '|'
    return text.strip()

def get_entities_from_api(resume_text):
    """Calls HuggingFace API for NER and returns the result."""
    try:
        response = requests.post(
            HF_API_URL, 
            headers=headers,
            json={"inputs": resume_text}
        )

        if response.status_code == 200:
            logger.debug(f"NER API Response: {response.json()}")
            return response.json()
        else:
            logger.error(f"Error calling HuggingFace API: {response.status_code}, {response.text}")
            return {"error": f"Failed to process resume: {response.text}"}
    except Exception as e:
        logger.error(f"Error during HuggingFace API request: {str(e)}")
        return {"error": str(e)}

def clean_and_group_entities(entities):
    """Clean and merge subword fragments from NER results."""
    combined_entities = []
    current_entity = ""

    for entity in entities:
        word = entity.get("word", "").replace("##", "")  # Remove subword indicators
        if word:  # Skip empty words
            if current_entity:  # Merge words if needed
                current_entity += f" {word}"
            else:
                current_entity = word

        if entity.get("entity_group") and not word.startswith("##"):
            combined_entities.append(current_entity.strip())
            current_entity = ""

    # Append any remaining entity
    if current_entity:
        combined_entities.append(current_entity.strip())

    return combined_entities

def parse_resume_with_api(resume_text):
    """Parse resume text using HuggingFace API and combine all entities into one list."""
    try:
        # Preprocess the resume text
        clean_text = preprocess_resume(resume_text)
        logger.info("Preprocessed Resume Text Successfully")

        # Get entities from HuggingFace API
        api_response = get_entities_from_api(clean_text)

        if "error" in api_response:
            logger.error("NER API returned an error.")
            return {"error": api_response["error"]}

        if not isinstance(api_response, list):
            logger.error(f"Unexpected NER API response format: {api_response}")
            return {"error": "Unexpected API response format"}

        # Clean and group NER entities into a single list
        combined_entities = clean_and_group_entities(api_response)
        logger.info(f"Combined Parsed Data: {combined_entities}")

        return {"parsed_data": combined_entities}

    except Exception as e:
        logger.error(f"Error parsing resume with API: {str(e)}")
        return {"error": str(e)}
