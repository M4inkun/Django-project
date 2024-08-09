from django.shortcuts import render
from django.http import HttpResponse


def login_users(request):
    return HttpResponse('login')


def logout_users(request):
    return HttpResponse('logout')