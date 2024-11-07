import os
import shutil
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import MediaFileForm, FolderForm
from .models import MediaFile, Folder
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from collections import Counter
from django.db.models import Q # Pour les requêtes de recherche
from django.http import JsonResponse
import json



#Création de dossier et fichiers/Upload de fichiers
def upload_file(request):
    if not request.user.is_authenticated:
        messages.error(request, "Your are not logged in!")
        return redirect('login')
    if request.method == 'POST':
        file_form = MediaFileForm(request.POST, request.FILES)
        folder_form = FolderForm(request.POST)
        
        user_folder_path = os.path.join(settings.MEDIA_ROOT, request.user.username)
        os.makedirs(user_folder_path, exist_ok=True)

    if 'add_file' in request.POST and file_form.is_valid():
            file_instance = file_form.save(commit=False)
            file_instance.user = request.user  # Associate the file with the logged-in user
            #save
            file_instance.save()
            #check folder size
            folder_size = 0
            start_path = f"media/"+request.user.username
            for path, dirs, files in os.walk(start_path):
                for f in files:
                    fp = os.path.join(path, f)
                    folder_size += os.path.getsize(fp)

            #if file_size exceeds, delete added file
            file_size = os.path.getsize(os.path.join(settings.MEDIA_ROOT, file_instance.file.name))
            if(file_size) > (40 * 1024 * 1024): #100mb folder limit
                print("file size of '"+request.user.username+" exceeds the 40MB limit.")
                messages.error(request, "Your file size exceeds the 40MB limit. The file was not uploaded.")
                file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                file_instance.delete()
                return redirect('upload_file')
                
            #if folder_size exceeds, delete added file
            if (folder_size) > (100 * 1024 * 1024): #100mb folder limit
                print("folder size of '"+request.user.username+" exceeds the 100MB limit.")
                messages.error(request, "Your folder size exceeds the 100MB limit. The file was not uploaded.")
                file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                file_instance.delete()
                return redirect('upload_file')
            
            print("folder size of '"+request.user.username+"':" + str(round(folder_size/(1024*1024),2)) + "MB")
            messages.success(request, f"Your folder size is now {round(folder_size / (1024 * 1024), 2)} MB.")
            return redirect('upload_file')

    if 'add_folder' in request.POST and folder_form.is_valid():
        folder_instance = folder_form.save(commit=False)
        folder_instance.user = request.user  # Associer le dossier à l'utilisateur connecté
        folder_instance.save()
        # Créer un dossier physique pour le dossier
        os.makedirs(os.path.join(user_folder_path, folder_instance.get_full_path()), exist_ok=True)
        return redirect('upload_file')

    else:
        file_form = MediaFileForm()
        folder_form = FolderForm()

    # ici on récupère les fichiers et dossiers de l'utilisateur et uniquement ceux de l'utilisateur
    user_folders = Folder.objects.filter(parent__isnull=True, user=request.user)
    user_files = MediaFile.objects.filter(user=request.user)

    # statistiques
    folder_count = Folder.objects.filter(user=request.user).count()
    folder_file_count=[]
    folder_file_count.append({
            'folder_name':"root",
            'file_count':MediaFile.objects.filter(user=request.user).count()
        })
    for folder in Folder.objects.filter(user=request.user):
        folder_file_count.append({
            'folder_name':folder.name,
            'file_count':MediaFile.objects.filter(folder=folder).count()
        })

    file_types = [os.path.splitext(file.file.name)[1].lower() for file in user_files]
    file_type_counts=dict(Counter(file_types))

    folder_size = 0
    start_path = f"media/"+request.user.username
    for path, dirs, files in os.walk(start_path):
        for f in files:
            fp = os.path.join(path, f)
            folder_size += os.path.getsize(fp)

    sizeMb = round(folder_size/(1024*1024),2)

    return render(request, 'myapp/home.html', {
        'file_form': file_form,
        'folder_form': folder_form,
        #ancien main
        #'folders': folders,
        #'files': files,
        'folder_count':folder_count,
        'folder_file_count':folder_file_count,
        'file_type_counts':json.dumps(file_type_counts),
        #merge flo 6/11 00:30
        'folders': user_folders,
        'files': user_files,
        'sizeMb':sizeMb,
    })

def delete_file(request, file_id):
    file_instance = get_object_or_404(MediaFile, id=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    file_instance.delete()

    return redirect('upload_file')

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

def create_physical_folder(folder_instance):
    # Crée un dossier physique dans le dossier uploads de media
    folder_path = os.path.join(settings.MEDIA_ROOT, folder_instance.get_full_path())
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def view_folder(request, folder_id):
    folder_instance = get_object_or_404(Folder, id=folder_id, user=request.user)
    files = MediaFile.objects.filter(folder=folder_instance, user=request.user)
    subfolders = Folder.objects.filter(parent=folder_instance, user=request.user)
    
    return render(request, 'myapp/folder_view.html', {
        'folder': folder_instance,
        'files': files,
        'subfolders': subfolders,
    })

def view_file(request, file_id):
    file_instance = get_object_or_404(MediaFile, id=file_id, user=request.user)
    return render(request, 'myapp/file_view.html', {
        'file': file_instance,
    })

#recherche de fichier
def search_files(request):
    query = request.GET.get('query', '')
    # Recherche tous les fichiers et dossiers de l'utilisateur
    files = MediaFile.objects.filter(user=request.user).filter(
        Q(title__icontains=query) |
        Q(folder__name__icontains=query)
    )
    folders = Folder.objects.filter(user=request.user).filter(
        Q(name__icontains=query)
    )

    return render(request, 'myapp/home.html', {
        'file_form': MediaFileForm(),
        'folder_form': FolderForm(),
        'folders': folders,
        'files': files,
        'query': query,
    })




def mon_drive(request):
    # Obtenir uniquement les dossiers racine de l'utilisateur (sans parent)
    root_folders = Folder.objects.filter(user=request.user, parent__isnull=True)
    
    # Obtenir uniquement les fichiers qui ne sont pas dans un dossier
    root_files = MediaFile.objects.filter(user=request.user, folder__isnull=True)

    return render(request, 'myapp/home.html', {
        'file_form': MediaFileForm(),
        'folder_form': FolderForm(),
        'folders': root_folders,
        'files': root_files,
    })



def drag_and_drop(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        folder_id = request.POST.get('folder_id')
        
        file_instance = MediaFile.objects.get(id=file_id)
        folder_instance = Folder.objects.get(id=folder_id)
        
        file_instance.folder = folder_instance
        file_instance.save()
    
    return redirect('upload_file')

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def move_file_to_folder(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        file_id = data.get('file_id')
        folder_id = data.get('folder_id')
        
        if not file_id or not folder_id:
            return JsonResponse({'success': False, 'error': 'Invalid file_id or folder_id'})

        file_instance = get_object_or_404(MediaFile, id=file_id)
        folder_instance = get_object_or_404(Folder, id=folder_id)
        file_instance.folder = folder_instance
        file_instance.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
