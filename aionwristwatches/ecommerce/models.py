from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

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
