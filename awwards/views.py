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

    context={
        'projects':projects,
        'today':today,
        'site':site_of_day,
        'site_ratings':site_of_day_ratings
    }
    return render(request,'index.html',context)


def register_user(request):
  if request.method == "POST":
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, f'Account for username {username} successfully created.')
        return redirect('home_page')
  else:
      form = SignUpForm()
  return render(request, 'registration/registration_form.html', {'form': form})

  
def user_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                login(request, user)

                return HttpResponseRedirect(reverse("home_page"))
            else:
                return HttpResponseRedirect(reverse("user_login"))

        else:
            return HttpResponseRedirect(reverse("user_login"))
    else:
        return render(request, "registration/login_form.html", context={})