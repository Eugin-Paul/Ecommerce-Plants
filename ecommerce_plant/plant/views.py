from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.http import JsonResponse
import requests
import json
from .forms import AddressForm,PincodeForm,CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def register(request) :
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST' :
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                Customer.objects.create(user=user,name=user.username)
                messages.success(request,'Account was created for ' + str(user))
                return redirect('loginpage')
    context = {
    'form' : form
    }
    return render(request,'plant/register.html',context)


def loginpage(request) :
    if request.user.is_authenticated:
        return redirect('home')
    else :
        if request.method == 'POST' :
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username = username, password = password)
            if user is not None :
                login(request,user)
                return redirect('home')
            else :
                messages.info(request,'Username OR Password is incorrect')
    context = {
    }
    return render(request,'plant/login.html',context)

def logoutpage(request) :
    logout(request)
    context = {
    }
    return redirect('loginpage')



def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        products = Product.objects.all()
        order,created = Order.objects.get_or_create(customer = customer,complete = False)
        cartItems = order.get_cart_quantity
    else:
        products = Product.objects.all()
        cartItems = ''


    context = {
    'products':products,
    'cartItems' : cartItems
    }
    return render(request,'plant/home.html',context)

@login_required(login_url = 'loginpage')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get(customer = customer,complete = False)
        items = order.orderitem_set.all()
        print(items)

        item_num = order.orderitem_set.count()
        print(item_num)
        cartItems = order.get_cart_quantity
    # else:
    #     items = []
    #     item_num = 0
    #     order = {'get_cart_total' : 0, 'get_cart_quantity' : 0}
    #     cartItems = order['get_cart_quantity']


    context = {
    'items' : items,
    'order' : order,
    'item_num' : item_num,
    'cartItems' : cartItems
    }
    return render(request,'plant/cart.html',context)

def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:' ,action)
    print('productId:' ,productId)

    customer = request.user.customer
    print('Customer is  : ', customer)
    product = Product.objects.get(id = productId)
    print('Product is  : ', product)
    order,created = Order.objects.get_or_create(customer = customer,complete = False)
    print('order is  : ', order)
    orderItem,created = OrderItem.objects.get_or_create(order = order, product = product)
    print('orderItem is  : ', orderItem)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0 :
        orderItem.delete()

    return JsonResponse('Item was added',safe = False)

@login_required(login_url = 'loginpage')
def address(request):
    if  request.user.is_authenticated:
        customer = request.user.customer
        form = AddressForm()
        if request.method == 'POST':
            form = AddressForm(request.POST)
            print(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                address = form.cleaned_data.get('address')
                city = form.cleaned_data.get('city')
                state = form.cleaned_data.get('state')
                city = form.cleaned_data.get('city')
                phonenumber = form.cleaned_data.get('phonenumber')
                landmark = form.cleaned_data.get('landmark')
                billing_address = BillingAddress(
                customer = customer,
                name=name,
                email = email,
                address = address,
                city = city,
                state = state,
                phonenumber = phonenumber,
                landmark = landmark,
                )
                billing_address.save()
                print("Valid Form")
                return redirect('home')

    context = {
    'form' : form
    }
    return render(request,'plant/address.html',context)

def sort_low_to_high(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        products = Product.objects.order_by('price')
        order = Order.objects.get(customer = customer,complete = False)
        cartItems = order.get_cart_quantity
    else:
        products = Product.objects.order_by('price')
        cartItems = ''


    context = {
    'products':products,
    'cartItems' : cartItems
    }
    return render(request,'plant/home.html',context)

def sort_high_to_low(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        products = Product.objects.order_by('-price')
        order = Order.objects.get(customer = customer,complete = False)
        cartItems = order.get_cart_quantity
    else:
        products = Product.objects.order_by('-price')
        cartItems = ''
    context = {
    'products':products,
    'cartItems' : cartItems
    }
    return render(request,'plant/home.html',context)

def sort_new(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        products = Product.objects.order_by('-id')
        order = Order.objects.get(customer = customer,complete = False)
        cartItems = order.get_cart_quantity
    else:
        products = Product.objects.order_by('-id')
        cartItems = ''
    context = {
    'products': products,
    'cartItems' : cartItems
    }
    return render(request,'plant/home.html',context)

def sort_old(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        products = Product.objects.order_by('id')
        order = Order.objects.get(customer = customer,complete = False)
        cartItems = order.get_cart_quantity
    else:
        products = Product.objects.order_by('id')
        cartItems = ''
    context = {
    'products':products,
    'cartItems' : cartItems
    }
    return render(request,'plant/home.html',context)

def search(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        products = Product.objects.filter(name__startswith = search)
        print(products)
    context = { 'products':products
    }
    return render(request,'plant/home.html',context)

def pincode(request,product_id):
    pincodes = ['682308','682311']
    products = Product.objects.get(pk = product_id)
    print(products)
    if request.method == 'GET':
        pincode = request.GET.get('pin_code')
        if pincode in pincodes:
            # messages.success(request,'Form submission successful')
            print("True")
    context = { 'products':products
    }
    return render(request,'plant/aralia.html',context)

def plants(request,product_id) :
    if request.user.is_authenticated:
        form = PincodeForm()
        customer = request.user.customer
        products = Product.objects.get(pk = product_id)
        order = Order.objects.get(customer = customer,complete = False)
        cartItems = order.get_cart_quantity
        if request.method == 'POST':
            form = PincodeForm(request.POST)
            if form.is_valid():
                # form.save()
                print("Valid Form")
                return redirect('plants')



    context = {
    'products': products,
    'cartItems' : cartItems,
    'form' : form
    }
    print(products.name)
    # if products.name == "Areca Palm Plant":
    #     return render(request,'plant/areca.html',context)
    # elif products.name == "Aralia Variegated Mini Plant":
    return render(request,'plant/aralia.html',context)
