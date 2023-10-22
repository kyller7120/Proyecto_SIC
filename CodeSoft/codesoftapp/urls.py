from django.urls import path
from . import views
urlpatterns = [
    ##login
    path('', views.inicio, name='inicio'),
    path('login', views.inicio),
    path('logout', views.logout_view),

    ##catalogo de cuentas
    path('catalogo_cuentas', views.catalogo),

    ##control de costos
    path('control_costos', views.control),
    path('costos_indirectos_fabricacion', views.indirectos),
    path('mano_de_obra_directa', views.manoobra),

    ##estados financieros
    path('estados_financieros', views.estados),

    path('balance_comprobacion', views.comprobacion),
    path('ajustes', views.ajustes),
    path('balance_ajustado', views.ajustado),
    path('estado_resultados', views.resultados),
    path('estado_capital', views.capital),
    path('balance_general', views.general),

    ##transacciones
    path('transacciones', views.transacciones),
    
    path('agregar_cuenta', views.agregar_cuenta, name='agregar_cuenta'),
    path('agregar_transaccion', views.agregar_transaccion, name='agregar_transaccion'),
]