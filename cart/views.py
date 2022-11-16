from django.shortcuts import render, redirect
import requests
import json
from django.template import loader
from articles.models import Reservation


# Create your views here.
def kakaoPay(request, reservation_pk):
    reservation = Reservation.objects.get(pk=reservation_pk)
    context = {
        'reservation':reservation,
    }
    return render(request, 'cart/kakaoPay.html', context)

def kakaoPayLogic(request):
    _admin_key = 'fc36d9bcf49db100bbe5167e1e0f95b1'
    _url = 'https://kapi.kakao.com/v1/payment/ready'
    _headers = {
        "Authorization": f"KakaoAK {_admin_key}"
    }
    _data = {
        "cid": "TC0ONETIME",    
        "partner_order_id": "partner_order_id",     
        "partner_user_id": "partner_user_id",    
        "item_name": "초코파이",        
        "quantity": "1",             
        "total_amount": "2200",       
        "vat_amount": "200",
        "tax_free_amount": "0",        
        "approval_url": "http://127.0.0.1:8000/cart/paySuccess",
        "fail_url": "http://127.0.0.1:8000/cart/payFail",
        "cancel_url": "http://127.0.0.1:8000/cart/payCancel",
    }

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