from django.shortcuts import redirect, render, get_object_or_404
from .models import  Team, Messages, Posts
from .models import Users, BlockUser, ViewPurchases, PointsBundle, MessageTemplates, BlockUser, ViewedProfile
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import datetime
from django.contrib.auth import *
from .forms import MessageForm
import hashlib
from dashboard.auth_backend import SHA2PasswordHasher
from .forms import UserForm, PointsBundleForm
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import PostForm
import os
from django.db import connections
import urllib.parse
from django.http import JsonResponse
from django.db.models import Q, Count
# from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Users, Match
from datetime import timedelta
import datetime
from dateutil import parser
from datetime import datetime, timedelta


now = datetime.now()

@login_required
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
@login_required
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

    # paginator = Paginator(view_purchases_data, 10)  # 10 items per page
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    return render(request, 'salesreport.html', {'view_purchases': view_purchases_data})

# @login_required
def MessageTemplate(request):
    messages = MessageTemplates.objects.all().order_by('-date_created')
    decoded_messages = [{'pk': message.pkmessage_template, 'value': urllib.parse.unquote(message.value)} for message in messages]
    
    return render(request, 'messagetemplate.html', {'messages': decoded_messages})

# @login_required
def PurchaseHistory(request):
    purchases = ViewPurchases.objects.all().order_by('-datetime')
    return render(request, 'purchasehistory.html', {'purchases': purchases})




@login_required
def ReportList(request): 
    reports = BlockUser.objects.filter(flags__in=[2, 3, 5]).order_by('-datetime')
    return render(request, 'reportlist.html', {'reports': reports})

@login_required
def Pricing(request):
    prices = PointsBundle.objects.all().order_by('-pkpoint_bundle')
    return render(request, 'pricing.html', {'prices': prices})

from django.shortcuts import render, redirect
from .models import PointsBundle

import logging
import pdb
logger = logging.getLogger(__name__)

def edit_points_bundle(request, pk):
    if request.method == 'POST':
        # Handle the POST request
        points_bundle = PointsBundle.objects.get(pk=pk)
        points_bundle.price = request.POST['price']
        points_bundle.name = request.POST['name']
        points_bundle.description = request.POST['description']
        points_bundle.save()
        return redirect('dashboard:Pricing')
    else:
        # Handle the GET request
        return render(request, 'pricing.html', {'prices': PointsBundle.objects.all()})




from django.core.cache import cache
@login_required
def UserList(request):
    # Check if the contact data is cached
    total_users = Users.objects.count()
    contact_data = cache.get('contact_data')
    sort = request.GET.get('sort')

    if sort is not None:
        # If the sort parameter is present, delete the cached data
        cache.delete('contact_data')

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
    sort_by = request.GET.get('sort_by')

    if sort_by == 'newest':
        users_with_post_count = sorted(users_with_post_count, key=lambda x: x['user'].pkuser, reverse=True)
    elif sort_by == 'oldest':
        users_with_post_count = sorted(users_with_post_count, key=lambda x: x['user'].pkuser)
   
    # Render the contact page with the contact data
    return render(request, 'userlist.html', {'users_with_post_count': users_with_post_count, 'total_users': total_users})
    
   
@receiver(post_save, sender=Users)
def invalidate_cache(sender, instance, **kwargs):
    cache.delete('contact_data')

@receiver(post_save, sender=Posts)
def invalidate_cache_on_post_save(sender, instance, **kwargs):
    cache.delete('contact_data')



@login_required
def AdminList(request):
    teams = Team.objects.all()
    users = Users.objects.all()
    return render(request, 'adminlist.html', {'users': users})






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


from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
import binascii
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
import hashlib

import mysql.connector

from django.contrib.auth import login

def loginpage(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Connect to the MySQL database
        cnx = mysql.connector.connect(
            user='dbmasteruser',
            password='oW-?ElK<,C~fo`e;3_;b[9svd<VdjEr2',
            host='ls-a6ea0c3b877a6923d6d9ca22364ab6ff3eb876b9.cleoey2mmxad.ap-southeast-1.rds.amazonaws.com',
            database='chatter'
        )

        # Create a cursor object
        cursor = cnx.cursor()

        # Call the stored procedure
        query = "CALL sp_Admin_Login(%s, %s)"
        cursor.execute(query, (email, password))

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        # Check if the result is not empty
        if result:
            # Extract the user_id, user_id_real, and nickname from the result
            user_id = result[0]
            user_id_real = result[1]
            nickname = result[2]

            # Create a Django user object
            from django.contrib.auth.models import User
            user = User.objects.get_or_create(username=user_id)[0]

            # Set the backend attribute on the user
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            # Log the user in
            login(request, user)

            # Return the user to the userlist page
            return redirect('dashboard:UserList')
        else:
            # Return an error message
            error_msg = 'Invalid username or password'
            return render(request, 'login.html', {'error_msg': error_msg})
    return render(request, 'login.html')

def logoutpage(request):
    logout(request)
    return redirect('/dashboard/login')


from django.utils import timezone

from dateutil import parser
import pytz
from datetime import datetime


@login_required
def UserProfile(request, pkuser):
    message_templates = [{'value': urllib.parse.unquote(template[0])} for template in MessageTemplates.objects.values_list('value')]
    user = get_object_or_404(Users, pk=pkuser)
    form = UserForm(instance=user, include_password_fields=True)
    message_form = MessageForm()  # New form for sending messages
    dummy_user = Users.objects.get(pk=1)  # Replace with a valid user ID
    request.user = dummy_user
    request.session['last_visited_profile_id'] = pkuser
    # Add the chat list logic here
    chat_users = Users.objects.filter(
        Q(pk__in=Messages.objects.filter(msg_to=user).values('msg_from')) |
        Q(pk__in=Messages.objects.filter(msg_from=user).values('msg_to'))
    ).distinct()

    chat_list = chat_users.annotate(
        msg_count=Count('messages', filter=Q(messages__msg_to=user, messages__read=0) | Q(messages__msg_from=user, messages__read=0))
    ).values('pk', 'nickname', 'name', 'msg_count')

    if request.method == 'POST':
        # print("Request method:", request.method)
        # print("Request POST:", request.POST)
        if 'add_points' in request.POST:
            point_type = request.POST.get('point_type')
            additional_points = int(request.POST.get('additional_points'))
            if point_type == 'calls':
                user.call_minutes += additional_points
            elif point_type == 'messages':
                user.mail_count += additional_points
            user.save()
            user = get_object_or_404(Users, pk=pkuser)  # Retrieve the updated user object
        elif 'send_message' in request.POST:  # New logic for sending messages
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                message = Messages(msg_from=request.user, msg_to=user, data=message_form.cleaned_data['data'], datetime=datetime.now().strftime('%Y-%m-%d  %I:%M %p'))
                message.save_to_db()
                return redirect('dashboard:UserProfile', pkuser=pkuser)
        elif 'send_to_all' in request.POST:
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                message_data = message_form.cleaned_data['data']
                for user in Users.objects.all():
                    if user != request.user:
                        message = Messages(msg_from=request.user, msg_to=user, data=message_data, datetime=datetime.datetime.now().strftime('%Y-%m-%d  %I:%M %p'))
                        message.save_to_db()
                return redirect('dashboard:UserProfile', pkuser=pkuser)
        else:
            form = UserForm(request.POST, instance=user, include_password_fields=True)
            message_form = MessageForm()  # Set message_form to a valid form instance
            if form.is_valid():
                print("Form is valid")
                print("Form data:", form.cleaned_data)
                print("New password:", form.cleaned_data.get('new_password'))
                form.save()

   # Add the chat display logic here
    conversation_user_id = request.GET.get('conversation_user')
    if conversation_user_id:
        conversation_user = get_object_or_404(Users, pk=conversation_user_id)
        messages = Messages.objects.filter(Q(msg_from=user, msg_to=conversation_user) | Q(msg_from=conversation_user, msg_to=user))
        for message in messages:
            
            
            if message.datetime:
                datetime_obj = datetime.strptime(message.datetime, '%Y-%m-%d %H:%M %p')
                date_string = datetime_obj.strftime('%Y-%m-%d %I:%M %p')
                date_parts = date_string.split(' ')
                if len(date_parts) >= 3:
                    date = date_parts[0]
                    time = date_parts[1]
                    am_pm = date_parts[2]
                    time_parts = time.split(':')
                    if len(time_parts) == 2:
                        hour, minute = time_parts
                        hour = int(hour)
                        minute = int(minute)
                    else:
                        hour = 0
                        minute = 0
                    if am_pm == 'PM' and hour != 12:
                        hour += 12
                    elif am_pm == 'AM' and hour == 12:
                        hour = 0
                    if hour > 23:  # handle invalid hour values
                        hour = 23
                    datetime_obj = datetime.strptime(f'{date} {hour}:{minute}', '%Y-%m-%d %H:%M')
                    if datetime_obj.tzinfo is None:
                                            datetime_obj = datetime_obj.replace(tzinfo=pytz.UTC)
                    message.datetime_obj = datetime_obj
                else:
                    message.datetime_obj = None
        messages = sorted(messages, key=lambda x: x.datetime_obj or datetime.min)
        print(messages)
    else:
        messages = []

    posts = Posts.objects.filter(fkuser=user)
    
    return render(request, 'userprofile.html', {
        'form': form,
        'user': user,
        'posts': posts,
        'pkuser': pkuser,
        'chat_list': chat_list,
        'messages': messages,
        'conversation_user': conversation_user if conversation_user_id else None,
        'message_form': message_form,
        'message_templates': message_templates,# Pass the message form to the template
    })


from django.core.cache import cache
@login_required
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




class DeletePostView(View):
    def post(self, request, pkpost):
        post = get_object_or_404(Posts, pk=pkpost)
        post.delete()
        last_visited_profile_id = request.session.get('last_visited_profile_id')
        if last_visited_profile_id:
            return redirect(reverse('dashboard:UserProfile', kwargs={'pkuser': last_visited_profile_id}))
        else:
            return redirect('dashboard:PostsList') # redirect to home page or any other page that doesn't require authentication
    




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

def edit_post_status(request, pk):
    post = Posts.objects.get(pk=pk)
    post.status = 1 - post.status  # toggle the status
    post.save()
    cache.delete('product_data')  # invalidate the cache
    return redirect('dashboard:PostsList')
def delete_user(request, pkuser):
    if request.method == 'POST':
        user = Users.objects.get(pk=pkuser)
        
        # Delete rows in match table that reference the user
        Match.objects.filter(user_to=user).delete()
        Match.objects.filter(user_from=user).delete()
        
        # Delete rows in messages table that reference the user
        Messages.objects.filter(msg_to=user).delete()
        Messages.objects.filter(msg_from=user).delete()

        ViewedProfile.objects.filter(fkviewer=user.pkuser).delete()
        ViewedProfile.objects.filter(fkviewed_profile=user.pkuser).delete()
        
        BlockUser.objects.filter(user_from=user.pkuser).delete()
        BlockUser.objects.filter(user_to=user.pkuser).delete()

        
        
        user.delete()
        return redirect(reverse('dashboard:delete_user', kwargs={'pkuser': pkuser}))
    else:
        return HttpResponse("Invalid request method")
    

def add_admin_member(request):
    if request.method == 'POST':
        strName = request.POST['name']
        strNickname = request.POST['nickname']
        strEmail = request.POST['email']
        strPassword = request.POST['password1']
        
        
        with connections['default'].cursor() as cursor:
            cursor.callproc('sp_Admin_Save', [strName, strNickname, strEmail, strPassword])
            
        return redirect('dashboard:AdminList')
    return render(request, 'register.html')
    

import json
def update_price(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        try:
            price_obj = PointsBundle.objects.get(pk=data['id'])
            
            if 'pkpoint_bundle' in data and data['pkpoint_bundle'] != '':
                price_obj.pkpoint_bundle = data['pkpoint_bundle']
            if 'price' in data:
                price_obj.price = data['price']
            if 'name' in data:
                price_obj.name = data['name']
            if 'description' in data:
                price_obj.description = data['description']
            
            price_obj.save()
            return JsonResponse({'status': 'success'})
        except PointsBundle.DoesNotExist:
            return JsonResponse({'status': 'error'})
    else:
        return JsonResponse({'status': 'error'})

def update_message(request, pk):
    message = get_object_or_404(MessageTemplates, pk=pk)
    if request.method == 'POST':
        message.value = request.POST['value']
        message.save()
    return redirect('dashboard:MessageTemplate')

def delete_message(request, pk):
    message = get_object_or_404(MessageTemplates, pk=pk)
    if request.method == 'POST':
        message.delete()
    return redirect('dashboard:MessageTemplate')

def add_message(request):
    if request.method == 'POST':
        value = request.POST['value']
        message = MessageTemplates(value=value)
        message.save()
    return redirect('dashboard:MessageTemplate')

def delete_admin(request, pk):
    user = get_object_or_404(Users, pk=pk)
    if request.method == 'POST':
        user.delete()
    return redirect('dashboard:AdminList')

from django.http import JsonResponse

def invalidate_cache(request):
    # Get the cache key from the request body
    cache_key = request.POST.get('cacheKey')

    # Invalidate the cache
    cache.delete(cache_key)

    # Return a JSON response indicating success
    return JsonResponse({'success': True})