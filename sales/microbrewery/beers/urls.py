from django.urls import path
from . import login, beers, search

urlpatterns = [
    path('', beers.list_beers, name='index'),
    path('login/', login.login, name='login'),
    path('logout/', login.logout, name='logout'),
    path('beers/', beers.list_beers, name='list-beers'),
    path('beers/new', beers.new_beer, name='new-beer'),
    path('search', search.search, name='search'),
]
