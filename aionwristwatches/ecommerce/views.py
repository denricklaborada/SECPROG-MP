
import re
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import login, logout
from django.http import HttpResponseRedirect
from .forms import RegistrationForm
from .models import Product
from django.contrib.auth.models import User

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
    prod = Product.objects.get(pk=1)
    product_diff = prod.initialstock - prod.quantity
    context = {
        'prod': prod,
        'product_list': product_list,
        'product_diff': product_diff,
	}
    return render(request, 'ecommerce/acctman.html', context)

def checkout(request, product_id):
    if request.method == "POST":
        prodid = request.POST["productid"]
        qty = request.POST["quantity"]
        #do the transaction part :)
    product = Product.objects.get(id=product_id)
    return render(request, 'ecommerce/checkout.html',{'product': product})

def shipping(request):
    return render(request, 'ecommerce/shipping.html')

def prodman(request):
	product_list = Product.objects.all()
	context = {
		'product_list': product_list,
	}
	return render(request, 'ecommerce/prodman.html', context)
def loginmanager(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST': 
        
        login(request)
        user = User.objects.filter(username=request.POST['username'])[:1].get()
        print(user.usertypes)
        if user.usertypes == 'Administrator':
            return redirect('/adminman/')
        if user.usertypes == 'ProductManager':
            return redirect('/prodman/')
        if user.usertypes == 'AccountingManager':
            return redirect('/acctman/')
        
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
                context["alert"] = "Password must be at least 6 characters long and the username must be at least 3 characters long."
            elif password != cpassword:
                context["alert"] = "Passwords do not match."
            elif not email_pattern.match(email):
                context["alert"] = "Invalid email address"
            elif len(User.objects.filter(username=username)) > 0 :
                context["alert"] = "The username already exists"
            elif len(User.objects.filter(email=email)) > 0 :
                context["alert"] = "That email is already in use"
            else:
                pm_inst = User.objects.create_user(username=username,
                                 email=email,
                                 password=password, first_name=first ,last_name=last,usertypes='ProductManager')

                pm_inst.save()
                context["alert"] = "Product manager created"
        else:
            context["alert"] = "Not enough information was given"
            
    return render(request, 'ecommerce/addpman.html')

def uacct(request):
	return render(request, 'ecommerce/uacct.html')

def product(request, product_id):
	product_obj = Product.objects.filter(id=product_id)[:1].get()
	context = {
		'product_obj': product_obj,
	}
	return render(request, 'ecommerce/product.html', context)
