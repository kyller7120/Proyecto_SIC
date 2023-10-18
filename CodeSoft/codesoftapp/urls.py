from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
urlpatterns = [
    ##login
    path('', login_required(views.inicio)),
    path('login', login_required(views.inicio)),
    path('logout', views.logout_view),

    ##catalogo de cuentas
    path('catalogo_cuentas', login_required(views.catalogo)),
    ##control de costos
    path('control_costos', login_required(views.control)),
    ##estados financieros
    path('estados_financieros', login_required(views.estados)),
    ##transacciones
    path('transacciones', login_required(views.transacciones)),
]