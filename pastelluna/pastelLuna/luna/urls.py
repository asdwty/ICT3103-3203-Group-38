from django.urls import path

from .views.profile import profile
from .views.product_details import retrieve_product_details
from .views.home import shop, home
from .views.user import editor_dash
from .views.registration import registration
from .views.admin_dashboard import admin_dashboard
from .views.loginpage import loginpage
from .views.logoutpage import logoutpage


urlpatterns = [

     path("", home, name="home"),
     path("home", home, name="home"),
     path("profile", profile, name="profile"),
     path("registration",registration, name="registation"), #added this
     path("loginpage", loginpage, name="loginpage"),
     path("logout", logoutpage, name="home"),
     path("shop", shop, name="shop"),
     path('editor_dash', editor_dash, name="editor_dashboard"),
     path('admin_dashboard', admin_dashboard, name="admin_dashboard"),
     path('<slug:slug>', retrieve_product_details,name="product_details"),


]

