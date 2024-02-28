from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
# Create your views here.

menu =[{'title': "Collection", 'urrll': 'about'}, {'title': "Shop", 'urrll': 'index.html'},
       {'title': "Offer", 'urrll': 'index.html'}, {'title': "Blog", 'urrll': 'index.html'}
]

fmenu =[{'title': "Infomation"},{'title': "Start a Return"},{'title': "Contact Us"},
        {'title': "Shipping FAQ"},{'title': "Terms & Conditions"},{'title': "Privacy Policy"}]

def services(request):
    return render(request, 'index1.html', {"menu": menu, "fmenu":fmenu})

def index(request):
    return render(request, 'index.html', {"menu": menu, "fmenu":fmenu})