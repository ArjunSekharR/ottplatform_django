from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
from .models import MovieList,PlanModel, AdminLogin,Subscriber,Userhistory
from .forms import MovieForm,Forgotform,Planform,Confirmpassword,LoginForm
from django.http import JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

def loginpage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('movielist')
            else:
                messages.error(request, 'Your email and password are incorrect')
        return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
@login_required(login_url=('loginpage'))
def homepage(request):
    movies = MovieList.objects.all()
    paginator = Paginator(movies, 2)
    page_number = request.GET.get('page')
    
    try:
        movies = paginator.page(page_number)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    return render(request, 'homepage.html', {'movies': movies})

def confirmpassword(request):
    message = None
    if request.method == 'POST':
        form = Forgotform(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if AdminLogin.objects.filter(email=email).exists():
                user = AdminLogin.objects.get(email=email)
                token = get_random_string(length=32)
                user.forgotkey = token
                user.save()
                subject = "Click the link below to reset your password:"
                from_email = "arjun@gmail.com"
                recipient_list = [email]
                message_body = "http://127.0.0.1:8000/reset/" + token + "/"  
                send_mail(subject, message_body, from_email, recipient_list, fail_silently=True)
                message = {'status': 'Check your Email'}
            else:
                message = {'status': 'User with this email does not exist'}
    else:
        form = Forgotform()

    return render(request, 'resetpassword.html', {'message': message, 'form': form})


def forgotpassword(request, key):
    message = None
    if AdminLogin.objects.filter(forgotkey=key).exists():
        user = AdminLogin.objects.get(forgotkey=key)
        form = Confirmpassword(request.POST)
        if form.is_valid():
            pass1 = form.cleaned_data.get('password')
            pass2 = form.cleaned_data.get('confirmpassword')
            if pass1 == pass2:
                user.password = make_password(pass1)
                user.forgotkey = None
                user.save()
                return redirect('loginpage')
            else:
                message = {'status': 'Password does not match, try again'}
        else:
            form = Confirmpassword()
    else:
        return redirect('loginpage')
    return render(request, 'confirm.html', {'message': message, 'form': form})

# def changepassword(request,usr):
#     message = None
#     user = AdminLogin.objects.get(email = usr)
#     form = Confirmpassword(request.POST)
#     if form.is_valid():
#         pass1 = form.cleaned_data('password')
#         pass2 = form.cleaned_data('confirmpassword')
#         if pass1==pass2:
#             user.password = make_password(pass1)
#             user.save()
#             return redirect('loginpage')
#         else:
#             message = {'status':"password dosen't match try again"}
#     else:
#         form = confirmpassword()
#         return render(request,'confirm.html',{'message':message})


@login_required(login_url=('loginpage'))
def subs_plan(request):
    Plan = PlanModel.objects.all()
    return render(request, 'subscription_plan.html', {'plan': Plan})


def plantoogle(request, pk):
    plan = get_object_or_404(PlanModel, pk=pk)
    if request.method == 'POST':
        if plan.status == 'true':
            plan.status = 'false'
        else:
            plan.status = 'true'
        plan.save()
    return redirect('plans')
             

def search_movies(request):
    search_term = request.GET.get('search_term')
    movies = MovieList.objects.filter(title__icontains=search_term)

    html = ''
    for movie in movies:
        movie_edit = reverse('movie_edit', args=[movie.id])
        delete_movie = reverse('delete_movie', args=[movie.id])
        movie_view = reverse('movie_view', args=[movie.id])
        html += f'''
        <tr>
            <td>{movie.id}</td>
            <td>{movie.title}</td>
            <td>
                <a href="{movie_edit}" class="btn btn-secondary">Update</a>
                <button class="btn btn-danger btn-sm" data-toggle="modal" data-target="#deleteModal{movie.id}">Delete</button>
                <a href="{movie_view}" class="btn btn-primary">View</a>
            </td>
        </tr>
        '''

    return JsonResponse({'html': html})

@login_required(login_url=('loginpage'))
def addnew_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movielist')
    else:
        form = MovieForm()
    return render(request,'add_movie.html', {'form': form})

@login_required(login_url=('loginpage'))
def movie_edit(request, id):
    movie = get_object_or_404(MovieList, id=id)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movielist')
    else:
        form = MovieForm()
    return render(request, 'edit.html', {'form': form})

@login_required(login_url=('loginpage'))
def delete_movie(request, id):
    movie = get_object_or_404(MovieList, id=id)
    movie.delete()
    return redirect('movielist')

def movie_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginpage') 
    context = {
        'user': request.user
    }
    return render(request, 'logout.html', context)

@login_required(login_url=('loginpage'))
def movie_views(request, id):
    movie = get_object_or_404(MovieList, id=id)
    context = { 'movie': movie }
    return render(request, 'views.html', context)

@login_required(login_url=('loginpage'))
def add_plan(request):
    if request.method == 'POST':
        form = Planform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plans')
        else:
            print(form.errors)
    else:
        form = Planform()
    return render(request, 'add_plan.html', {'form': form})

@login_required(login_url=('loginpage'))
def plan_views(request,id):
     plan_movie = get_object_or_404(PlanModel,id=id )
     return render(request,'subplan_view.html',{'plan_movie':plan_movie})

@login_required(login_url=('loginpage'))
def user_list(request):
    user_list = AdminLogin.objects.filter(is_staff=0)
    return render(request, 'userlist.html', {'user_list': user_list})

def monthly_subs(request):
     return render(request,'monthly_subs.html')

def total_revenue(request):
     return render(request,'total_revenue.html')

def most_viewed(request):
     return render(request,'mostviewed.html')

def rated_movie(request):
     return render(request,'high_rate.html')

def watch_history(request, id):
    movie_subscribers = Subscriber.objects.filter(userid_id=id)
    watch_history = Userhistory.objects.filter(userid_id=id)
    return render(request, 'watchhistory.html', {'subscribers': movie_subscribers, 'history': watch_history})
   


