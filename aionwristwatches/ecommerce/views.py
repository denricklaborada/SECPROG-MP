from django.shortcuts import render, redirect,reverse
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from .forms import RegistrationForm
from .models import Product

def index(request):
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
        }
		return login(request, context)
	regform = RegistrationForm()
	context = {
		'regform': regform,
	}
	return render(request, 'ecommerce/index.html', context)

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

def uacct(request):

	return render(request, 'ecommerce/uacct.html')