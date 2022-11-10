from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('index/', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('<int:articles_pk>/', views.detail, name="detail"),
    path('<int:articles_pk>/update', views.update, name="update"),
    path('<int:articles_pk>/delete', views.delete, name="delete"),
]
