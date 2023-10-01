import json
from typing import List, Any

from django.contrib.auth.decorators import login_required
from django.db.models.functions import window
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import OrderDetails
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.contrib import messages
from django.views import View
from .models.cart import Cart
from .models.contact import Contact
from django.db.models import Q
from django.http import JsonResponse



def home(request):
    products = None
    totalitem = 0
    if request.session.has_key('password'):
        password = request.session['password']
        category = Category.get_all_categories()
        customer = Customer.objects.filter(password=password)
        totalitem = len(Cart.objects.filter(password=password))
        for c in customer:
            name = c.name

            categoryID = request.GET.get('category')
            if categoryID:
                products = Product.get_all_product_by_category_id(categoryID)
            else:
                products = Product.get_all_products();

            # if products.isExists():
            #    error_message = "Product is already exists.."

            data = {}
            data['name'] = name
            data['product'] = products
            data['category'] = category
            data['totalitem'] = totalitem
            # data['error_message'] = error_message
            return render(request, 'home.html', data)
    else:
        return redirect('shop')


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        name = request.POST.get('name')
        password = request.POST.get('password')
        error_message = None
        value = {
            'name': name,
            'password': password
        }

        customer = Customer(name=name, password=password)
        if (not name):
            error_message = "Name is required"
        elif not password:
            error_message = "mobile no is required"
        elif len(password) < 10:
            error_message = "mobile number must be 10 character long or more"

        elif customer.isExists():
            error_message = "Mobile number already exists.."

        if not error_message:
            messages.success(request, 'Congratulations!! Register Successfully')
            customer.register()
            return redirect('signup')
        else:
            data = {
                'error': error_message,
                'value': value
            }
            return render(request, 'signup.html', data)


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        password = request.POST.get('password')
        error_message = None
        value = {
            'password': password
        }
        customer = Customer.objects.filter(password=request.POST["password"])
        if customer:
            request.session['password'] = password
            return redirect('homepage')
        else:
            error_message = "Mobile number is invalid!!.."
            data = {'error': error_message,
                    'value': value
                    }
            return render(request, 'login.html', data)


def productdetail(request, pk):
    totalitem = 0

    product = Product.objects.get(pk=pk)
    items_already_in_cart = False
    items_already_in_wishlist = False
    if request.session.has_key('password'):
        password = request.session['password']
        totalitem = len(Cart.objects.filter(password=password))
        items_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(password=password)).exists()
        #items_already_in_wishlist = Wishlist.objects.filter(Q(product=product.id) & Q(user=password)).exists()
        customer = Customer.objects.filter(password=password)
        for c in customer:
            name = c.name
        data = {
            'product': product,
            'items_already_in_cart': items_already_in_cart,
           # 'items_already_in_wishlist': items_already_in_wishlist,
            'name': name,
            'totalitem': totalitem

        }
    return render(request, 'productdetail.html', data)


def shop(request):
    return render(request, 'shop.html')


def logout(request):
    if request.session.has_key('password'):
        del request.session['password']
        return redirect('shop')
    else:
        return redirect('shop')


def add_to_cart(request):
    password = request.session['password']
    product_id = request.GET.get('prod_id')
    product_name = Product.objects.get(id=product_id)
    product = Product.objects.filter(id=product_id)
    # for product in product.stock:
    #   product.stock -= 1
    for p in product:
        image = p.image
        price = p.price
        Cart(password=password, product=product_name, image=image, price=price, total_price=product_name.price).save()
        return redirect(f"/product-detail/{product_id}")


def show_cart(request):
    subtotal = 0
    totalitem = 0
    if request.session.has_key('password'):
        password = request.session['password']
        customer = Customer.objects.filter(password=password)
        data2 = {}
        customer = Customer.objects.filter(password=password)
        for c in customer:
            name = c.name
        for us in customer:
            cart = Cart.objects.filter(password=password)
        for c in cart:
            user = c.password
            cart_prods = [p for p in Cart.objects.all() if p.password == user]

            if cart_prods:
                for p in cart_prods:
                    tempTotal = p.quantity * Product.objects.filter(id=p.product.id)[0].price
                    subtotal += tempTotal

                    totalitem = len(Cart.objects.filter(password=password))

                    data = {
                        'name': name,
                        'cart': cart,
                        'totalitem': totalitem,
                        'total': subtotal,
                        'subtotal': subtotal,
                    }
                return render(request, 'show_cart.html', data)
        data2['name'] = name
        data2['totalitem'] = totalitem

        return render(request, 'empty_cart.html', data2)


def plus_cart(request):
    if request.session.has_key('password'):
        password = request.session['password']
        prod_id = request.GET['prod_id']
        print(prod_id)
        customer = Customer.objects.filter(password=password)
        prod_id = request.GET['prod_id']
        for us in customer:
            id = us.id
            user_password = us.password
            phone3 = Customer.objects.get(id=id)
            c1 = Cart.objects.get(Q(product=prod_id) & Q(password=user_password))
            print(c1)
            c1.quantity += 1
            c1.save()
        subtotal = 0
        cart = Cart.objects.filter(password=password)
        #myli = json.loads((str(cart.product)).replace("'", '"'))
        #if myli['objects'][0][str(prod_id)] != 5:
            #myli['objects'][0][str(prod_id)] = myli['objects'][0].get(str(prod_id), 0) + 1

        for c in cart:
            user = c.password
            cart_prods = [p for p in Cart.objects.all() if p.password == user]
            print(cart_prods)
            if cart_prods:
                for p in cart_prods:
                    tempTotal = p.quantity * Product.objects.filter(id=prod_id)[0].price
                    subtotal += tempTotal

                data = {
                    'quantity': c1.quantity,
                    'subtotal': subtotal,
                    'total': subtotal,
                }
                return JsonResponse(data)
    else:
        return redirect('login')


def minus_cart(request):
    if request.session.has_key('password'):
        password = request.session['password']
        prod_id = request.GET['prod_id']
        print(prod_id)
        customer = Customer.objects.filter(password=password)
        prod_id = request.GET['prod_id']
        for us in customer:
            id = us.id
            user_password = us.password
            phone3 = Customer.objects.get(id=id)
            c1 = Cart.objects.get(Q(product=prod_id) & Q(password=user_password))
            print(c1)
            c1.quantity -= 1
            c1.save()
        subtotal = 0.0
        cart = Cart.objects.filter(password=password)
        for c in cart:
            user = c.password
            cart_prods = [p for p in Cart.objects.all() if p.password == user]
            print(cart_prods)
            if cart_prods:
                for p in cart_prods:
                    tempTotal = p.quantity * Product.objects.filter(id=prod_id)[0].price
                    subtotal += tempTotal

                data = {
                    'quantity': c1.quantity,
                    'subtotal': subtotal,
                    'total': subtotal,
                }
                return JsonResponse(data)
    else:
        return redirect('login')


def remove_cart(request):
    if request.session.has_key('password'):
        cart_id = request.GET.get('cart_id')
        cart = Cart.objects.get(id=cart_id)
        cart.delete()
        return redirect('show_cart')
    else:
        return redirect('login')


def place_order(request):
    if request.session.has_key('password'):
        user_password = request.session['password']

        if request.method == 'POST':
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            address = request.POST.get('address')

            cart_prod = Cart.objects.filter(password=user_password)
            for cr in cart_prod:
                user = cr.password
            cart_product = [p for p in Cart.objects.all() if p.password == user]
            for p in cart_product:
                qty = p.quantity
                price = p.price
                product_name = p.product
                image = p.image

                OrderDetails(user=user, product_name=product_name, image=image, qty=qty, price=price).save()
                cart_prod.delete()

                data = {
                    'name': name,
                }
                return render(request, 'success.html', data)
            return redirect('order/')


def order(request):
    totalitem = 0
    if request.session.has_key('password'):
        password = request.session['password']
        # phone = request.POST.get('phone')
        totalitem = len(Cart.objects.filter(password=password))
        customer = Customer.objects.filter(password=password)
        for c in customer:
            name = c.name
            order = OrderDetails.objects.filter(user=password)
            data = {
                'order': order,
                'name': name,
                'totalitem': totalitem
            }
            if order:
                return render(request, 'order.html', data)
            else:
                return render(request, 'emptyorder.html', data)
    else:
        return redirect('login')


def search(request):
    totalitem = 0
    if request.session.has_key('password'):
        password = request.session['password']
        query = request.GET.get('query')
        search = Product.objects.filter(name__contains=query)
        category = Category.get_all_categories()
        totalitem = len(Cart.objects.filter(password=password))
        customer = Customer.objects.filter(password=password)
        for c in customer:
            name = c.name
        data = {
            'name': name,
            'totalitem': totalitem,
            'search': search,
            'category': category,
            'query': query
        }

        return render(request, 'search.html', data)
    else:
        return redirect('login')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        content = request.POST['content']
        contact = Contact(name=name, email=email, content=content)
        contact.save()

    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def success(request):
    return render(request, 'success.html')





def download_invoice(request, pk):
    order = OrderDetails.objects.get(id=pk)
    user = Customer.objects.get(password=order.user)
    total_price = order.price * order.qty
    data = {
        'order': order,
        'user': user,
        'total_price': total_price,
    }
    return render(request, 'download_invoice2.html', data)







