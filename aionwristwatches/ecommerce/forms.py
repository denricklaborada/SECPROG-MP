from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import Textarea, widgets
from .models import Review

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    middle_initial = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.CharField(required=True)
    bhouse_num = forms.IntegerField(required=True, min_value=1)
    bstreet = forms.CharField(required=True)
    bsubdivision = forms.CharField(required=True)
    bcity = forms.CharField(required=True)
    bpc = forms.IntegerField(required=True, min_value=1)
    bcountry = forms.CharField(required=True)
    shouse_num = forms.IntegerField(required=True, min_value=1)
    sstreet = forms.CharField(required=True)
    ssubdivision = forms.CharField(required=True)
    scity = forms.CharField(required=True)
    spc = forms.IntegerField(required=True, min_value=1)
    scountry = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'middle_initial',
            'last_name',
            'password1',
            'password2',
            'email',
            'bhouse_num',
            'bstreet',
            'bsubdivision',
            'bcity',
            'bpc',
            'bcountry',
            'shouse_num',
            'sstreet',
            'ssubdivision',
            'scity',
            'spc',
            'scountry',
        ]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.middle_initial = self.cleaned_data['middle_initial']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.bhouse_num = self.cleaned_data['bhouse_num']
        user.bstreet = self.cleaned_data['bstreet']
        user.bsubdivision = self.cleaned_data['bsubdivision']
        user.bcity = self.cleaned_data['bcity']
        user.bpc = self.cleaned_data['bpc']
        user.bcountry = self.cleaned_data['bcountry']
        user.shouse_num = self.cleaned_data['shouse_num']
        user.sstreet = self.cleaned_data['sstreet']
        user.ssubdivision = self.cleaned_data['ssubdivision']
        user.scity = self.cleaned_data['scity']
        user.spc = self.cleaned_data['spc']
        user.scountry = self.cleaned_data['scountry']
        if commit:
            user.save()

        return user
    


STAR_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]
class ReviewForm(forms.ModelForm):
    rating = forms.CharField(label='', widget=forms.RadioSelect(attrs={'class':'id_rating'}, choices=STAR_CHOICES))
    class Meta:
        model = Review
        exclude = [
            'product',
            'user',
        ]
        fields = [
            'comment',
            'rating',
        ]
        widgets = {
            'comment': Textarea(attrs={'cols':80, 'rows':20, 'placeholder':'Write your review here...'}),
            #'rating': forms.TextInput('required': True),
        }
        labels = {
            'comment': '',
        }