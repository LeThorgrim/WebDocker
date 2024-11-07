from django.db import models
from django.contrib.auth.models import User
import os

def user_directory_path(instance, filename):
    # fonction pour définir le chemin de stockage des fichiers
    folder_path = instance.folder.get_full_path() if instance.folder else ''
    return os.path.join(instance.user.username, folder_path, filename)

class Folder(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  

    def __str__(self):
        return self.name

    def get_full_path(self):
        """
        Retourne le chemin complet du dossier à partir du répertoire 'media'
        """
        if self.parent:
            return os.path.join(self.parent.get_full_path(), self.name)
        return self.name

class MediaFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Relier au modèle User de login_app
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=user_directory_path)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title