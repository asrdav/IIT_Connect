from django.contrib.auth.models import User
from django import forms
from .models import Item, CabService


# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         fields = ['profile_pic', ]


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


'''class UserLogoForm(forms.ModelForm):
    class Meta:
        model = UserLogo
        fields = ['user_logo']      '''


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'item_pic', 'item_description', 'item_tag', 'item_status']


class CabServiceForm(forms.ModelForm):
    class Meta:
        model = CabService
        fields = ['source', 'destination', 'date_time', 'book_status']



