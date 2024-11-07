from django.urls import path
from . import views

urlpatterns = [
    path('indexTest/', views.index_view, name='index'),  # This is the index page
]