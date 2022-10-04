from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext

class Home(View):
	def get(self, request):
		return render(request, 'base-reg.html')
