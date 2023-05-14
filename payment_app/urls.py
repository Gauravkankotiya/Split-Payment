from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login),
    path('register/',views.register),
    path('all-users/',views.all_users),
    path('make-group/',views.make_group),
    path('add-expenses/',views.add_expenses),
    path('caluculate-expenses/',views.caluculate)
]