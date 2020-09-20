from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import datetime 

class Search(forms.Form): 
    search_form = forms.CharField(label='SEARCH', max_length=40, required=True)


# Create your views here.
