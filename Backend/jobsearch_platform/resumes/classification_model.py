# import logging
# import requests
# import json
# from django.conf import settings

# logger = logging.getLogger(__name__)

# # Configure DeepSeek API details
# DEEPSEEK_API_KEY = settings.DEEPSEEK_API_KEY
# DEEPSEEK_API_ENDPOINT = "https://api.deepseek.com/v1/chat/completions" 

# def classify_resume_text(resume_text):
#     """
#     Classifies the extracted resume text into predefined categories using DeepSeek AI's classification API.
#     """
#     if not resume_text.strip():
#         logger.warning("No text found in the resume for classification.")
#         return {"skills": [], "experience": [], "education": [], "projects": []}

#     headers = {
#         "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
#         "Content-Type": "application/json",
#     }

#     payload = {
#         "messages": [
#             {"role": "system", "content": "You are a helpful assistant."},
#             {
#                 "role": "user",
#                 "content": (
#                     f"Classify the following resume text into the categories: skills, experience, education, and projects. "
#                     f"Return the result in a JSON format with these keys: 'skills', 'experience', 'education', and 'projects'. "
#                     f"Here is the text:\n\n{resume_text}"
#                 )
#             },
#         ],
#         "model": "deepseek-chat",
#     }

#     try:
#         response = requests.post(DEEPSEEK_API_ENDPOINT, headers=headers, data=json.dumps(payload))
#         response.raise_for_status()  

#         response_data = response.json()
#         classification_results = response_data.get("choices", [{}])[0].get("message", {}).get("content", "")

#         logger.debug(f"Raw Classification Results: {classification_results}")

#         try:
#             categories = json.loads(classification_results)
#             return {
#                 "skills": categories.get("skills", []),
#                 "experience": categories.get("experience", []),
#                 "education": categories.get("education", []),
#                 "projects": categories.get("projects", [])
#             }
#         except json.JSONDecodeError:
#             logger.error("Failed to parse classification response as JSON.")
#             return {"skills": [], "experience": [], "education": [], "projects": []}

#     except requests.exceptions.HTTPError as http_err:
#         logger.error(f"HTTP error occurred: {http_err}")
#     except requests.exceptions.RequestException as req_err:
#         logger.error(f"Request error occurred: {req_err}")
#     except Exception as e:
#         logger.error(f"Unexpected error during classification: {str(e)}")

#     return {"skills": [], "experience": [], "education": [], "projects": []}