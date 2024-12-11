import spacy
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Load the large English model
nlp = spacy.load('en_core_web_lg')

def parse_resume_with_spacy(resume_text):
    try:
        doc = nlp(resume_text)
        entities = [{'text': ent.text, 'type': ent.label_} for ent in doc.ents]
        logger.debug(f"spaCy extracted entities: {entities}")
        return entities
    except Exception as e:
        error_msg = f"Error parsing resume with spaCy: {str(e)}"
        logger.error(error_msg)
        return {'error': error_msg}
    
