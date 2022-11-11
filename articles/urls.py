from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('<int:article_pk>/', views.detail, name="detail"),
    path('<int:article_pk>/update', views.update, name="update"),
    path('<int:article_pk>/delete', views.delete, name="delete"),
    path('<int:pk>/like/', views.like, name="like"),
    path("<int:article_pk>/review/create/", views.review_create, name="review_create"),
    path("review/<int:review_pk>/", views.review_detail, name="review_detail"),
    path("review/<int:review_pk>/delete/", views.review_delete, name="review_delete"),
    path("review/<int:review_pk>/update/", views.review_update, name="review_update"),
    path("review/<int:review_pk>/like/", views.review_like, name="review_like"),
    path('review/<int:review_pk>/comments/', views.comment_create, name='comment_create'),
    path("review/<int:review_pk>/comments/<int:comment_pk>/delete/",views.comment_delete, name="comment_delete"),
    path("search/", views.search, name='search'),
    path('<int:article_category>/region_index/', views.region_index, name="region_index"),
]
