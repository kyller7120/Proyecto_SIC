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
@login_required
def indirectos(request):
    return render(request, 'controlcostos/indirectos.html')
@login_required
def manoobra(request):
    return render(request, 'controlcostos/manoobra.html')

#estados financieros
@login_required
def estados(request):
    return render(request, 'estadosfinancieros/estadosfinancieros.html')
@login_required
def comprobacion(request):
    return render(request, 'estadosfinancieros/comprobacion.html')
@login_required
def ajustes(request):
    return render(request, 'estadosfinancieros/ajustes.html')
@login_required
def ajustado(request):
    return render(request, 'estadosfinancieros/ajustado.html')
@login_required
def general(request):
    return render(request, 'estadosfinancieros/general.html')
@login_required
def resultados(request):
    return render(request, 'estadosfinancieros/resultados.html')
@login_required
def capital(request):
    return render(request, 'estadosfinancieros/capital.html')


#transacciones
@login_required
def transacciones(request):
    return render(request, 'transacciones/transacciones.html')
