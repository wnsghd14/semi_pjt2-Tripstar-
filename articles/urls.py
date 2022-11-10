from django.urls import path
from . import views


app_name = 'articles'

urlpatterns = [
    path('index/', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('<int:articles_pk>/', views.detail, name="detail"),
    path('<int:articles_pk>/update', views.update, name="update"),
    path('<int:articles_pk>/delete', views.delete, name="delete"),
    path('reviews/<int:pk>/comments/', views.comment_create, name='comment_create'),
    path("reviews/<int:pk>/comments/<int:comment_pk>/delete/",views.comment_delete, name="comment_delete"),
    path("reviews/<int:pk>/comments/<int:comment_pk>/update/",views.comment_update,name="comment_update"),
]
