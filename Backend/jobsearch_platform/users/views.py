from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

@require_http_methods(["POST"])
def register(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return JsonResponse({'message': 'User registered successfully'}, status=201)
    return JsonResponse({'error': form.errors}, status=400)

@require_http_methods(["POST"])
def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'message': 'Login successful'}, status=200)
    return JsonResponse({'error': 'Invalid credentials'}, status=400)

# @login_required
def user_profile(request):
    # Commenting out the authentication check
    # if request.user.is_authenticated:
    user_data = {
        'username': request.user.username,
        'email': request.user.email,
        'role': request.user.userprofile.role,  
    }
    return JsonResponse(user_data, status=200)
    # return JsonResponse({'error': 'User not authenticated'}, status=401)


# def user_profile(request):
#     # Check if the user is authenticated; otherwise, return default values or an empty response
#     if request.user.is_authenticated:
#         user_data = {
#             'username': request.user.username,
#             'email': request.user.email,
#             'role': request.user.userprofile.role,  
#         }
#     else:
#         # Default values for unauthenticated users
#         user_data = {
#             'username': 'Guest',
#             'email': 'Not logged in',
#             'role': 'Unknown'
#         }
    
#     return JsonResponse(user_data, status=200)
