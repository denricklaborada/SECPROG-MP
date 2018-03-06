from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import timedelta, datetime

class Product(models.Model):
    prodname = models.CharField(max_length=40)
    description = models.CharField(max_length=300)
    price = models.DecimalField(default=0.00, max_digits=20, decimal_places=2,  validators=[MinValueValidator(0)])
    initialstock = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    CHOICES = (
        ('Analog', 'Analog'),
        ('Digital', 'Digital'),
        ('Smart', 'Smart'),
    )
    category = models.CharField(max_length=7, choices=CHOICES)
    image = models.ImageField(upload_to='ecommerce/static/product_images/', blank=True)

    def __str__(self):
        return self.prodname
    class Meta:
        verbose_name_plural = "Products"

#User Additional Classes
middle_initial = models.CharField(blank=True, max_length=5)
middle_initial.contribute_to_class(User, 'middle_initial')

bhouse_num = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1)])
bstreet = models.CharField(blank=True, max_length=60)
bsubdivision = models.CharField(blank=True, max_length=60)
bcity = models.CharField(blank=True, max_length=60)
bpc = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1)])
bcountry = models.CharField(blank=True, max_length=60)

bhouse_num.contribute_to_class(User, 'bhouse_num')
bstreet.contribute_to_class(User, 'bstreet')
bsubdivision.contribute_to_class(User, 'bsubdivision')
bcity.contribute_to_class(User, 'bcity')
bpc.contribute_to_class(User, 'bpc')
bcountry.contribute_to_class(User, 'bcountry')

shouse_num = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1)])
sstreet = models.CharField(blank=True, max_length=60)
ssubdivision = models.CharField(blank=True, max_length=60)
scity = models.CharField(blank=True, max_length=60)
spc = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1)])
scountry = models.CharField(blank=True, max_length=60)

shouse_num.contribute_to_class(User, 'shouse_num')
sstreet.contribute_to_class(User, 'sstreet')
ssubdivision.contribute_to_class(User, 'ssubdivision')
scity.contribute_to_class(User, 'scity')
spc.contribute_to_class(User, 'spc')
scountry.contribute_to_class(User, 'scountry')

cart = models.ManyToManyField(Product, blank=True)

cart.contribute_to_class(User, 'cart')



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    comment = models.CharField(blank=True, max_length=20)
    pubdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Review - " + str(self.id)
    class Meta:
        verbose_name_plural = "Reviews"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prodlist = models.ManyToManyField(Product, blank=True)
    pubdate = models.DateTimeField(auto_now_add=True)
    subtotal =  models.DecimalField(default=0.00, max_digits=20, decimal_places=2,  validators=[MinValueValidator(0)])

    def __str__(self):
        return "Transaction - " + str(self.id)

    class Meta:
        verbose_name_plural = "Transactions"

class ProductManager(models.Model):
    first = models.CharField(max_length=20)
    last = models.CharField(max_length=20)
    uname = models.CharField(unique=True, max_length=20)
    password = models.CharField(blank=True, max_length=20)
    email = models.CharField(unique=True,  max_length=20)
    temporary = models.BooleanField(default=True)
    datecreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Product Manager - " + str(self.uname)

    def is_expired(self):
        if self.temporary == True and (timezone.now() - self.datecreated) > timedelta(1):
            return True

        return False
        
    class Meta:
        verbose_name_plural = "Product Managers"

class AccountingManager(models.Model):
    first = models.CharField(max_length=20)
    last = models.CharField(max_length=20)
    uname = models.CharField(unique=True, max_length=20)
    password = models.CharField(blank=True, max_length=20)
    email = models.CharField(unique=True, max_length=20)
    temporary = models.BooleanField(default=True)
    datecreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Accounting Manager - " + str(self.uname)

    def is_expired(self):
        if self.temporary == True and (timezone.now() - self.datecreated) > timedelta(1):
            return True

        return False

    class Meta:
        verbose_name_plural = "Accounting Managers"

class Admin(models.Model):
    uname = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    datecreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Admin - " + str(self.uname)

    class Meta:
        verbose_name_plural = "Admins"