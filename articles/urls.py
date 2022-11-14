from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name="index"),
    path('region_create/', views.region_create, name='region_create'),
    path('<int:region_pk>/region_update/', views.region_update, name='region_update'),
    path('<int:region_pk>/region_delete/', views.region_delete, name='region_delete'),
    path('theme_create/', views.theme_create, name='theme_create'),
    path('<int:theme_pk>/theme_update/', views.theme_update, name='theme_update'),
    path('<int:theme_pk>/theme_delete/', views.theme_delete, name='theme_delete'),
    path('theme_region_list/', views.theme_region_list, name='theme_region_list'),
    path('create/', views.create, name="create"),
    path('<int:article_pk>/', views.detail, name="detail"),
    path('<int:article_pk>/update', views.update, name="update"),
    path('<int:article_pk>/delete', views.delete, name="delete"),
    path('<int:pk>/like/', views.like, name="like"),
    path('<int:region_pk>/<int:theme_pk>/region_theme_articles/', views.region_theme_articles, name='region_theme_articles'),
    path('<int:region_pk>/<int:theme_pk>/region_theme_articles_grade/', views.region_theme_articles_grade, name='region_theme_articles_grade'),
    path('<int:region_pk>/<int:theme_pk>/region_theme_articles_review/', views.region_theme_articles_review, name='region_theme_articles_review'),
    path('<int:region_pk>/<int:theme_pk>/region_theme_articles_low/', views.region_theme_articles_low, name='region_theme_articles_low'),
    path('<int:region_pk>/<int:theme_pk>/region_theme_articles_high/', views.region_theme_articles_high, name='region_theme_articles_high'),
    path('<int:region_pk>/<int:theme_pk>/region_theme_articles_recent/', views.region_theme_articles_recent, name='region_theme_articles_recent'),
    path("<int:article_pk>/review/create/", views.review_create, name="review_create"),
    path("review/<int:review_pk>/", views.review_detail, name="review_detail"),
    path("review/<int:review_pk>/delete/", views.review_delete, name="review_delete"),
    path("review/<int:review_pk>/update/", views.review_update, name="review_update"),
    path("review/<int:review_pk>/like/", views.review_like, name="review_like"),
    path('review/<int:review_pk>/comments/', views.comment_create, name='comment_create'),
    path("review/<int:review_pk>/comments/<int:comment_pk>/delete/",views.comment_delete, name="comment_delete"),
    path("search/", views.search, name='search'),
    path('<int:article_category>/region_index/', views.region_index, name="region_index"),
    path('map/',views.map, name="map"),
    path('<int:region_pk>/region_index/', views.region_index, name="region_index"),

]
