from django.core.files.storage import FileSystemStorage
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from .serializers import ResumeSerializer
from .models import Resume
from .spacy_parser import parse_resume_with_spacy
import logging

from PyPDF2 import PdfReader  
import docx  
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
def upload_resume_and_parse(request):
    try:
        with transaction.atomic():
            # Deactivate previous resumes for the user
            Resume.objects.filter(user=request.user, is_active=True).update(is_active=False)
            
            # Serialize and validate incoming data
            serializer = ResumeSerializer(data=request.data)
            if serializer.is_valid():
                resume = serializer.save(user=request.user)
                
                # Get the resume file
                file = resume.file
                file_name = get_valid_filename(file.name)

                # Extract text based on file type
                try:
                    logger.info(f"Extracting text from resume file: {file_name}")
                    if file_name.endswith('.pdf'):
                        reader = PdfReader(file)
                        resume_text = ' '.join(page.extract_text() for page in reader.pages)

                    elif file_name.endswith('.docx'):
                        doc = docx.Document(file)
                        resume_text = ' '.join(paragraph.text for paragraph in doc.paragraphs)

                    elif file_name.endswith('.txt'):
                        resume_text = file.read().decode('utf-8', errors='ignore')

                    else:
                        return Response({
                            'error': 'Unsupported file format. Please upload .pdf, .docx, or .txt files.'
                        }, status=status.HTTP_400_BAD_REQUEST)

                    logger.info(f"Text extraction successful for {file_name}")

                except Exception as e:
                    logger.error(f"Failed to extract text from file {file_name}: {str(e)}")
                    return Response({
                        'error': f"Failed to extract text from the uploaded file. Error: {str(e)}"
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # Use spaCy to parse the resume text
                parsed_data = parse_resume_with_spacy(resume_text)
                
                if 'error' in parsed_data:
                    return Response({'error': parsed_data['error']}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                # Assuming you have logic to handle the parsed data, such as saving it to the database
                # Update the resume instance with parsed data
                resume.parsed_data = parsed_data
                resume.save()

                # Trigger job matching (implement job matching logic if needed)
                # Commenting out the job matching logic as per instructions
                # matching_jobs = find_matching_jobs(resume)
                
                logger.info(f"Resume processed successfully for user: {request.user.id}")
                return Response({
                    'message': 'Resume processed successfully',
                    'data': ResumeSerializer(resume).data,
                    # 'matching_jobs': matching_jobs
                }, status=status.HTTP_201_CREATED)
            logger.warning(f"Invalid resume data for user: {request.user.id}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        logger.error(f"Unhandled exception in upload_resume_and_parse for user {request.user.id}: {str(e)}")
        return Response({
            'error': f'Error processing resume: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def get_resume_details(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id, user=request.user)
        serializer = ResumeSerializer(resume)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Resume.DoesNotExist:
        logger.error(f"Resume with ID {resume_id} not found for user {request.user.id}")
        return Response({
            'error': 'Resume not found'
        }, status=status.HTTP_404_NOT_FOUND)

def update_resume_with_parsed_data(resume, parsed_data):
    try:
        # Ensure parsed_data is a list and contains dictionaries
        if not isinstance(parsed_data, list) or not all(isinstance(item, dict) for item in parsed_data):
            raise ValueError("Parsed data is not in the expected format: List of dictionaries required.")

        # Process each entity in the parsed data
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
