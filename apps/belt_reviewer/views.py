from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    
    return render(request,'belt_reviewer/index.html')

def home(request):
    if not "logged_id" in request.session:
        return redirect("/")

    key = Review.objects.all().order_by("-created_at")
    key2= Book.objects.all()
    data = {
        "loggeduser": User.objects.get(id=request.session["logged_id"]),
        "recentbook": key[:3],
        "allbook": key2
    }
    return render(request,'belt_reviewer/home.html', data)

def login(request):
    if request.method == 'POST':
        checklogin = User.objects.login_validator(request.POST)
        if "user" in checklogin:
            request.session["logged_id"] = checklogin["user"].id
            request.session["idk"] = "logged in"
            return redirect('/books')
        else:
            for tag, error in checklogin.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        
    else:
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")


def registration(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if "user" in errors: 
            request.session["idk"] = "registered"
            request.session["logged_id"] = errors["user"].id
            return redirect('/books')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
    else:
        return redirect("/")


def add(request):
    if not "logged_id" in request.session:
        return redirect("/")
    context={
        "mfauthors": Book.objects.all()
    }
    return render(request,'belt_reviewer/add.html', context)

def processadd(request):
    if not "logged_id" in request.session:
        return redirect("/")
    if request.method == 'POST':
        errors = Book.objects.book_validator(request.POST)
    
        if "exist" in errors:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/books/add')
        if "book" in errors:

            return redirect("/books/"+str(errors["book"].id))
    
def users(request, id):
    if not "logged_id" in request.session:
        return redirect("/")
   
    key= User.objects.get(id=id)
    key1=key.user_reviews.all()
    data={
            "loggeduser": key,
            "usersreviews": key1,
            "countreviews": len(key1),
    }
    
    return render(request,'belt_reviewer/showuser.html', data) 

def showbook(request, id):
    if not "logged_id" in request.session:
        return redirect("/")
    key= Book.objects.get(id=id)
    key1= Review.objects.filter(bookreview_id=id)
    request.session["currentbook"]= key.id
    data={
        "book": key,
        "review": key1
    }

    return render(request,'belt_reviewer/showbook.html', data) 

def addreview(request, id):
    
    Review.objects.create(content=request.POST["content"], rating=request.POST["rating"], bookreview_id=id, reviewer_id=request.POST['ruploader_id'])
    key = Review.objects.filter(bookreview_id=id)
    data={
        "review": key,
    }

    return redirect("/books/"+id, data)
def deletereview(request, id):
    Review.objects.get(id=id).delete()

    return redirect("/books/" + str(request.session["currentbook"]))