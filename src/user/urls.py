from django.urls import path
from . import views

urlpatterns = [
    path("",views.login, name="login"),
    path("searchBlood",views.searchBlood, name="searchBlood"),
    path("donateBlood",views.donateBlood, name="donateBlood"),
    path("loginpage",views.loginpage, name="loginpage"),
    path("signup", views.blood_bank_signup, name="signup"),
    path("register", views.register_blood_bank, name="register_blood_bank"),
    path("loginUser", views.loginUser, name="loginUser"),
    path("logout", views.logout, name="logout"),
    path("blood_bank_dashboard",views.blood_bank_dashboard, name="blood_bank_dashboard"),
    path("getdetails", views.getdetails, name="getdetails"),
    path("blood_bank_dashboard/blood_camp", views.blood_camp, name="blood_camp"),
    path("blood_bank_dashboard/blood_camp/formsubmit", views.blood_camp_form_submit, name="blood_camp_form_submit"),
    path("blood_bank_dashboard/blood_bank_profile", views.blood_bank_profile, name="blood_bank_profile"),
    path("blood_bank_dashboard/blood_bank_profile/update_blood_bank_profile", views.update_blood_bank_profile, name="update_blood_bank_profile"),
    path("blood_bank_dashboard/update_blood_details", views.update_blood_details, name="update_blood_details"),

]