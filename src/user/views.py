from asyncio.log import logger
from audioop import add
from re import M
from django.utils import timezone
from django.forms import PasswordInput
from django.shortcuts import render, redirect, HttpResponseRedirect
import logging
import json as simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    BloodCamp,
    User,
    State,
    City,
    RBC,
    Platelets,
    Plasma,
    CryoAHF,
    Granulocytes
)

from django.contrib import messages
from django.contrib.auth import logout, login, authenticate

from .utils import (
    IsLoggedIn,
    MAKE_PASSWORD,
    CHECK_PASSWORD,
    role_based_redirection,
)

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import (
    User,
    City,
    RBC,
    Platelets,
    Plasma,
    CryoAHF,
    Granulocytes
)

# Create your views here.

def login(request):
    user = IsLoggedIn(request)
    if user is None:
        return render(request,"public.html")
    else:
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)

# def public(request):
#     user = IsLoggedIn(request)
#     if user is not None:
#         HttpResponseRedirect("/user/login")

def loginpage(request):
    return render(request,"signin.html")
    # user = IsLoggedIn(request)
    # if user in None:
    #     return render(request,"signin.html")
    # else:
    #     url = role_based_redirection(request)
    #     return HttpResponseRedirect(url)



def blood_bank_signup(request):
    user = IsLoggedIn(request)
    if user is None:
        return render(
            request, "signup.html", 
            {
                "cities" : City.objects.all(),
                "states" : State.objects.all(),
            }
            )

    else:
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)

def register_blood_bank(request):
    user = IsLoggedIn(request)
    if user is None:
        if request.method == "POST":
            name = request.POST.get("blood_bank_name")
            username = request.POST.get("username")
            email = request.POST.get("email")
            password1 = request.POST.get("password")
            password2 = request.POST.get("conf_password")
            address = request.POST.get("address")
            contact = request.POST.get("contact")
            city = City.objects.get(name=request.POST.get("city"))
            state = State.objects.get(name=request.POST.get("state"))
            if(city.state != state) :
                messages.error(request, "City is not present in given state!")
                return HttpResponseRedirect("/user/signup")
            if(password1 != password2):
                messages.error(request, "Password does not match!")
                return HttpResponseRedirect("/user/signup")   
            else:
                password = MAKE_PASSWORD(password1)
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already in use!")
                    return HttpResponseRedirect("/user/signup")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "User with this email already exits!")
                    return HttpResponseRedirect("/user/signup")
                else:
                    #create a user obj and save
                    user = User(roles="blood_bank")
                    user.blood_bank_name = name
                    user.username = username
                    user.email = email
                    user.password = password
                    user.address = address
                    user.contact= contact
                    user.city = city
                    user.state = state
                    user.save()
                    
                    #create a corresponding RBC object for given user while registering
                    rbc = RBC(user=user)
                    rbc.quantity_Apstv = 0 
                    rbc.quantity_Angtv = 0 
                    rbc.quantity_Bpstv  =0 
                    rbc.quantity_Bngtv = 0 
                    rbc.quantity_Opstv = 0
                    rbc.quantity_Ongtv = 0
                    rbc.quantity_ABpstv =0 
                    rbc.quantity_ABngtv =0 
                    rbc.save()

                    #create a corresponding Platelets object for given user while registering
                    platelets = Platelets(user=user)
                    platelets.quantity_Apstv = 0 
                    platelets.quantity_Angtv = 0 
                    platelets.quantity_Bpstv  =0 
                    platelets.quantity_Bngtv = 0 
                    platelets.quantity_Opstv = 0
                    platelets.quantity_Ongtv = 0
                    platelets.quantity_ABpstv =0 
                    platelets.quantity_ABngtv =0 
                    platelets.save()

                    #create a corresponding Plasma object for given user while registering
                    plasma = Plasma(user=user)
                    plasma.quantity_Apstv = 0 
                    plasma.quantity_Angtv = 0 
                    plasma.quantity_Bpstv  =0 
                    plasma.quantity_Bngtv = 0 
                    plasma.quantity_Opstv = 0
                    plasma.quantity_Ongtv = 0
                    plasma.quantity_ABpstv =0 
                    plasma.quantity_ABngtv =0 
                    plasma.save()

                    #create a corresponding CryoAHF object for given user while registering
                    cryo_ahf = CryoAHF(user=user)
                    cryo_ahf.quantity_Apstv = 0 
                    cryo_ahf.quantity_Angtv = 0 
                    cryo_ahf.quantity_Bpstv  =0 
                    cryo_ahf.quantity_Bngtv = 0 
                    cryo_ahf.quantity_Opstv = 0
                    cryo_ahf.quantity_Ongtv = 0
                    cryo_ahf.quantity_ABpstv =0 
                    cryo_ahf.quantity_ABngtv =0 
                    cryo_ahf.save()

                    #create a corresponding Granulocytes object for given user while registering
                    granulocytes = Granulocytes(user=user)
                    granulocytes.quantity_Apstv = 0 
                    granulocytes.quantity_Angtv = 0 
                    granulocytes.quantity_Bpstv  =0 
                    granulocytes.quantity_Bngtv = 0 
                    granulocytes.quantity_Opstv = 0
                    granulocytes.quantity_Ongtv = 0
                    granulocytes.quantity_ABpstv =0 
                    granulocytes.quantity_ABngtv =0 
                    granulocytes.save()

                    messages.success(request, "User account created successfully!")
                    return HttpResponseRedirect("/user/loginpage")
        else:
            messages.error(request, "Please fill in the credentials to sign up!")
            return HttpResponseRedirect("/user/signup")
    else: # user is already logged in 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)

# rendered when logging in using the form on login page
def loginUser(request): 
    user = IsLoggedIn(request)
    if user is None:  # user is not already logged in 
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            if User.objects.filter(username=username).exists(): # username exists in the dB
                user = User.objects.get(username=username)
                if CHECK_PASSWORD(password, user.password): # entered password matches with the password stored in dB
                    request.session["username"] = username
                    request.session.modified = True
                    # rendering pages based on roles
                    url = role_based_redirection(request)
                    return HttpResponseRedirect(url)
                    #return HttpResponseRedirect("/user/dashboard")
                else:
                    messages.error(request, "Incorrect password!") # password does not matches : redirect to login page 
                    return HttpResponseRedirect("/user/loginpage") 
            else: # user is not registered in the database : redirect to sign up page 
                messages.error(request, "User does not exist. Kindly register yourself! ")
                return HttpResponseRedirect("/user/loginpage")
        else:
            messages.error(request, "Please fill in the credentials first to login in!")
            return HttpResponseRedirect("/user/loginpage")
    else: # user is already logged in : redirect to the login page
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)


def logout(request):
    if IsLoggedIn(request) is not None:
        del request.session["username"]
    return HttpResponseRedirect("/user/")

def blood_bank(request):
    return render(
        request,
        "blood_bank_dashboard.html",
        {
            "user": IsLoggedIn(request),
            #"blood_bank": user.objects.get(user=IsLoggedIn(request)),
        },
    )

def blood_bank_dashboard(request):
    # logging.basicConfig(level=logging.INFO)
    # logger = logging.getLogger('myapp')
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "blood_bank": # already logged in but not as blood_bank
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
    #logging.basicConfig(level=logging.INFO)
    #logger = logging.getLogger('myapp')
        data = {"blood_bank": None, "rbc": None, "platelets": None, "platelets":None, "cryo_ahf":None, "granulocytes":None}#,"items": []}

        for b in User.objects.all():
            if b == user:
                data["blood_bank"] = b
                for r in RBC.objects.all():
                    if r.user == b:
                        data["rbc"]= r
                        
                        break
                for pt in Platelets.objects.all():
                    if pt.user == b:
                        data["platelets"] = pt
                        break
                for pl in Plasma.objects.all():
                    if pl.user == b:
                        data["plasma"]= pl
                        break
                for c in CryoAHF.objects.all():
                    if c.user == b:
                        data["cryo_ahf"] = c
                        break
                for g in Granulocytes.objects.all():
                    if g.user == b:
                        data["granulocytes"]= g
                        break
                break
        return render(request, "blood_bank_dashboard.html",data)

def getdetails(request):
    state = request.GET.get('state')
    state_object = -1
    for t in State.objects.all():
        if t.name == state:
            state_object = t
    result_set = []
    for city in City.objects.all():
        if city.state == state_object: 
            result_set.append({'id': city.city_id, 'name': city.name})
    return HttpResponse(simplejson.dumps(result_set), content_type="application/json")

def searchBlood(request):
    # logging.basicConfig(level=logging.INFO)
    # logger = logging.getLogger('myapp')
    data = {"items": [], 
            "blood_groups": ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'], 
            "blood_components": ['RBC', 'Plasma', "Platelets", "Cryo AHF", "Granulocytes"],
            "states": State.objects.all(),
            "start": 1}
    if request.method == "GET":
        state_ = request.GET.get("state")
        city_ = request.GET.get("city")
        blood_group_ = request.GET.get("blood_group")
        blood_component_ = request.GET.get("blood_component")
        state_object = -1
        city_object = -1
        for t in State.objects.all():
            if t.name == state_:
                state_object = t
                break
        for c in City.objects.all():
            if c.name == city_:
                city_object = c
                break
        count = 1
        for t in User.objects.all():
            if state_object != -1 and t.state != state_object:
                continue
            if city_object != -1 and t.city != city_object:
                continue
            if (blood_component_ == '' or blood_component_ == "RBC") and RBC.objects.filter(user=t).exists():
                rbc = RBC.objects.get(user=t)
                a = rbc.quantity_Apstv if (blood_group_ == '' or blood_group_ == 'A+') else 0
                b = rbc.quantity_Angtv if (blood_group_ == '' or blood_group_ == 'A-') else 0
                c = rbc.quantity_Bpstv if (blood_group_ == '' or blood_group_ == 'B+') else 0
                d = rbc.quantity_Bngtv if (blood_group_ == '' or blood_group_ == 'B-') else 0
                e = rbc.quantity_Opstv if (blood_group_ == '' or blood_group_ == 'O+') else 0
                f = rbc.quantity_Ongtv if (blood_group_ == '' or blood_group_ == 'O-') else 0
                g = rbc.quantity_ABpstv if (blood_group_ == '' or blood_group_ == 'AB+') else 0
                h = rbc.quantity_ABngtv if (blood_group_ == '' or blood_group_ == 'AB-') else 0
                data["items"].append({
                    's_no': count,
                    'blood_bank' : t,
                    'blood_component' : 'RBC',
                    'blood_group_apstv' : a,
                    'blood_group_angtv' : b,
                    'blood_group_bpstv' : c,
                    'blood_group_bngtv' : d,
                    'blood_group_opstv' : e,
                    'blood_group_ongtv' : f,
                    'blood_group_abpstv' : g,
                    'blood_group_abngtv' : h,
                    'flag' : 1 if (a + b + c + d + e + f + g + h > 0) else 0
                })
                if (a + b + c + d + e + f + g + h > 0):
                    count += 1
            if (blood_component_ == '' or blood_component_ == "Plasma") and Plasma.objects.filter(user=t).exists():
                plasma = Plasma.objects.get(user=t)
                a = plasma.quantity_Apstv if (blood_group_ == '' or blood_group_ == 'A+') else 0
                b = plasma.quantity_Angtv if (blood_group_ == '' or blood_group_ == 'A-') else 0
                c = plasma.quantity_Bpstv if (blood_group_ == '' or blood_group_ == 'B+') else 0
                d = plasma.quantity_Bngtv if (blood_group_ == '' or blood_group_ == 'B-') else 0
                e = plasma.quantity_Opstv if (blood_group_ == '' or blood_group_ == 'O+') else 0
                f = plasma.quantity_Ongtv if (blood_group_ == '' or blood_group_ == 'O-') else 0
                g = plasma.quantity_ABpstv if (blood_group_ == '' or blood_group_ == 'AB+') else 0
                h = plasma.quantity_ABngtv if (blood_group_ == '' or blood_group_ == 'AB-') else 0
                data["items"].append({
                    's_no': count,
                    'blood_bank' : t,
                    'blood_component' : 'Plasma',
                    'blood_group_apstv' : a,
                    'blood_group_angtv' : b,
                    'blood_group_bpstv' : c,
                    'blood_group_bngtv' : d,
                    'blood_group_opstv' : e,
                    'blood_group_ongtv' : f,
                    'blood_group_abpstv' : g,
                    'blood_group_abngtv' : h,
                    'flag' : 1 if (a + b + c + d + e + f + g + h > 0) else 0
                })
                if (a + b + c + d + e + f + g + h > 0):
                    count += 1
            if (blood_component_ == '' or blood_component_ == "Platelets") and Platelets.objects.filter(user=t).exists():
                platelets = Platelets.objects.get(user=t)
                a = platelets.quantity_Apstv if (blood_group_ == '' or blood_group_ == 'A+') else 0
                b = platelets.quantity_Angtv if (blood_group_ == '' or blood_group_ == 'A-') else 0
                c = platelets.quantity_Bpstv if (blood_group_ == '' or blood_group_ == 'B+') else 0
                d = platelets.quantity_Bngtv if (blood_group_ == '' or blood_group_ == 'B-') else 0
                e = platelets.quantity_Opstv if (blood_group_ == '' or blood_group_ == 'O+') else 0
                f = platelets.quantity_Ongtv if (blood_group_ == '' or blood_group_ == 'O-') else 0
                g = platelets.quantity_ABpstv if (blood_group_ == '' or blood_group_ == 'AB+') else 0
                h = platelets.quantity_ABngtv if (blood_group_ == '' or blood_group_ == 'AB-') else 0
                data["items"].append({
                    's_no': count,
                    'blood_bank' : t,
                    'blood_component' : 'Platelets',
                    'blood_group_apstv' : a,
                    'blood_group_angtv' : b,
                    'blood_group_bpstv' : c,
                    'blood_group_bngtv' : d,
                    'blood_group_opstv' : e,
                    'blood_group_ongtv' : f,
                    'blood_group_abpstv' : g,
                    'blood_group_abngtv' : h,
                    'flag' : 1 if (a + b + c + d + e + f + g + h > 0) else 0
                })
                if (a + b + c + d + e + f + g + h > 0):
                    count += 1
            if (blood_component_ == '' or blood_component_ == "Cryo AHF") and CryoAHF.objects.filter(user=t).exists():
                cryo_ahf = CryoAHF.objects.get(user=t)
                a = cryo_ahf.quantity_Apstv if (blood_group_ == '' or blood_group_ == 'A+') else 0
                b = cryo_ahf.quantity_Angtv if (blood_group_ == '' or blood_group_ == 'A-') else 0
                c = cryo_ahf.quantity_Bpstv if (blood_group_ == '' or blood_group_ == 'B+') else 0
                d = cryo_ahf.quantity_Bngtv if (blood_group_ == '' or blood_group_ == 'B-') else 0
                e = cryo_ahf.quantity_Opstv if (blood_group_ == '' or blood_group_ == 'O+') else 0
                f = cryo_ahf.quantity_Ongtv if (blood_group_ == '' or blood_group_ == 'O-') else 0
                g = cryo_ahf.quantity_ABpstv if (blood_group_ == '' or blood_group_ == 'AB+') else 0
                h = cryo_ahf.quantity_ABngtv if (blood_group_ == '' or blood_group_ == 'AB-') else 0
                data["items"].append({
                    's_no': count,
                    'blood_bank' : t,
                    'blood_component' : 'CryoAHF',
                    'blood_group_apstv' : a,
                    'blood_group_angtv' : b,
                    'blood_group_bpstv' : c,
                    'blood_group_bngtv' : d,
                    'blood_group_opstv' : e,
                    'blood_group_ongtv' : f,
                    'blood_group_abpstv' : g,
                    'blood_group_abngtv' : h,
                    'flag' : 1 if (a + b + c + d + e + f + g + h > 0) else 0
                })
                if (a + b + c + d + e + f + g + h > 0):
                    count += 1
            if (blood_component_ == '' or blood_component_ == "Granulocytes") and Granulocytes.objects.filter(user=t).exists():
                granulocytes = Granulocytes.objects.get(user=t)
                a = granulocytes.quantity_Apstv if (blood_group_ == '' or blood_group_ == 'A+') else 0
                b = granulocytes.quantity_Angtv if (blood_group_ == '' or blood_group_ == 'A-') else 0
                c = granulocytes.quantity_Bpstv if (blood_group_ == '' or blood_group_ == 'B+') else 0
                d = granulocytes.quantity_Bngtv if (blood_group_ == '' or blood_group_ == 'B-') else 0
                e = granulocytes.quantity_Opstv if (blood_group_ == '' or blood_group_ == 'O+') else 0
                f = granulocytes.quantity_Ongtv if (blood_group_ == '' or blood_group_ == 'O-') else 0
                g = granulocytes.quantity_ABpstv if (blood_group_ == '' or blood_group_ == 'AB+') else 0
                h = granulocytes.quantity_ABngtv if (blood_group_ == '' or blood_group_ == 'AB-') else 0
                data["items"].append({
                    's_no': count,
                    'blood_bank' : t,
                    'blood_component' : 'Granulocytes',
                    'blood_group_apstv' : a,
                    'blood_group_angtv' : b,
                    'blood_group_bpstv' : c,
                    'blood_group_bngtv' : d,
                    'blood_group_opstv' : e,
                    'blood_group_ongtv' : f,
                    'blood_group_abpstv' : g,
                    'blood_group_abngtv' : h,
                    'flag' : 1 if (a + b + c + d + e + f + g + h > 0) else 0
                })
                if (a + b + c + d + e + f + g + h > 0):
                    count += 1
    return render(request, "searchBlood.html",data)

def blood_camp(request):
    # logging.basicConfig(level=logging.INFO)
    # logger = logging.getLogger('myapp')
    user = IsLoggedIn(request)
    if user is None:
        messages.error(request, "Please login first to fill reimbursement form!")
        return HttpResponseRedirect("/user/logout")
    else:
        state_object = user.state
        city_object = user.city
        state = State.objects.filter(state_id=state_object.state_id)
        city = City.objects.filter(city_id=city_object.city_id)
        logger.info(f"{state} {city}")
        return render(
            request,
            "blood_camp.html",
            {
                "user": user,
                "state": state,
                "city": city,
                
            },
        )

def blood_camp_form_submit(request):
    user = IsLoggedIn(request)
    if user is None: 
        messages.error(request, "Please login first to submit the reimbursement form!")
        return HttpResponseRedirect("/user/logout")
    else: 
        if request.method == "POST":
            camp = BloodCamp()
            camp.user = user
            camp.name = request.POST.get('camp_name')
            camp.organizer = request.POST.get('camp_organizer')
            camp.start_date = request.POST.get('start_date')
            camp.end_date = request.POST.get('end_date')
            camp.start_time = request.POST.get('start_time')
            camp.end_time = request.POST.get('end_time')
            camp.location = request.POST.get('location')
            camp.description = request.POST.get('description')
            camp.save() 
            return HttpResponseRedirect("/user/blood_bank_dashboard")
        else:
            return HttpResponseRedirect("/user")

def donateBlood(request):
    data = {"items": [], 
            "states": State.objects.all(),
            "start": 1}
    if request.method == "GET":
        state_ = request.GET.get("state")
        city_ = request.GET.get("city")
        logger.info(f"{state_} {city_}")
        state_object = -1
        city_object = -1
        for t in State.objects.all():
            if t.name == state_:
                state_object = t
                break
        for c in City.objects.all():
            if c.name == city_:
                city_object = c
                break
        logger.info(f"{state_object} {city_object}")
        count = 1
        for camp in BloodCamp.objects.all():
            if (state_object == -1 or camp.user.state == state_object) and (city_object == -1 or camp.user.city == city_object):
                data["items"].append({
                    's_no': count,
                    'camp_name': camp.name,
                    'blood_bank_name': camp.user.blood_bank_name,
                    'start_date': camp.start_date,
                    'end_date': camp.end_date,
                    'start_time': camp.start_time,
                    'end_time': camp.end_time,
                    'location': camp.location,
                    'description': camp.description,
                    'organizer': camp.organizer,
                    'state': camp.user.state.name,
                    'city': camp.user.city.name,
                })
                count += 1
        return render(request, "donateBlood.html",data)
def blood_bank_profile(request):
    user = IsLoggedIn(request)
    if user is None:
        return HttpResponseRedirect("/user")
    else:
        if user.roles == "blood_bank":
            data = {"blood_bank": None}
            for b in User.objects.all():
                if b == user:
                    data["blood_bank"] = b
                    break
            return render(request, "blood_bank_profile.html", data)
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")


def update_blood_bank_profile(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "blood_bank": # already logged in but not as blood_bank 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            username = user.username
            contact = request.POST.get("contact")
            #address = request.POST.get("address")
            

            # return HttpResponse(str(username) + " " + str(contact))
            userp = User.objects.get(username=username)
            userp.contact = contact
            # userp.address = address
            userp.save()

            messages.success(request, "Profile Succesfully Updated!")
            return HttpResponseRedirect("/user/blood_bank_dashboard/blood_bank_profile")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")

def update_blood_details(request):
    user = IsLoggedIn(request)
    if user is None: # not already logged in 
        messages.error(request, "Kindly login to view the page!")
        return HttpResponseRedirect("/user/logout")
    elif user.roles != "blood_bank": # already logged in but not as blood_bank 
        url = role_based_redirection(request)
        return HttpResponseRedirect(url)
    else:
        if request.method == "POST":
            #usern = user.username

            #new rbc details updated
            rbc_quantity_Apstv =  request.POST.get("rbc_quantity_Apstv")
            rbc_quantity_Angtv = request.POST.get("rbc_quantity_Angtv") 
            rbc_quantity_Bpstv  = request.POST.get("rbc_quantity_Bpstv")
            rbc_quantity_Bngtv = request.POST.get("rbc_quantity_Bngtv") 
            rbc_quantity_Opstv = request.POST.get("rbc_quantity_Opstv")
            rbc_quantity_Ongtv = request.POST.get("rbc_quantity_Ongtv")
            rbc_quantity_ABpstv = request.POST.get("rbc_quantity_ABpstv")
            rbc_quantity_ABngtv = request.POST.get("rbc_quantity_ABngtv")

            rbc = RBC.objects.get(user=user)
            rbc.quantity_Apstv =  rbc_quantity_Apstv
            rbc.quantity_Angtv = rbc_quantity_Angtv 
            rbc.quantity_Bpstv  = rbc_quantity_Bpstv
            rbc.quantity_Bngtv = rbc_quantity_Bngtv 
            rbc.quantity_Opstv = rbc_quantity_Opstv
            rbc.quantity_Ongtv = rbc_quantity_Ongtv
            rbc.quantity_ABpstv = rbc_quantity_ABpstv
            rbc.quantity_ABngtv = rbc_quantity_ABngtv
            rbc.save()
            

            #new platelets details updated
            platelets_quantity_Apstv =  request.POST.get("platelets_quantity_Apstv")
            platelets_quantity_Angtv = request.POST.get("platelets_quantity_Angtv") 
            platelets_quantity_Bpstv  = request.POST.get("platelets_quantity_Bpstv")
            platelets_quantity_Bngtv = request.POST.get("platelets_quantity_Bngtv") 
            platelets_quantity_Opstv = request.POST.get("platelets_quantity_Opstv")
            platelets_quantity_Ongtv = request.POST.get("platelets_quantity_Ongtv")
            platelets_quantity_ABpstv = request.POST.get("platelets_quantity_ABpstv")
            platelets_quantity_ABngtv = request.POST.get("platelets_quantity_ABngtv")

            platelets = Platelets.objects.get(user=user)
            platelets.quantity_Apstv =  platelets_quantity_Apstv
            platelets.quantity_Angtv = platelets_quantity_Angtv 
            platelets.quantity_Bpstv  = platelets_quantity_Bpstv
            platelets.quantity_Bngtv = platelets_quantity_Bngtv 
            platelets.quantity_Opstv = platelets_quantity_Opstv
            platelets.quantity_Ongtv = platelets_quantity_Ongtv
            platelets.quantity_ABpstv = platelets_quantity_ABpstv
            platelets.quantity_ABngtv = platelets_quantity_ABngtv
            platelets.save()


            #new plasma details updated
            plasma_quantity_Apstv =  request.POST.get("plasma_quantity_Apstv")
            plasma_quantity_Angtv = request.POST.get("plasma_quantity_Angtv") 
            plasma_quantity_Bpstv  = request.POST.get("plasma_quantity_Bpstv")
            plasma_quantity_Bngtv = request.POST.get("plasma_quantity_Bngtv") 
            plasma_quantity_Opstv = request.POST.get("plasma_quantity_Opstv")
            plasma_quantity_Ongtv = request.POST.get("plasma_quantity_Ongtv")
            plasma_quantity_ABpstv = request.POST.get("plasma_quantity_ABpstv")
            plasma_quantity_ABngtv = request.POST.get("plasma_quantity_ABngtv")

            plasma = Plasma.objects.get(user=user)
            plasma.quantity_Apstv =  plasma_quantity_Apstv
            plasma.quantity_Angtv = plasma_quantity_Angtv 
            plasma.quantity_Bpstv  = plasma_quantity_Bpstv
            plasma.quantity_Bngtv = plasma_quantity_Bngtv 
            plasma.quantity_Opstv = plasma_quantity_Opstv
            plasma.quantity_Ongtv = plasma_quantity_Ongtv
            plasma.quantity_ABpstv = plasma_quantity_ABpstv
            plasma.quantity_ABngtv = plasma_quantity_ABngtv
            plasma.save()


            # #new cryo_ahf details updated
            cryo_ahf_quantity_Apstv =  request.POST.get("cryo_ahf_quantity_Apstv")
            cryo_ahf_quantity_Angtv = request.POST.get("cryo_ahf_quantity_Angtv") 
            cryo_ahf_quantity_Bpstv  = request.POST.get("cryo_ahf_quantity_Bpstv")
            cryo_ahf_quantity_Bngtv = request.POST.get("cryo_ahf_quantity_Bngtv") 
            cryo_ahf_quantity_Opstv = request.POST.get("cryo_ahf_quantity_Opstv")
            cryo_ahf_quantity_Ongtv = request.POST.get("cryo_ahf_quantity_Ongtv")
            cryo_ahf_quantity_ABpstv = request.POST.get("cryo_ahf_quantity_ABpstv")
            cryo_ahf_quantity_ABngtv = request.POST.get("cryo_ahf_quantity_ABngtv")

            cryo_ahf = CryoAHF.objects.get(user=user)
            cryo_ahf.quantity_Apstv =  cryo_ahf_quantity_Apstv
            cryo_ahf.quantity_Angtv = cryo_ahf_quantity_Angtv 
            cryo_ahf.quantity_Bpstv  = cryo_ahf_quantity_Bpstv
            cryo_ahf.quantity_Bngtv = cryo_ahf_quantity_Bngtv 
            cryo_ahf.quantity_Opstv = cryo_ahf_quantity_Opstv
            cryo_ahf.quantity_Ongtv = cryo_ahf_quantity_Ongtv
            cryo_ahf.quantity_ABpstv = cryo_ahf_quantity_ABpstv
            cryo_ahf.quantity_ABngtv = cryo_ahf_quantity_ABngtv
            cryo_ahf.save()


            # # #new granulocytes details updated
            granulocytes_quantity_Apstv =  request.POST.get("granulocytes_quantity_Apstv")
            granulocytes_quantity_Angtv = request.POST.get("granulocytes_quantity_Angtv") 
            granulocytes_quantity_Bpstv  = request.POST.get("granulocytes_quantity_Bpstv")
            granulocytes_quantity_Bngtv = request.POST.get("granulocytes_quantity_Bngtv") 
            granulocytes_quantity_Opstv = request.POST.get("granulocytes_quantity_Opstv")
            granulocytes_quantity_Ongtv = request.POST.get("granulocytes_quantity_Ongtv")
            granulocytes_quantity_ABpstv = request.POST.get("granulocytes_quantity_ABpstv")
            granulocytes_quantity_ABngtv = request.POST.get("granulocytes_quantity_ABngtv")

            granulocytes = Granulocytes.objects.get(user=user)
            granulocytes.quantity_Apstv =  granulocytes_quantity_Apstv
            granulocytes.quantity_Angtv = granulocytes_quantity_Angtv 
            granulocytes.quantity_Bpstv  = granulocytes_quantity_Bpstv
            granulocytes.quantity_Bngtv = granulocytes_quantity_Bngtv 
            granulocytes.quantity_Opstv = granulocytes_quantity_Opstv
            granulocytes.quantity_Ongtv = granulocytes_quantity_Ongtv
            granulocytes.quantity_ABpstv = granulocytes_quantity_ABpstv
            granulocytes.quantity_ABngtv = granulocytes_quantity_ABngtv
            granulocytes.save()

            messages.success(request, "Blood Details Succesfully Updated!")
            return HttpResponseRedirect("/user/blood_bank_dashboard")
        else:
            messages.error(request, "Kindly login to view the page!")
            return HttpResponseRedirect("/user")