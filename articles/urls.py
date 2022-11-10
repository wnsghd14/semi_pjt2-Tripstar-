from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    # path("<int:article_pk>/review_create/", views.review_create, name="review_create"),
    # path("<int:article_pk>/review/<int:review_pk>", views.review_detail, name="review_detail"),
    # path("<int:article_pk>/review/<int:review_pk>/delete", views.review_delete, name="review_delete"),
    # path("<int:article_pk>/review/<int:review_pk>/update", views.review_update, name="review_update"),
    # path("<int:article_pk>/review/<int:review_pk>/like", views.review_like, name="review_like"),
    path("review/create/", views.review_create, name="review_create"),
    path("review/<int:review_pk>", views.review_detail, name="review_detail"),
    path("review/<int:review_pk>/delete", views.review_delete, name="review_delete"),
    path("review/<int:review_pk>/update", views.review_update, name="review_update"),
    path("review/<int:review_pk>/like", views.review_like, name="review_like"),
]
