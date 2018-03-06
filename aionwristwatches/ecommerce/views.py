import re
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from .forms import RegistrationForm
from .models import Product, ProductManager, AccountingManager, Admin

def index(request):
	product_list = Product.objects.all()
	if request.method == 'POST':
		regform = RegistrationForm(request.POST)
		print("REQUEST POST")
		if regform.is_valid():
			print("FORM VALID")
			regform.save()
			return redirect('/')

		regform = RegistrationForm()
		context = {
			'product_list': product_list,
        	'regform': regform,
        }
		return login(request, context)
	regform = RegistrationForm()
	context = {
		'product_list': product_list,
		'regform': regform,
	}
	return render(request, 'ecommerce/index.html', context)


def acctman(request):
    product_list = Product.objects.all()
    context = {
        'product_list': product_list,
	}
    return render(request, 'ecommerce/acctman.html', context)

def add_to_cart(request, product_id):
#     cart = request.session.get('cart',{})
#     product = Product.objects.get(id=product_id)
#     cart[product_id] = product
#     request.session['cart'] = cart
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#Cart View
def checkout(request):
	##cart = request.session.get('cart', {})
	return render(request, 'ecommerce/checkout.html')

def shipping(request):
    return render(request, 'ecommerce/shipping.html')

def prodman(request):
	product_list = Product.objects.all()
	context = {
		'product_list': product_list,
	}
	return render(request, 'ecommerce/prodman.html', context)
def loginmanager(request):
    
    return render(request, 'ecommerce/loginmanager.html')

def adminman(request):
    
    return render(request, 'ecommerce/adminman.html')

def prodmng(request):
    
    return render(request, 'ecommerce/prodmng.html')

def editp(request):
    
    return render(request, 'ecommerce/editpman.html')
def addp(request):
	context = { 
		"alert": None
	}

	if request.method == "POST":
		pm_inst = ProductManager()

		first = request.POST["first"]
		last = request.POST["last"]
		username = request.POST["username"]
		password = request.POST["password"]
		cpassword = request.POST["cpassword"]
		email = request.POST["email"]

		if len(first) > 0 and len(last) > 0 and len(username) > 0 and \
			len(password) > 0 and len(cpassword) > 0 and len(email) > 0:
			email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

			if len(password) < 6 or len(username) < 3:
				context["alert"] = "Password must be at least 6 characters long and the\
				username must be at least 3 characters long."
			elif password != cpassword:
					context["alert"] = "Passwords do not match."
			elif not email_pattern.match(email):
				context["alert"] = "Invalid email address"
			elif len(ProductManager.objects.filter(uname=username)) > 0 or \
				len(AccountingManager.objects.filter(uname=username)) > 0 or \
				len(Admin.objects.filter(uname=username)) > 0:
				context["alert"] = "The username already exists"
			elif len(ProductManager.objects.filter(email=email)) > 0 or \
				len(AccountingManager.objects.filter(email=email)) > 0 or \
				len(Admin.objects.filter(email=email)) > 0:
				context["alert"] = "That email is already in use"
			else:
				pm_inst.uname = username
				pm_inst.password = password
				pm_inst.email = email
				pm_inst.first = first
				pm_inst.last = last

				pm_inst.save(force_insert=True)
				context["alert"] = "Product manager created"
		else:
			context["alert"] = "Not enough information was given"

	return render(request, 'ecommerce/addpman.html', context)

def uacct(request):
	return render(request, 'ecommerce/uacct.html')

def product(request, product_id):
	product_obj = Product.objects.filter(id=product_id)[:1].get()
	context = {
		'product_obj': product_obj,
	}
	return render(request, 'ecommerce/product.html', context)
