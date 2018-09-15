from django.shortcuts import render, redirect
from django.db.models import Q

import control.models as modelos
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# from control.forms import PersonalForm, ControlHorasForm
from django.contrib import messages
import datetime

# from django import forms

def index(request):
    
    return render(request, "index.html")