from django.urls import path
from . import views
app_name = 'articles'

urlpatterns = [
    path('reviews/<int:pk>/comments/', views.comment_create, name='comment_create'),
    path("reviews/<int:pk>/comments/<int:comment_pk>/delete/",views.comment_delete, name="comment_delete"),
    path("reviews/<int:pk>/comments/<int:comment_pk>/update/",views.comment_update,name="comment_update"),
]
