from django.contrib import admin

from .models import Product
from .models import Review
from .models import Transaction

# Register your models here.

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Transaction)
