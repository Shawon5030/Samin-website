from django.shortcuts import render, redirect
from django.views import View
from . models import Product,Customer,Cart,OrderPlaced
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
class ProductView(View):
     def get(self, request):
          totalitem = 0
          all = Product.objects.all()
          if request.user.is_authenticated:
               totalitem = len(Cart.objects.filter(user=request.user))
          return render(request, 'Shop/home.html', {'all':all,'totalitem':totalitem})

class ProductDetailView(View):
     def get(self, request, pk):
          product = Product.objects.get(pk=pk)
          item_already_in_cart = False
          if request.user.is_authenticated:
               item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
          
          return render(request, 'Shop/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart})


@login_required
def add_to_cart(request):
     user = request.user
     product_id = request.GET.get('prod_id')
     product = Product.objects.get(id=product_id)
     Cart(user=user,product=product).save()
     return redirect('/cart')

def buy_now(request):
 return render(request, 'Shop/buynow.html')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render(request, 'Shop/profile.html', {'form':form, 'active':'btn-primary'})

 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
      usr = request.user
      name = form.cleaned_data['name']
      division = form.cleaned_data['division']
      district = form.cleaned_data['district']
      thana = form.cleaned_data['thana']
      villorroad = form.cleaned_data['villorroad']
      zipcode = form.cleaned_data['zipcode']
      reg = Customer(user=usr,name=name, division=division,district=district, thana=thana, villorroad=villorroad, zipcode=zipcode)
      reg.save()
      messages.success(request, 'Congratulations! Profile Updated Successfully')
  return render(request, 'Shop/profile.html', {'form':form, 'active':'btn-primary'})


@login_required
def address(request):
     add = Customer.objects.filter(user=request.user)
     return render(request, 'Shop/address.html', {'add':add, 'active':'btn-primary'})

@login_required
def orders(request):
 return render(request, 'Shop/orders.html')



def lehenga(request, data = None):
     if data == None:
          lehengas = Product.objects.filter(category='L')
     elif data == 'lubnan' or data == 'infinity':
          lehengas = Product.objects.filter(category='L').filter(brand=data)
     elif data == 'above':
          lehengas = Product.objects.filter(category='L').filter(discounted_price__gt = 20000)
     elif data == 'below':
          lehengas = Product.objects.filter(category='L').filter(discounted_price__lt = 20000)
     return render(request, 'Shop/lehenga.html', {'lehengas':lehengas})



class CustomerRegistrationView(View):
     def get(self,request):
          form = CustomerRegistrationForm()
          return render(request, 'Shop/customerregistration.html', {'form':form})

     def post(self,request):
          form = CustomerRegistrationForm(request.POST)
          if form.is_valid():
               messages.success(request, 'Congratulations Registration Done')
               form.save()
          return render(request, 'Shop/customerregistration.html', {'form':form})


@login_required
def checkout(request):
     user = request.user
     add = Customer.objects.filter(user=user)
     if not add.exists():
          return redirect('address')
     cart_items = Cart.objects.filter(user=user)
     amount = 0.0
     shipping_amount = 100.0
     total_amount = 0
     cart_product = [p for p in Cart.objects.all() if p.user==user]
     if cart_product:
          for p in cart_product:
               tempamount = (p.quantity * p.product.discounted_price)
               amount += tempamount
          totalamount = amount + shipping_amount

     return render(request, 'Shop/checkout.html', {'add':add,'totalamount':totalamount,'cart_items':cart_items })


@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 100.0
  total_amount = 0
  cart_product = [p for p in Cart.objects.all() if p.user==user]
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    totalamount = amount + shipping_amount
   return render(request, 'Shop/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount})
  else:
   return render(request, 'Shop/emptycart.html')


#plus cart
def plus_cart(request):
    if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity +=1
      c.save()
      amount = 0
      shipping_amount = 100
      cart_product = [p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount  
            totalamount = amount + shipping_amount
      data = {
         'quantity': c.quantity,
         'amount': amount,
         'totalamount': totalamount
      }
      return JsonResponse(data)



#minus cart
def minus_cart(request):
    if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity -=1
      c.save()
      amount = 0
      shipping_amount = 100
      cart_product = [p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount  
            totalamount = amount + shipping_amount
      data = {
         'quantity': c.quantity,
         'amount': amount,
         'totalamount': totalamount
      }
      return JsonResponse(data)


#remove cart
def remove_cart(request):
    if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.delete()
      amount = 0
      shipping_amount = 100
      cart_product = [p for p in Cart.objects.all() if p.user==request.user]
      for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount  
            
      data = {
         'amount': amount,
         'totalamount': amount + shipping_amount
      }
      return JsonResponse(data)
    
  



from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, OrderPlaced, Customer

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)

    cart = Cart.objects.filter(user=user)
    order_details = []

    for c in cart:
        OrderPlaced.objects.create(
            user=user,
            customer=customer,
            product=c.product,
            quantity=c.quantity
        )
        order_details.append(f"{c.product.title} (x{c.quantity})")
        c.delete()

    # Prepare email content
    subject = 'New Order Placed Successfully'
    message = (
        f"Dear {user.username},\n\n"
        f"Thank you for your order!\n\n"
        f"Customer Name: {customer.name}\n"
        f"Address: {customer.district}, {customer.division}, {customer.zipcode}\n\n"
        f"Order Details:\n" + "\n".join(order_details) +
        f"\n\nWe’ll contact you soon.\n\nBest regards,\n{settings.DEFAULT_FROM_EMAIL}"
    )

    # Send to both user and admin
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email, settings.DEFAULT_FROM_EMAIL],  # User + Admin
        fail_silently=False,
    )

    return redirect('orders')


@login_required
def orders(request):
     op = OrderPlaced.objects.filter(user=request.user)
     return render(request, 'Shop/orders.html', {'order_placed': op})

