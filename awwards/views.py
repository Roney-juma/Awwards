from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm,ProjectForm,RatingsForm,UserProfileForm
from django.http  import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Project,Rating,Profile
import datetime
import random

# Create your views here.

def home_page(request):
    projects=Project.get_all_projects()
    today = datetime.date.today()
    ratings= Rating.objects.all()
    prjs= [p.project for p in ratings]
    site_of_day=random.choice(prjs)
    site_of_day_ratings=get_project_ratings_av(site_of_day.id)
