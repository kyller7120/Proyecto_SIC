from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
urlpatterns = [
    path('', login_required(views.inicio)),
    path('login', login_required(views.inicio)),
    path('logout', views.logout_view),
]