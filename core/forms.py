from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Group, Member, Cycle


class SignUpForm(UserCreationForm):
  name = forms.CharField(max_length=100)
  last_name = forms.CharField(max_length=100)
  email = forms.EmailField()
  class Meta:
    model = User
    fields = ['username', 'password1', 'password2']

class GroupForm(forms.ModelForm):
  class Meta:
    model = Group
    fields = ['name', 'amount']

class AddMemberForm(forms.Form):
  member = forms.ModelChoiceField(queryset=Member.objects.all())


class CycleForm(forms.ModelForm):
  class Meta:
    model = Cycle
    fields = ['start_date',]