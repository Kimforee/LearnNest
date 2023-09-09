from .forms import NestForm
from django.db.models import Q
from django.contrib import messages
from . models import Nest, Topic, Message, JoinRequest
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.

# nests = [
#     {'id':1,'name':'Java Fundamental'},
#      {'id':2,'name':'Spring-Boot Introdction'},
#       {'id':3,'name':'Python Software Development'},
# ]

def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # email = request.POST.get('email')
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
              user = User.objects.get(username=username)
        except:
              messages.error(request, 'User does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
           login(request,user)
           return redirect('home')
        else:
           messages.error(request, ' Password incorrect',fail_silently=True)

    context = {'page':page}
    return render(request,'LearnNest/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred while registering')    
            # user = form.cleaned_data['user']
    return render(request,'LearnNest/login_register.html',{'form':form})

def home(request): 
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    nests = Nest.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username__icontains=q)
        )

    topics = Topic.objects.all()
    nest_count = nests.count()
    nest_messages = Message.objects.filter(Q(nest__topic__name__icontains=q))

    context =  {'nests': nests, 'topics': topics, 'nest_count': nest_count, 'nest_messages': nest_messages}
    return render(request, 'LearnNest/home.html', context)

@login_required(login_url='login')
def nest(request, pk):
    nest = Nest.objects.get(id=pk)
    nest_messages = nest.message_set.all().order_by('-created')
    participants  = nest.participants.all()
    join_request  = None

    try:
        join_request = JoinRequest.objects.get(user=request.user, nest=nest)
    except JoinRequest.DoesNotExist:
        pass

    if join_request and  join_request.is_accepted:
        nest.participants.add(request.user)
        
    if request.method == 'POST':
        if 'body' in request.POST:
            if (request.user in nest.participants.all()) or (request.user.username == nest.host.username):
            # Handle sending a message
                message = Message.objects.create(
                    user=request.user,
                    nest=nest,
                    body=request.POST.get('body'),
                )
                nest.participants.add(request.user)
                return redirect('nest', pk=nest.id)
            else:
                messages.error(request, 'You are not a member of this nest ! click join nest to join now !')

        elif 'join_request' in request.POST:
            # Handle sending a join request
            if not join_request:
                messages.success(request, "Your request sent successfully !.")
                JoinRequest.objects.create(user=request.user, nest=nest)

    context = {'nest': nest, 'nest_messages': nest_messages,'participants': participants}
    return render(request, 'LearnNest/nest.html',context)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    nest_message =  user.message_set.all()
    topics = Topic.objects.all()
    nests = user.nest_set.all()
    context  = {'user':user,'nests':nests,'topics':topics,'nest_message':nest_message } 
    return render(request, 'LearnNest/profile.html',context)

@login_required(login_url='login')
def createNest(request):
    form = NestForm()
    if request.method == 'POST':
        print(request.POST)
        form = NestForm(request.POST)
        if form.is_valid():
            nest = form.save(commit=False)  # Don't save to the database yet
            nest.host = request.user
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'LearnNest/nest_form.html',context)

@login_required(login_url='login')
def updateNest(request, pk):
    nest = Nest.objects.get(id=pk)
    form = NestForm(instance=nest)
     
    if request.method == 'POST':
        form = NestForm(request.POST, instance=nest)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'LearnNest/nest_form.html', context)

@login_required(login_url='login')
def deleteNest(request, pk):
    nest = Nest.objects.get(id=pk)

    if request.user != nest.host:
        return HttpResponse('You are not allowed to delete !')

    if request.method == 'POST':
        nest.delete()
        return redirect('home')
    return render(request, 'LearnNest/delete.html', {'obj':nest})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed to delete !')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'LearnNest/delete.html', {'obj':message})

def acccept_join_request(request,pk):
    join_request = JoinRequest.objects.get(id=pk)
    
    if request.method == 'POST':
        # participants  = request.user.nest.participants.all()
        join_request.is_accepted = True
        join_request.save()
        # nest.participants.add(request.user)
        return redirect('nest', pk=join_request.nest.pk)
    else:
        messages.error(request, 'Some error occurred !')
    

def reject_join_request(request,pk):

    if request.method == 'POST':
        join_request = JoinRequest.objects.get(id=pk)
        join_request.delete()
        return redirect('nest', pk=join_request.nest.pk)

    else:
        messages.error(request, 'Some error occurred !')
        return render(request, 'LearnNest/all_requests.html',context)

def allRequests(request, pk):
    nest = Nest.objects.get(id=pk)
    if request.user != nest.host:
        messages.error(request, 'Access denied !')
        # Only the host should be able to access this view
    join_requests = JoinRequest.objects.filter(nest=nest)
    context = {'join_requests': join_requests}
    return render(request, 'LearnNest/all_requests.html',context)

# def joinNest(request, pk):
#     nest = Nest.objects.get(id=pk)
#     user = request.user


def flashMessage(request):
    messages.success(request, "Your request sent successfully !.")
    flash_message = "Your request for joining this Nest has been sent successfully !"
    return render(request, 'LearnNest/flash_message.html',{"flash_message": flash_message})