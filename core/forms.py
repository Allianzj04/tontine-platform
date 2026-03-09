from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Groupe


class InscriptionForm(UserCreationForm):
  nom = forms.CharField(max_length=100)
  prenom = forms.CharField(max_length=100)
  email = forms.EmailField()
  class Meta:
    model = User
    fields = ['username', 'password1', 'password2']

class GroupeForm(forms.ModelForm):
  class Meta:
    model = Groupe
    fields = ['nom', 'montant_cotisation']