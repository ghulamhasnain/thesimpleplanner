import http
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin

from . import forms
from .models import *

class Home(View):
	def get(self, request):
		return render(request, 'base-reg.html')

class SignupView(View):
	def get(self, request):
		form = forms.SignUpForm()
		return render(request, 'registration/signup.html', {'form': form})
	
	def post(self, request):
		from django.contrib.auth.models import User
		from django.contrib.auth import login, authenticate
		from django.contrib.auth.forms import UserCreationForm

		form = forms.SignUpForm(request.POST)
		if form.is_valid():
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			email = form.cleaned_data.get('email')
			password1 = form.cleaned_data.get('password1')
			if not User.objects.filter(email=email).exists():
				newUser = User.objects.create_user(username=email,
                                                    first_name=first_name,
                                                    last_name=last_name,
                                                    email=email,
                                                    password=password1)
				newUser.save()
				account = Account(user=newUser)
				account.save()
				user = authenticate(username=email, password=password1)
				login(request, user)
				return redirect('/planning/dashboard')
			else:
				form.errors['email'] = ['This user already exists.']
				return render(request, 'registration/signup.html', {'form': form})
		else:
			return render(request, 'registration/signup.html', {'form': form})

class EditAccount(LoginRequiredMixin, View):
	def get(self, request):
		try:
			account = Account.objects.get(user__username = request.user.username)
		except:
			account = Account()
			account.user = request.user
			account.currency = "£"
			account.save()
		return render(request, 'account.html', {'account': account})
	
	def post(self, request):
		user = request.user
		account = Account.objects.get(user__username = request.user.username)
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')
		currency = request.POST.get('currency')
		account_change = False
		user_change = False
		message = False
		if account.currency != currency:
			account.currency = currency
			account_change = True
		if user.first_name != first_name or user.last_name != last_name:
			user.first_name = first_name
			user.last_name = last_name
			user_change = True
		if account_change:
			account.save()
			message = 'Account information changed'
		if user_change:
			user.save()
			message = 'Account information changed'
		return render(request, 'account.html', {'account': account, 'message': message})