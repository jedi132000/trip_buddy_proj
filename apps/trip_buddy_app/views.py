from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Trip, User
import bcrypt
import re

def index (request):
    return render(request, 'trip_buddy_app/index.html')

def createUser(request):
    errors = User.objects.validate(request.POST)
    if errors :
        for key, value in errors.items():
            messages.error(request, value)
    else:
        user_id = User.objects.easy_create(request.POST)
        print(User.FirstName)
        print('*'*50)
        print(User.LastName)
        print('*'*50)
        print('*'*50)
    return redirect('/')


def validate_login(request):
    existing_users = User.objects.filter(email=request.POST['email'])
    # print(user.id) # make this work for emails that don't exist
    if len(existing_users) > 0:
        user = existing_users[0]
        if bcrypt.checkpw(request.POST['Password'].encode(), user.Password.encode()):
            print("password match")
            request.session['id']= user.id
            return redirect('/dashboard/')
    messages.error(request, "Email or password invalid")
    return redirect('/')

def dashboard(request):
    context = {
        "my_trip_list": Trip.objects.filter(creator=User.objects.get(id=request.session['id'])),
        "user": User.objects.get(id=request.session['id']),
        "other_users_list" : Trip.objects.exclude(creator=User.objects.get(id=request.session['id']))


        # "user_quotes": User.objects.filter(quotes=Quote.objects.get(id=creator_id),
        #  "others_trip_list" : Book.objects.exclude(authors=my_val),
    }
    print('#'*50)
    print(context['user'])
    # print(context['wish_list'][4].Item)
    return render(request,'trip_buddy_app/dashboard.html', context)

def validate_trip(request):
        errors = {}
        if len(form['Destination']) < 1:
            errors["Destination"] = "Destination should not be blank"
            print(errors)
        if len(form['Plan']) < 1:
            errors["Plan"] = "Plan should not be blank"
            print("*" * 50)
            print(errors)
        return redirect ('/dashboard/')

def addtrip(request):
    context = {
        "user": User.objects.get(id=request.session['id'])
    }
    print('#'*50)
    print(context['user'])
    
    return render(request,'trip_buddy_app/createtrip.html', context)

  

def createtrip(request):
    errors = Trip.objects.validate_trip(request.POST)
    if errors :
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ("/trips/new")
    else:
        trip_id = Trip.objects.easy_trip_create(request.POST,request.session['id'] )
        print(Trip.Destination)
        print('*'*50)
        print(Trip.Plan)
        print('*'*50)
        print(Trip.id)
    return redirect("/dashboard/")

def tripjoin(request, trip_id):
    context = {
     "join_trips" : Trip.objects.easy_trip_join(trip_id, request.session['id']),
     "my_trip_list": Trip.objects.filter(creator=User.objects.get(id=request.session['id'])),
     "user": User.objects.get(id=request.session['id']),
     "other_users_list" : Trip.objects.exclude(creator=User.objects.get(id=request.session['id']))
    }
    return render(request,'trip_buddy_app/dashboard.html', context)

def tripcancel(request, trip_id):
    Trip.objects.easy_trip_cancel(trip_id, request.session['id']),
    return redirect("/dashboard/")



def tripview(request, trip_id):
    context = {
        "user": User.objects.get(id=request.session['id']),
        "trip" : Trip.objects.get(id=trip_id),
        "other_users_trips": User.objects.filter(join_other_trip__creator=User.objects.get(id=request.session['id'])).exclude(id=request.session['id'])
    }
    print('#'*50)
    print(context['trip'])
    return render(request,'trip_buddy_app/tripview.html', context)

# def tripjoin(request, trip_id):
#     this_user = User.objects.get(id=request.session['id'])
#     this_trip =  Trip.objects.get(id=trip_id)
#     context = {
#         'join_trip' : this_trip.join_trip.add(this_user),
#     }
#     print('#'*50)
#     print(context['trip'])
#     return render (request,'trip_buddy_app/dashboard.html', context )


def deletetrip(request, trip_id):
    Trip.objects.easy_trip_delete(trip_id)
    return redirect('/dashboard/')

def logout(request):
    request.session.clear()
    return redirect('/')










