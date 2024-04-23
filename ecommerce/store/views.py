from django.shortcuts import render
from .models import *
from .models import User
from django.http import JsonResponse
import json

# Create your views here.

def store(request):

# Dodane zeby pokazac ilosc produktow w koszyku dla widoku. Nie bede uzywal raczej.

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items_number
    else:
        items = []

    # Dodane, zeby przy niezalogowanym uzytkowniku nie wywalalo bleu tylko dawalo pusty koszyk.
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items_number']


    products = Product.objects.all()
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'products': products}
    return render(request, 'store/store.html', context)


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items_number
    else:
        items = []
        print("Uzytkownik musi byc zalogowany, zeby zlozyc zamowienie!")
        # Dodane, zeby przy niezalogowanym uzytkowniku nie wywalalo bleu tylko dawalo pusty koszyk.
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items_number']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items_number
    else:
        items = []

        # Dodane, zeby przy niezalogowanym uzytkowniku nie wywalalo bleu tylko dawalo pusty koszyk.
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items_number']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +100)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -100)
    orderItem.save()
    if orderItem.quantity <= 0 or action == 'delete':
        orderItem.delete()


    return JsonResponse('dodano obiekt', safe=False)


