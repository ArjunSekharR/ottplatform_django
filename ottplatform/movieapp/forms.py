from django import forms
from .models import MovieList,AdminLogin,PlanModel


class MovieForm(forms.ModelForm):
    class Meta:
        model = MovieList
        fields = ['title','description','thumbnail','video']

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)


class Planform(forms.ModelForm):
    class Meta:
        model = PlanModel
        fields = ['name', 'description', 'price', 'duration', 'status']

class Forgotform(forms.Form):
        email = forms.EmailField(label="Email",max_length=254)

class Confirmpassword(forms.Form):
     password = forms.CharField(max_length=200)
     confirm = forms.CharField(max_length=200)




