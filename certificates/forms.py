from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField()

class NameForm(forms.Form):
    name = forms.CharField(max_length=200)
