from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

#inicio
@login_required
def inicio(request):
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('/')

#catalogo de cuentas
@login_required
def catalogo(request):
    return render(request, 'catalogo/catalogo.html')
#control de costos
@login_required
def control(request):
    return render(request, 'controlcostos/controlcostos.html')
#estados financieros
@login_required
def estados(request):
    return render(request, 'estadosfinancieros/estadosfinancieros.html')
#transacciones
@login_required
def transacciones(request):
    return render(request, 'transacciones/transacciones.html')

