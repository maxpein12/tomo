from django.shortcuts import redirect, render, get_object_or_404
from .models import Client, Team, Product, Orders, Messages, Posts
from .models import Users, BlockUser, ViewPurchases, PointsBundle, MessageTemplates
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import datetime
from django.contrib.auth import *
import hashlib
from dashboard.auth_backend import SHA2Backend
from .forms import UserForm, PointsBundleForm
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import PostForm
import os
import urllib.parse
from django.http import JsonResponse





now = datetime.datetime.now()

def SalesChart(request):
    year = request.GET.get('year', now.year)
    orders = ViewPurchases.objects.all().order_by('-datetime')

    orders_january = ViewPurchases.objects.filter(datetime__month='1', datetime__year=year).aggregate(total=Sum('price'))
    orders_february = ViewPurchases.objects.filter(datetime__month='2', datetime__year=year).aggregate(total=Sum('price'))
    orders_march = ViewPurchases.objects.filter(datetime__month='3', datetime__year=year).aggregate(total=Sum('price'))
    orders_april = ViewPurchases.objects.filter(datetime__month='4', datetime__year=year).aggregate(total=Sum('price'))
    orders_may = ViewPurchases.objects.filter(datetime__month='5', datetime__year=year).aggregate(total=Sum('price'))
    orders_june = ViewPurchases.objects.filter(datetime__month='6', datetime__year=year).aggregate(total=Sum('price'))
    orders_july = ViewPurchases.objects.filter(datetime__month='7', datetime__year=year).aggregate(total=Sum('price'))
    orders_august = ViewPurchases.objects.filter(datetime__month='8', datetime__year=year).aggregate(total=Sum('price'))
    orders_september = ViewPurchases.objects.filter(datetime__month='9', datetime__year=year).aggregate(total=Sum('price'))
    orders_october = ViewPurchases.objects.filter(datetime__month='10', datetime__year=year).aggregate(total=Sum('price'))
    orders_november = ViewPurchases.objects.filter(datetime__month='11', datetime__year=year).aggregate(total=Sum('price'))
    orders_december = ViewPurchases.objects.filter(datetime__month='12', datetime__year=year).aggregate(total=Sum('price'))

    return render(request, 'saleschart.html', {
        'orders': orders,
        'orders_january': orders_january,
        'orders_february': orders_february,
        'orders_march': orders_march,
        'orders_april': orders_april,
        'orders_may': orders_may,
        'orders_june': orders_june,
        'orders_july': orders_july,
        'orders_august': orders_august,
        'orders_september': orders_september,
        'orders_october': orders_october,
        'orders_november': orders_november,
        'orders_december': orders_december,
        'year': year
    })





from django.core.cache import cache

from django.core.paginator import Paginator

def SalesReport(request):
    cache_key = 'view_purchases_data'
    view_purchases_data = cache.get(cache_key)

    if view_purchases_data is None:
        view_purchases = ViewPurchases.objects.all().order_by('-datetime')
        view_purchases_data = []

        for view_purchase in view_purchases:
            user = Users.objects.get(pk=view_purchase.fkuser)
            view_purchase_data = {
                'pkpurchase': view_purchase.pk,
                'datetime': view_purchase.datetime,
                'product_name': view_purchase.bundle_name,
                'name': view_purchase.name,
                'email': user.email,
            }
            view_purchases_data.append(view_purchase_data)

        cache.set(cache_key, view_purchases_data, 60 * 60)  # Cache for 1 hour

    paginator = Paginator(view_purchases_data, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'salesreport.html', {'view_purchases': page_obj})


def MessageTemplate(request):
    messages = MessageTemplates.objects.all().order_by('-date_created')
    decoded_messages = [{'pk': message.pkmessage_template, 'value': urllib.parse.unquote(message.value)} for message in messages]
    
    return render(request, 'messagetemplate.html', {'messages': decoded_messages})


def PurchaseHistory(request):
    purchases = ViewPurchases.objects.all().order_by('-datetime')
    return render(request, 'purchasehistory.html', {'purchases': purchases})





def ReportList(request): 
    reports = BlockUser.objects.filter(flags__in=[2, 3, 5]).order_by('-datetime')
    return render(request, 'reportlist.html', {'reports': reports})


def Pricing(request):
    prices = PointsBundle.objects.all().order_by('-pkpoint_bundle')
    return render(request, 'pricing.html', {'prices': prices})

def edit_points_bundle(request, pk):
    points_bundle = PointsBundle.objects.get(pk=pk)
    if request.method == 'POST':
        form = PointsBundleForm(request.POST, instance=points_bundle)
        if form.is_valid():
            form.save()
            return redirect('points_bundles')  # redirect to the points bundles page
    else:
        form = PointsBundleForm(instance=points_bundle)
    return render(request, 'edit_points_bundle.html', {'form': form})


def calendar(request):
    return render(request, 'calendar.html')


def todo(request):
    return render(request, 'to-do.html')


from django.core.cache import cache

def UserList(request):
    # Check if the contact data is cached
    total_users = Users.objects.count()
    contact_data = cache.get('contact_data')
    sort = request.GET.get('sort')

    if contact_data is None:
        # If the contact data is not cached, retrieve it from the database
        users = Users.objects.all()
        users_with_post_count = []

        for user in users:
            post_count = Posts.objects.filter(fkuser=user).count()
            profile_photo = ''
            try:
                profile_photo = Users.objects.get(pk=user.pk).profile_photo
            except:
                pass
            users_with_post_count.append({'user': user, 'post_count': post_count, 'profile_photo': profile_photo})
            
        # Cache the contact data for 1 hour
        cache.set('contact_data', users_with_post_count, 60 * 60)
    else:
        # If the contact data is cached, use it
        users_with_post_count = contact_data

    # Sort the contact data based on the selected option
    if sort == 'newest':
        users_with_post_count = sorted(users_with_post_count, key=lambda x: x['user'].pk, reverse=True)
    
    elif sort == 'oldest':
        users_with_post_count = sorted(users_with_post_count, key=lambda x: x['user'].pk)
    
    # Render the contact page with the contact data
    return render(request, 'userlist.html', {'users_with_post_count': users_with_post_count, 'total_users': total_users})
   


def invoice(request):
    orders = Orders.objects.all().order_by('-date')
    
    return render(request, 'invoice.html', {'orders': orders})

def ui(request):    
    return render(request, 'ui.html')


def AdminList(request):
    teams = Team.objects.all()
    users = Users.objects.all()
    return render(request, 'adminlist.html', {'users': users})



def table(request):
    return render(request, 'table.html')



# def register(request):
    # username = email = password = None
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     email = request.POST['email']
    #     password = request.POST['password']
    #     new_user = User.objects.create_user(username, email, password)
    #     new_user.save()
    #     return redirect('/dashboard/team')
    
    # return render(request, 'register.html')
    


def clientRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        gender = request.POST['gender']
        new_client = Client.objects.create(name=name, age=age, username=username , email=email, gender=gender)
        new_client.save()
        return redirect('contact')
    return render(request, 'register.html')


import hashlib

def loginpage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = Users.objects.get(email=email)
            salt = user.salt  # assuming you have a 'salt' field in your Users model
            hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
            if hashed_password == user.password and user.type == 0:
                # Login the user
                login(request, user)
                print("Login successful! Redirecting to index page...")
                return redirect('/dashboard')
            else:
                print("Password is incorrect")
        except Users.DoesNotExist:
            print("Email does not exist")
        error_msg = 'Invalid username or password'
        return render(request, 'login.html', {'error': error_msg})
    return render(request, 'login.html')


def logoutpage(request):
    logout(request)
    return redirect('/dashboard/login')






def UserProfile(request, pkuser):
    user = get_object_or_404(Users, pk=pkuser)
    form = UserForm(instance=user, include_password_fields=True)

    if request.method == 'POST':
        if 'add_points' in request.POST:
            point_type = request.POST.get('point_type')
            additional_points = int(request.POST.get('additional_points'))
            if point_type == 'calls':
                user.call_minutes += additional_points
            elif point_type == 'messages':
                user.mail_count += additional_points
            user.save()
            user = get_object_or_404(Users, pk=pkuser)  # Retrieve the updated user object
        else:
            form = UserForm(request.POST, instance=user, include_password_fields=True)
            if form.is_valid():
                if form.cleaned_data.get('new_password'):
                    from django.contrib.auth.hashers import make_password
                    user.password = make_password(form.cleaned_data.get('new_password'))
                user.name = form.cleaned_data.get('name')
                user.email = form.cleaned_data.get('email')
                user.gender = form.cleaned_data.get('gender')
                user.status = form.cleaned_data.get('status')
                user.age_verified = form.cleaned_data.get('age_verified')
                user.call_minutes = form.cleaned_data.get('call_minutes')
                user.mail_count = form.cleaned_data.get('mail_count')
                user.save()

    posts = Posts.objects.filter(fkuser=user)

    return render(request, 'userprofile.html', {'form': form, 'user': user, 'posts': posts, 'pkuser': pkuser})


from django.core.cache import cache

def PostsList(request):
    # Check if the product data is cached
    product_data = cache.get('product_data')

    if product_data is None:
        # If the product data is not cached, retrieve it from the database
        posts = Posts.objects.all().order_by('-datetime')

        # Cache the product data for 1 hour
        cache.set('product_data', posts, 60 * 60)
    else:
        # If the product data is cached, use it
        posts = product_data

    return render(request, 'postslist.html', {'posts': posts})

# def update_user(request, pkuser):
#     user = Users.objects.get(pk=pkuser)
#     if request.method == 'POST':
#         form = UserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return render(request, 'test.html', {'user': user})
#     else:
#         form = UserForm(instance=user)
#     return render(request, 'test.html', {'form': form})


class DeletePostView(LoginRequiredMixin, View):
    def post(self, request, pkpost):
        post = get_object_or_404(Posts, pk=pkpost)
        post.delete()
        return render (request, 'test.html')  # Replace 'home' with the URL of the home page
    


# class NewPostView(LoginRequiredMixin, View):
#     def post(self, request):
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.fkuser = request.user
#             post.save()
#             return redirect('home')  # Replace 'home' with the URL of the home page
#         return HttpResponse('Invalid form data', status=400)

def update_total_users_count(request):
    filter_value = request.POST.get('filter')
    if filter_value == 'all':
        total_users = Users.objects.all().count()
    elif filter_value == 'online':
        total_users = Users.objects.filter(status=1).count()
    elif filter_value == 'offline':
        total_users = Users.objects.filter(status=0).count()
    elif filter_value == 'unregistered':
        total_users = Users.objects.filter(age_verified=0).count()
    elif filter_value == 'checking':
        total_users = Users.objects.filter(age_verified=2).count()
    elif filter_value == 'It was not accepted due to a comprehensive judgement.':
        total_users = Users.objects.filter(age_verified=3).count()
    elif filter_value == 'verified':
        total_users = Users.objects.filter(age_verified=1).count()
    elif filter_value == 'newest':
        total_users = Users.objects.all().order_by('-pk').count()
    elif filter_value == 'oldest':
        total_users = Users.objects.all().order_by('pk').count()
    return JsonResponse({'total_users': total_users})