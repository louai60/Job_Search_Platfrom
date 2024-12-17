from transformers import pipeline
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import logging
from .serializers import ResumeSerializer
from .models import Resume
from .huggingface_parser import parse_resume_with_api
from .summarize_resume import summarize_text
from .pdf_extractor import extract_text_pdf, extract_text_docx, extract_text_txt, extract_text_rtf_odt
from django.utils.text import get_valid_filename

# Configure logging
logger = logging.getLogger(__name__)

def extract_text_from_resume(file):
    file_name = get_valid_filename(file.name)
    try:
        if file_name.endswith('.pdf'):
            return {'text': extract_text_pdf(file)}
        elif file_name.endswith('.docx'):
            return {'text': extract_text_docx(file)}
        elif file_name.endswith('.txt'):
            return {'text': extract_text_txt(file)}
        elif file_name.endswith('.rtf') or file_name.endswith('.odt'):
            return {'text': extract_text_rtf_odt(file)}
        else:
            return {'error': 'Unsupported file format. Please upload .pdf, .docx, .txt, .rtf, or .odt files.'}
    except Exception as e:
        logger.error(f"Failed to extract text from file {file_name}: {str(e)}")
        return {'error': f"Failed to extract text from file {file_name}: {str(e)}"}

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_and_process_resume(request):
    """
    Handles the upload of a resume and processes it using Hugging Face transformers.
    """
    try:
        with transaction.atomic():
            # Deactivate previous resumes for the user
            Resume.objects.filter(user=request.user, is_active=True).update(is_active=False)

            # Serialize and validate incoming data
            serializer = ResumeSerializer(data=request.data)
            if serializer.is_valid():
                resume = serializer.save(user=request.user)

                # Extract text from the uploaded resume
                file = resume.file
                logger.info(f"Extracting text from file: {file.name}")
                extracted_data = extract_text_from_resume(file)

                if "error" in extracted_data:
                    raise ValueError(extracted_data["error"])

                resume_text = extracted_data["text"]

                # Summarize the extracted text
                logger.info("Summarizing the extracted resume text.")
                summary = summarize_text(resume_text)

                if "error" in summary:
                    raise ValueError(summary["error"])

                # Parse the summarized text for skills, experience, education, and projects
                logger.info("Parsing the summarized resume text.")
                parsed_data = parse_resume_with_api(summary)

                if "error" in parsed_data:
                    raise ValueError(parsed_data["error"])

                # Save parsed data back to the resume
                resume.parsed_data = parsed_data
                # resume.skills = parsed_data.get("skills", [])
                # resume.experience = parsed_data.get("experience", [])
                # resume.education = parsed_data.get("education", [])
                # resume.projects = parsed_data.get("projects", [])
                resume.save()

                logger.info(f"Resume processed successfully for user {request.user.id}")
                return Response({
                    "message": "Resume processed successfully",
                    "data": ResumeSerializer(resume).data
                }, status=status.HTTP_201_CREATED)

            logger.warning("Invalid resume data")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        return Response({
            "error": f"Error processing resume: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_resume_details(request, resume_id):
    """
    Retrieves the details of a specific resume.
    """
    try:
        resume = Resume.objects.get(id=resume_id, user=request.user)
        serializer = ResumeSerializer(resume)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Resume.DoesNotExist:
        logger.error(f"Resume with ID {resume_id} not found for user {request.user.id}")
        return Response({"error": "Resume not found"}, status=status.HTTP_404_NOT_FOUND)

def update_resume_with_parsed_data(resume, parsed_data):
    try:
        # Ensuring parsed_data is a list and contains dictionaries
        if not isinstance(parsed_data, list) or not all(isinstance(item, dict) for item in parsed_data):
            raise ValueError("Parsed data is not in the expected format: List of dictionaries required.")

        # Processing each entity in the parsed data
        for entity in parsed_data:
            entity_group = entity.get('entity_group')
            if entity_group == 'SKILL':
                resume.skills.append(entity['word'])
            elif entity_group == 'EXPERIENCE':
                resume.experience.append(entity['word'])
            elif entity_group == 'EDUCATION':
                resume.education.append(entity['word'])

        resume.save()
    except Exception as e:
        logger.error(f"Error updating resume with parsed data: {str(e)}")
        raise
