from django.db import models
import bcrypt
import re
from datetime import datetime, timedelta

class UserManager(models.Manager):
    def validate(self, form):
        EMAIL_REGEX = re.compile(r'^[a-z A-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        REGTEX = re.compile(r'^[a-z A-Z]{2,}$')
        REGPASSWD = re.compile(r'^[a-z A-Z0-9.+_-]{8,}$')
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if not REGTEX.match(form['FirstName']) :
            errors["FirstName"] = "First Name should be at least 2 characters"
            print(errors)
        if not REGTEX.match(form['LastName']) :
            errors["LastName"] = "Last Name should be at least 2 alphabetical characters"
        if not EMAIL_REGEX.match(form['email']): 
            errors['email'] = "Email not in valid format"
        if not REGPASSWD.match(form['Password']) :
            errors['password'] = "Password should be at least 8 "
        print("*" * 50)
        print(errors)
        return errors

    def easy_create(self, form):
        pw_hash = bcrypt.hashpw(form['Password'].encode(), bcrypt.gensalt())
        user = User.objects.create(
            FirstName=form['FirstName'],
            LastName=form['LastName'],
            email=form['email'],
            Password = pw_hash
            )
        return user.id

   
    def easy_update(self, form, user_id):
        user = User.objects.get(id=user_id)
        user.FirstName = form['FirstName']
        user.LastName = form['LastName']
        user.email = form['email']
        user.save()

class User(models.Model):
    FirstName = models.CharField(max_length=45)
    LastName = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    Password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
    def __repr__(self):
        return f"User: {self.FirstName} ({self.LastName})"
    
    def __str__(self):
        return f"User: {self.FirstName} ({self.LastName})"


class TripManager(models.Manager):
    def validate_trip(self, form):
        errors = {}
        if len(form["Destination"]) < 1:
            errors["Destination"] = "Destination cant be blank"
            print(errors)
        if len(form['Plan']) < 1:
            errors["Plan"] = "Plan should not be blank"
            print("*" * 50)
            print(errors)
        return errors
    
    def easy_trip_create(self, form, user_id):
        trip = Trip.objects.create(
            Destination=form['Destination'],
            start_date=form['start_date'],
            end_date=form['end_date'],
            Plan=form['Plan'],
            creator=User.objects.get(id=user_id),
            )
        trip.join_trip.add(User.objects.get(id=user_id))
        return trip.id
        
          

    def easy_trip_join(self, trip_id):
         trip=Trip.objects.get(id=trip_id)
         print("*" * 50)
         print(trip)
         print("*" * 50)
         print(user)
         print("*" * 50)
         trip.join_trip.add(user)
         trip.save()
    
    def easy_trip_cancel(self, trip_id, user_id):
         trip=Trip.objects.get(id=trip_id)
         user = User.objects.get(id=user_id)
         print("*" * 50)
         print(trip)
         print("*" * 50)
         print(user)
         print("*" * 50)
         trip.join_trip.remove(user)
         trip.save()

    def easy_trip_update (self, form, trip_id):
        trip = Trip.objects.get(id=trip_id)
        trip.Destination = form['Destination']
        trip.start_date = form['start_date']
        trip.end_date = form['end_date']
        trip.Plan = form['Plan']
        print("*" * 50)
        print(trip.Destination)
        print("*" * 50)
        print("*" * 50)
        print(trip.start_date)
        print("*" * 50)
        print("*" * 50)
        print(trip.end_date)
        print("*" * 50)
        print("*" * 50)
        print(trip.Plan)
        print("*" * 50)
        trip.save()
    
    
    def easy_trip_delete(self, trip_id):
        trip = Trip.objects.get(id=trip_id)
        trip.delete()

class Trip(models.Model):
    Destination = models.CharField(max_length=255)
    start_date= models.DateTimeField(auto_now_add=True)
    end_date= models.DateTimeField()
    Plan = models.TextField()
    creator = models.ForeignKey(User, related_name="trips")
    join_trip = models.ManyToManyField(User, related_name="join_other_trip")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

    def __repr__(self):
        return f"Trip: {self.Destination} ({self.Plan}   ({self.start_date})"
      

    def __str__(self):
        return f"<Trip: {self.Destination}  ({self.Plan} ({self.start_date} )>"