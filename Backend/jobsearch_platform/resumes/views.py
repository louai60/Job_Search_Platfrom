# from django.http import JsonResponse
# from django.views.decorators.http import require_http_methods
# from .models import Resume
# from django.contrib.auth.decorators import login_required

# @login_required
# @require_http_methods(["POST"])
# def upload_resume(request):
#     file = request.FILES.get('resume')
#     if not file:
#         return JsonResponse({'error': 'No resume file provided'}, status=400)
    
#     resume = Resume(user=request.user, file=file)
#     resume.save()
#     return JsonResponse({'message': 'Resume uploaded successfully'}, status=201)

# @login_required
# def list_resumes(request):
#     resumes = Resume.objects.filter(user=request.user)
#     resume_data = [{'id': resume.id, 'file': resume.file.url} for resume in resumes]
#     return JsonResponse(resume_data, safe=False)


from django.http import JsonResponse
from jobmatches.utils import parse_resume
from django.contrib.auth.decorators import login_required

@login_required
def upload_resume_and_parse(request):
    if request.method == 'POST' and request.FILES['resume']:
        # Read the resume file content
        resume_file = request.FILES['resume']
        resume_text = resume_file.read().decode('utf-8')
        
        # Parse the resume
        parsed_data = parse_resume(resume_text)
        
        # Here you can save the parsed data to the database or perform further processing
        return JsonResponse(parsed_data, safe=False)
    return JsonResponse({"error": "No resume uploaded"}, status=400)