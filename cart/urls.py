from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('<int:reservation_pk>/', views.kakaoPay, name="kakaoPay"),
    path('<int:pk>/kakaoPayLogic/', views.kakaoPayLogic, name="kakaoPayLogic"),
    path('paySuccess/', views.paySuccess, name="paySuccess"),
    path('payFail/', views.payFail, name="payFail"),
    path('payCancel/', views.payCancel, name="payCancel"),
]
