
import re
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import login, logout
from django.http import HttpResponseRedirect
from .forms import RegistrationForm
from .models import Product, Transaction, Review
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

def myorders(request):
	if request.user.is_authenticated:
		trans = Transaction.objects.filter(user=request.user)

		return render(request, 'ecommerce/myorders.html', {'trans': trans,})

	return redirect('/')


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
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
    	user = request.user
    	qty = request.POST['quantity']
    	total = request.POST['total']

    	trans_inst = Transaction.objects.create(user=user, product=product, quantity=qty, subtotal=total)
    	trans_inst.save()

    	product.quantity = product.quantity - int(qty)
    	product.save()

    	return redirect('/')
    
    return render(request, 'ecommerce/checkout.html',{'product': product})

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

	if request.method == "POST":
		user = request.user
		try:
			fname = request.POST['fname']
			minitial = request.POST['minitial']
			lname = request.POST['lname']
			uname = request.POST['uname']
			email = request.POST['email']
			email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

			if len(fname) > 0 and len(minitial) == 1 and len(lname) > 0 and len(uname) > 0 and len(email) > 0 and email_pattern.match(email):
				user.first_name = fname
				user.middle_initial = minitial
				user.last_name = lname
				user.username = uname
				user.email = email
				user.save()


		except:
			print('not account')

			try:
				currpass = request.POST['currpass']
				pass1 = request.POST['pass1']
				pass2 = request.POST['pass2']

				if user.check_password(currpass) and len(pass1) > 0 and len(pass2) > 0 and pass1 == pass2:
					user.set_password(pass1)
					user.save()

					return redirect('/')

			except:
				print('not password')

				try:
					bhouse_num = request.POST['bhouse_num']
					bstreet = request.POST['bstreet']
					bsubdivision = request.POST['bsubdivision']
					bcity = request.POST['bcity']
					bpc = request.POST['bpc']
					bcountry = request.POST['bcountry']

					shouse_num = request.POST['shouse_num']
					sstreet = request.POST['sstreet']
					ssubdivision = request.POST['ssubdivision']
					scity = request.POST['scity']
					spc = request.POST['spc']
					scountry = request.POST['scountry']

					if len(bhouse_num) > 0 and len(bstreet) > 0 and len(bsubdivision) > 0 and len(bcity) > 0 and len(bpc) > 0 and len(bcountry) > 0 and len(shouse_num) > 0 and len(sstreet) > 0 and len(ssubdivision) > 0 and len(scity) > 0 and len(spc) > 0 and len(scountry) > 0:
						user.bhouse_num = bhouse_num
						user.bstreet = bstreet
						user.bsubdivision = bsubdivision
						user.bcity = bcity
						user.bpc = bpc
						user.bcountry = bcountry

						user.shouse_num = shouse_num
						user.sstreet = sstreet
						user.ssubdivision = ssubdivision
						user.scity = scity
						user.spc = spc
						user.sbcountry = scountry

						user.save()

				except:
					print('not address')

	return render(request, 'ecommerce/uacct.html')

def product(request, product_id):
	product_obj = Product.objects.filter(id=product_id)[:1].get()
	reviews_obj = Review.objects.filter(product=product_obj)
	if request.method == 'POST':
		regform = RegistrationForm(request.POST)
		print("REQUEST POST")
		if regform.is_valid():
			print("FORM VALID")
			regform.save()
			return redirect('/')

		regform = RegistrationForm()
		context = {
        	'regform': regform,
		'product_obj': product_obj,
		'reviews_obj': reviews_obj,
        }
		login(request)
		return render(request, 'ecommerce/product.html', context)
	regform = RegistrationForm()
	context = {
		'regform': regform,
		'product_obj': product_obj,
		'reviews_obj': reviews_obj,
	}
	return render(request, 'ecommerce/product.html', context)
