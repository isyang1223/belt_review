from __future__ import unicode_literals
from django.db import models
import re 
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z\s]+$')
# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['name']) < 1:
            errors["name"] = "User's name cannot be empty!"
        if len(postData['alias']) < 1:
            errors["alias"] = "User's alias name cannot be empty!"
        if not NAME_REGEX.match(postData['name']):
            errors["name"] = "User's name cannot contain any numbers or special characters!"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email/Password!"
        if len(postData['password']) < 8:
            errors["password"] = "Invalid Email/Password!"
        if not postData['password'] == postData['password2']:
            errors["password2"] = "Password is not matching with confirm password!"
        if len(User.objects.filter(email=postData["email"])) > 0:
            errors["email"] = "Email already exist"
        if len(errors) == 0:
            hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name=postData['name'], alias=postData['alias'], email=postData['email'], password=hash1 )
            errors['user'] = user
        return errors

    def login_validator(self, postData):
        errors={}
        checklogin= User.objects.filter(email=postData["logemail"])
        if checklogin:
            if bcrypt.checkpw(postData['password'].encode(), checklogin[0].password.encode()) == True:
                errors["user"]=checklogin[0]
            else:
                errors["errorsuser"]="Login failed"
        else:
            errors["errorsuser"]="Login failed"
        return errors


    def book_validator(self, postData):
        errors={}
        checkbook= Book.objects.filter(title=postData["title"])
        print "*****************", checkbook

        if checkbook:
            errors["exist"] = "This book already exists"
            return errors
 
   
        if len(postData['add_author']) > 0:
            
            a = Book.objects.create(title=postData['title'], author=postData['add_author'], uploader_id=int(postData['huploader_id']))
            Review.objects.create(content=postData["content"], rating=postData['rating'], bookreview_id=a.id, reviewer_id=int(postData['huploader_id']))
            errors["book"] = a
        else:
            a = Book.objects.create(title=postData['title'], author=postData['authorlist'], uploader_id=int(postData['huploader_id']))
            Review.objects.create(content=postData["content"], rating=postData['rating'], bookreview_id=a.id, reviewer_id=int(postData['huploader_id']))
            errors["book"] = a
        return errors
        

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length = 255)
    author = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    uploader = models.ForeignKey(User, related_name="books_uploaded")
    objects = UserManager()
    
class Review(models.Model):
    content = models.TextField(default="")
    rating = models.IntegerField(default=1)
    reviewer = models.ForeignKey(User, related_name="user_reviews")
    bookreview = models.ForeignKey(Book, related_name="book_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()
    


    