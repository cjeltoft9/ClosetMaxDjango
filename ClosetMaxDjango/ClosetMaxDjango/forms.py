from django import forms
from .models import User, Clothes, Outfit

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
        }

class ClothesForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = ['user', 'clothing_type', 'material', 'size', 'brand', 'season', 'favorite']
        widgets = {
            'clothing_type': forms.TextInput(attrs={'placeholder': 'Type of clothing'}),
            'material': forms.TextInput(attrs={'placeholder': 'Material'}),
            'size': forms.NumberInput(attrs={'placeholder': 'Size'}),
            'brand': forms.NumberInput(),
            'season': forms.NumberInput(),
            'favorite': forms.NumberInput(),
        }

class OutfitForm(forms.ModelForm):
    class Meta:
        model = Outfit
        fields = ['favorite', 'clothes']
        widgets = {
            'favorite': forms.NumberInput(),
        }
