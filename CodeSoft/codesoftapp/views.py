from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Cuenta, Transaccion
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

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
    cuentas = Cuenta.objects.all()
    return render(request, 'catalogo/catalogo.html', {'cuentas': cuentas})

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
    transacciones = Transaccion.objects.all()
    transacciones = transacciones.order_by('fecha')
    cuentas = Cuenta.objects.all()
    cuentas = cuentas.order_by('codigo')
    return render(request, 'transacciones/transacciones.html', {'transacciones': transacciones, 'cuentas': cuentas})

@login_required
def agregar_cuenta(request):
    cuentas = Cuenta.objects.all()  # Obtiene todas las cuentas de la base de datos
    cuentas = cuentas.order_by('codigo')
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')

        cuenta_existente = Cuenta.objects.filter(Q(codigo=codigo) | Q(nombre=nombre)).first()

        if cuenta_existente:
            error_message = "Una cuenta con el mismo código o nombre ya existe en la base de datos."
        else:
            nueva_cuenta = Cuenta(codigo=codigo, nombre=nombre)
            nueva_cuenta.save()
    return render(request, 'catalogo/catalogo.html', {'cuentas': cuentas, 'error_message': error_message if 'error_message' in locals() else None})

@login_required
def agregar_transaccion(request):
    transacciones = Transaccion.objects.all()

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        fecha = request.POST.get('fecha')
        descripcion = request.POST.get('descripcion')
        movimiento_debe = request.POST.get('movimiento_debe')
        movimiento_haber = request.POST.get('movimiento_haber')
        saldo_deudor = request.POST.get('saldo_deudor')
        saldo_acreedor = request.POST.get('saldo_acreedor')

        # Busca la instancia de Cuenta con el código proporcionado
        cuenta = Cuenta.objects.get(codigo=codigo)

        # Crea una nueva instancia de Transaccion
        nueva_transaccion = Transaccion(
            codigo=cuenta,  # Asigna la instancia de Cuenta
            fecha=fecha,
            descripcion=descripcion,
            movimiento_debe=movimiento_debe,
            movimiento_haber=movimiento_haber,
            saldo_deudor=saldo_deudor,
            saldo_acreedor=saldo_acreedor
        )
        nueva_transaccion.save()
        cuentas = Cuenta.objects.all()
        cuentas = cuentas.order_by('codigo')
    return render(request, 'transacciones/transacciones.html', {'transacciones': transacciones, 'cuentas': cuentas})
