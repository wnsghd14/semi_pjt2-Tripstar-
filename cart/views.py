from django.shortcuts import render, redirect, get_object_or_404
import requests
import json
from django.template import loader
from articles.models import Reservation, Article
from django.contrib.auth import get_user_model
import math


# Create your views here.
def kakaoPay(request, reservation_pk):
    reservation = Reservation.objects.get(pk=reservation_pk)
    total_price = reservation.adult * int(reservation.article.price) + (reservation.kid * int(reservation.article.price))/2
    context = {
        'reservation':reservation,
        'total_price':math.trunc(total_price),
        
    }
    return render(request, 'cart/kakaoPay.html', context)

def kakaoPayLogic(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    print(pk)
    reservation = Reservation.objects.get(pk=pk)
    article = Article.objects.get(pk=reservation.article.pk)
    total_price = int(reservation.adult + reservation.kid) * int(reservation.article.price)
    _admin_key = 'fc36d9bcf49db100bbe5167e1e0f95b1'
    _url = 'https://kapi.kakao.com/v1/payment/ready'
    _headers = {
        "Authorization": f"KakaoAK {_admin_key}"
    }
    _data = {
        "cid": "TC0ONETIME",    
        "partner_order_id": "partner_order_id",     
        "partner_user_id": "partner_user_id",    
        "item_name": article.title,        
        "quantity": "1",             
        "total_amount": total_price, # Integer Field로 맞춰줘야함       
        "vat_amount": "200", # total_amount = vat_amount 보다 값이 커야 함
        "tax_free_amount": "0",        
        "approval_url": "http://127.0.0.1:8000/cart/paySuccess",
        "fail_url": "http://127.0.0.1:8000/cart/payFail",
        "cancel_url": "http://127.0.0.1:8000/cart/payCancel",
    }
    print(_data)
    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()  
    request.session['tid'] = _result['tid']     
    return redirect(_result['next_redirect_pc_url'])

def paySuccess(request):
    _url = 'https://kapi.kakao.com/v1/payment/approve'
    _admin_key = 'fc36d9bcf49db100bbe5167e1e0f95b1'
    _headers = {
        "Authorization": f"KakaoAK {_admin_key}"  
    }
    _data = {
        "cid": "TC0ONETIME",    
        "tid": request.session['tid'],
        "partner_order_id": "partner_order_id",     
        "partner_user_id": "partner_user_id", 
        "pg_token": request.GET['pg_token']
    }

    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()  
    if _result.get('msg'):
        return redirect('cart:payFail')
    else:
        return render(request, 'cart/paySuccess.html')

def payFail(request):
    return render(request, 'cart/payFail.html')

def payCancel(request):
    return render(request, 'cart/payCancel.html')