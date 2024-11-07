from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from pathlib import Path
import os
import shutil

from myapp.models import Folder, MediaFile

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log the user in
            print("login successful")
            return redirect('/main')  # Ensure this name matches the index route
        else:
            messages.error(request, 'Invalid username or password.')
            print("login failed")

    return render(request, 'login.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)  # Log the user out
        return redirect('login')
    return render(request, 'logout.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, f'Account created for {username}!')
            Path(f'media/{username}').mkdir(parents=True, exist_ok=True)
            return redirect('login')

    return render(request, 'register.html')

def delete_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Delete the user's folder
            folder_path = os.path.join('media', username)
            #folder_instance = get_object_or_404(Folder, path="media/"+username)

            # Supprimer le dossier physique et son contenu
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)

            user.delete()
            messages.success(request, f'Account deleted for {username}!')
            return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'delete.html')


#some utils 
def delete_folder(request, folder_id):
    folder_instance = get_object_or_404(Folder, id=folder_id)
    folder_path = os.path.join(settings.MEDIA_ROOT, folder_instance.get_full_path())
    
    # Supprimer tous les fichiers dans le dossier
    files = MediaFile.objects.filter(folder=folder_instance)
    for file in files:
        file_path = os.path.join(settings.MEDIA_ROOT, file.file.name)
        if os.path.exists(file_path):
            os.remove(file_path)
        file.delete()
    
    # Supprimer tous les sous-dossiers
    subfolders = Folder.objects.filter(parent=folder_instance)
    for subfolder in subfolders:
        delete_folder(request, subfolder.id)
    
    # Supprimer le dossier physique et son contenu
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    folder_instance.delete()
    return redirect('upload_file')

def delete_file(request, file_id):
    file_instance = get_object_or_404(MediaFile, id=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    file_instance.delete()
    return redirect('upload_file')