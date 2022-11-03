
from django.shortcuts import redirect, render
# from rest_framework.decorators import api_view
from django.http.response import JsonResponse
# from rest_framework import status
from luna.models import *
import re
from django.views.decorators.csrf import csrf_exempt

from django.views.decorators.debug import sensitive_variables
from luna.models import *
from luna.validator import *


@sensitive_variables('uid')
def viewcart(request):
    # static filer for cart need to change once addtocart is implemented
    uid = request.session['id']
    cart = Cart.objects.select_related("user_id").filter(user_id=uid)
    total_price = 0
    quantity = 0
    for item in cart:
        total_price = total_price + item.quantity * item.total_price
        quantity = quantity + item.quantity 
    context = {"cart": cart, 'total_price':total_price, 'quantity':quantity}
    return render(request, "cart.html", context)


@sensitive_variables('uid')
def updatecart(request):
    uid = request.session['id']
    prodID = int(request.POST.get('product_id'))
    if request.method == 'POST':
        if(Cart.objects.filter( user_id  = uid, product_id = prodID )):
            prod_qty = (request.POST.get('quanity'))
            cart = Cart.objects.get( product_id = prodID, user_id  = uid,)
            cart.quantity = prod_qty
            cart.save()
            messages.success(request, 'Updated successfully')
        return JsonResponse({'status': "Updated Successfully"})
    return redirect('/')


@sensitive_variables('uid')
def deletecartitem(request):
    uid = request.session['id']
    if request.method == 'POST':
        prodID = int(request.POST.get('product_id'))
        if(Cart.objects.filter( user_id  = uid, product_id = prodID )):
            cart = Cart.objects.get(product_id = prodID , user_id  = uid)
            cart.delete()
            messages.success(request, 'Deleletd successfully')
        return JsonResponse({'status': "Deleted Successfully"})
    return redirect('/')