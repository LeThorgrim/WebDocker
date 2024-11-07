from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('delete_folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('view_folder/<int:folder_id>/', views.view_folder, name='view_folder'),
    path('files/<int:file_id>/', views.view_file, name='view_file'),
    path('search/', views.search_files, name='search_files'),
    path('mon-drive/', views.mon_drive, name='mon_drive'),
    path('move-file-to-folder/', views.move_file_to_folder, name='move_file_to_folder'),
]