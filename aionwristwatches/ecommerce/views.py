from django.shortcuts import render
from django.contrib.auth.views import login

def index(request):
	if request.method == 'POST':
		return login(request, template_name="ecommerce/index.html")
	return render(request, 'ecommerce/index.html')