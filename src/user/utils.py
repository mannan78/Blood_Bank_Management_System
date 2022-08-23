from .models import User
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
import bcrypt

# make new hashed password
def MAKE_PASSWORD(password):
    password = password.encode()
    hash = bcrypt.hashpw(password, bcrypt.gensalt())
    return hash


# match password to hashed one
def CHECK_PASSWORD(password, hash):
    return bcrypt.checkpw(password.encode(), hash.encode())


# check if user is already logged in or not
def IsLoggedIn(request):
    if request.session.has_key("username"):
        try:
            user = User.objects.get(username=request.session["username"])
            return user
        except:
            return None
    else:
        return None

def get_role(request):
    if request.session.has_key("username"):
        try:
            user = User.objects.get(username=request.session["username"])
            return user.roles
        except:
            return None
    else:
        return None

def role_based_redirection(request):
    role = get_role(request)
    if role == "blood_bank":
        return "/user/blood_bank_dashboard"
    
    else:
        messages.error(request, "Role not valid!")
        return "/user/logout"