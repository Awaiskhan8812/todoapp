from django.urls.resolvers import URLPattern
from . import views
from django.urls import path

urlpatterns = [
    path('',views.home),
    path('register/', views.register),
    path('login/' , views.login),
    path('todo/' , views.todo),
    path('save/' , views.save),
    path('delete' , views.delete),
    path('logout' , views.logout),
]
