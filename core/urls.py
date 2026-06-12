from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('contact', views.contact, name = "contact"),
    path('my-work', views.work, name = "work"),
    path('about-me', views.about_me, name = "about_me"),
]