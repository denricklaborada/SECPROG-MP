from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from .forms import RegistrationForm

def index(request):

	if request.method == 'POST':
		regform = RegistrationForm(request.POST)
		if regform.is_valid():
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
def checkout(request):

	
	return render(request, 'ecommerce/checkout.html')