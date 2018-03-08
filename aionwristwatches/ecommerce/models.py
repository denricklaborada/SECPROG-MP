from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

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

bhouse_num = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1)], default=1)
bstreet = models.CharField(blank=True, max_length=60, default='')
bsubdivision = models.CharField(blank=True, max_length=60, default='')
bcity = models.CharField(blank=True, max_length=60, default='')
bpc = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1)], default=1)
bcountry = models.CharField(blank=True, max_length=60, default='')

bhouse_num.contribute_to_class(User, 'bhouse_num')
bstreet.contribute_to_class(User, 'bstreet')
bsubdivision.contribute_to_class(User, 'bsubdivision')
bcity.contribute_to_class(User, 'bcity')
bpc.contribute_to_class(User, 'bpc')
bcountry.contribute_to_class(User, 'bcountry')

shouse_num = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1)], default=1)
sstreet = models.CharField(blank=True, max_length=60, default='')
ssubdivision = models.CharField(blank=True, max_length=60, default='')
scity = models.CharField(blank=True, max_length=60, default='')
spc = models.PositiveIntegerField(null=True, validators=[MinValueValidator(1)], default=1)
scountry = models.CharField(blank=True, max_length=60, default='')

shouse_num.contribute_to_class(User, 'shouse_num')
sstreet.contribute_to_class(User, 'sstreet')
ssubdivision.contribute_to_class(User, 'ssubdivision')
scity.contribute_to_class(User, 'scity')
spc.contribute_to_class(User, 'spc')
scountry.contribute_to_class(User, 'scountry')

#cart = models.ManyToManyField(Product, blank=True)
#
#cart.contribute_to_class(User, 'cart')

USERTYPES = (
        ('Administrator', 'Administrator'),
        ('ProductManager', 'ProductManager'),
        ('AccountingManager', 'AccountingManager'),
        ('Customer', 'Customer'),
)
usertypes = models.CharField(max_length=7, choices=USERTYPES,default='Customer')
usertypes.contribute_to_class(User, 'usertypes')


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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    pubdate = models.DateTimeField(auto_now_add=True)
    subtotal =  models.DecimalField(default=0.00, max_digits=20, decimal_places=2,  validators=[MinValueValidator(0)])

    def __str__(self):
        return "Transaction - " + str(self.id)

    class Meta:
        verbose_name_plural = "Transactions"

#class ProductManager(models.Model):
#    uname = models.CharField(unique=True, max_length=20)
#    password = models.CharField(blank=True, max_length=20)
#    email = models.CharField(unique=True,  max_length=20)
#    datecreated = models.DateTimeField(auto_now_add=True)
#
#    def __str__(self):
#        return "Product Manager - " + str(self.uname)
#    class Meta:
#        verbose_name_plural = "Product Managers"
#
#class AccountingManager(models.Model):
#    uname = models.CharField(unique=True, max_length=20)
#    password = models.CharField(blank=True, max_length=20)
#    email = models.CharField(unique=True, max_length=20)
#    datecreated = models.DateTimeField(auto_now_add=True)
#
#    def __str__(self):
#        return "Accounting Manager - " + str(self.uname)
#
#    class Meta:
#        verbose_name_plural = "Accounting Managers"
