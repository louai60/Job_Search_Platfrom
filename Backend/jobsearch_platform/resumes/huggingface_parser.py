import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def parse_resume_with_huggingface(resume_text):
    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACE_API_TOKEN}"
    }
    API_URL = "https://api-inference.huggingface.co/models/dslim/bert-base-NER"

    
    # Debug log to ensure the token and request are being sent properly
    logger.debug("Sending request to Hugging Face API")

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": resume_text})

        if response.status_code == 200:
            response_data = response.json()
            logger.debug(f"Hugging Face response: {response_data}")  # Log the raw response to check its structure
            
            # Ensure the response data is in the expected list format
            if not isinstance(response_data, list) or not all(isinstance(item, dict) for item in response_data):
                error_msg = "Expected a list of dictionaries but got something else."
                logger.error(error_msg)
                return {'error': error_msg}
            
            return response_data  # Return the list of parsed entities directly
        
        else:
            error_msg = f"Failed to parse resume with status {response.status_code}: {response.text}"
            logger.error(error_msg)
            return {'error': error_msg}
    
    except requests.exceptions.RequestException as e:
        # Catch any other request-related errors (e.g., connection errors)
        error_msg = f"Request to Hugging Face failed: {str(e)}"
        logger.error(error_msg)
        return {'error': error_msg}
