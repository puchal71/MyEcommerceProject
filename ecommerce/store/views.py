from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .forms import CreateUserForm
from .models import *
from django.http import JsonResponse, HttpResponse
import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required
# from django.conf import settings
# from django.template.loader import render_to_string
# import weasyprint



@login_required
def store(request):

# Dodane zeby pokazac ilosc produktow w koszyku dla widoku. Nie bede uzywal raczej.


    if request.user.is_authenticated:
        user = request.user
        customer, created = Customer.objects.get_or_create(
            user=user,
            name=user.first_name,
            email=user.email,
        )

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

@login_required
def cart(request):

    if request.user.is_authenticated:
        user = request.user
        customer, created = Customer.objects.get_or_create(
            user=user,
            name=user.first_name,
            email=user.email,
        )
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

@login_required
def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        customer, created = Customer.objects.get_or_create(
            user=user,
            name=user.first_name,
            email=user.email,
        )
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

    user = request.user
    customer, created = Customer.objects.get_or_create(
        user=user,
        name=user.first_name,
        email=user.email,
    )
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


def login_page(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, "Felaktiga uppgifter")

        context = {}
        return render(request, 'store/login_page.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Kontot skaffade för: " + user)
                return redirect('login')
            else:
                messages.info(request, "Kunde inte skaffa konto...")
        context = {'form': form}
        return render(request, 'store/register.html', context)


def logout_page(request):
    logout(request)
    return redirect('store')


# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('orders/pdf.html', {'order':order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=order_{order_id}.pdf'
#     weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT/'css/pdf.css')])
#     return response

