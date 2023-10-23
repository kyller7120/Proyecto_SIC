from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Cuenta, Transaccion, ResumenCuentas
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db.models import Sum
from django.db.models import F, ExpressionWrapper, FloatField, Case, When, Value, IntegerField

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
    cuentas = cuentas.order_by('codigo')
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
    suma_debe = Transaccion.objects.aggregate(Sum('movimiento_debe'))['movimiento_debe__sum']
    suma_haber = Transaccion.objects.aggregate(Sum('movimiento_haber'))['movimiento_haber__sum']
    return render(request, 'transacciones/transacciones.html', {'transacciones': transacciones, 'cuentas': cuentas, 'suma_debe': suma_debe, 'suma_haber': suma_haber})

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
        movimiento_debe = request.POST.get('movimiento_debe', 0)  # Si está vacío, asigna 0
        movimiento_haber = request.POST.get('movimiento_haber', 0)  # Si está vacío, asigna 0
        # Busca la instancia de Cuenta con el código proporcionado
        cuenta = Cuenta.objects.get(codigo=codigo)
        # Crea una nueva instancia de Transaccion
        nueva_transaccion = Transaccion(
            codigo=cuenta,  # Asigna la instancia de Cuenta
            fecha=fecha,
            descripcion=descripcion,
            movimiento_debe=movimiento_debe,
            movimiento_haber=movimiento_haber,
        )
        nueva_transaccion.save()
        cuentas = Cuenta.objects.all()
        cuentas = cuentas.order_by('codigo')
        
    # Calcular la suma total del movimiento_debe y movimiento_haber
    suma_debe = Transaccion.objects.aggregate(Sum('movimiento_debe'))['movimiento_debe__sum']
    suma_haber = Transaccion.objects.aggregate(Sum('movimiento_haber'))['movimiento_haber__sum']

    return render(request, 'transacciones/transacciones.html', {'transacciones': transacciones, 'cuentas': cuentas, 'suma_debe': suma_debe, 'suma_haber': suma_haber})

# Otras vistas existentes...

@login_required
def modificar_transaccion(request, transaccion_id):
    # Obtén la transacción que se va a editar
    transaccion = get_object_or_404(Transaccion, pk=transaccion_id)

    if request.method == 'POST':
        if 'fecha' in request.POST:
            transaccion.fecha = request.POST['fecha']
        if 'descripcion' in request.POST:
            transaccion.descripcion = request.POST['descripcion']
        if 'movimiento_debe' in request.POST:
            transaccion.movimiento_debe = request.POST['movimiento_debe']
        else:
            transaccion.movimiento_debe = 0
        if 'movimiento_haber' in request.POST:
            transaccion.movimiento_haber = request.POST['movimiento_haber']
        else:
            transaccion.movimiento_haber = 0
        transaccion.save()
    transacciones = Transaccion.objects.all().order_by('fecha')
    suma_debe = Transaccion.objects.aggregate(Sum('movimiento_debe'))['movimiento_debe__sum']
    suma_haber = Transaccion.objects.aggregate(Sum('movimiento_haber'))['movimiento_haber__sum']

    cuentas = Cuenta.objects.all().order_by('codigo')
    return redirect('/transacciones', {'transaccion': transaccion, 'transacciones': transacciones, 'suma_debe': suma_debe, 'suma_haber': suma_haber, 'cuentas': cuentas})

@login_required
def eliminar_transaccion(request, transaccion_id):
    transaccion = Transaccion.objects.get(id=transaccion_id)
    transaccion.delete()
    transacciones = Transaccion.objects.all()
    transacciones = transacciones.order_by('fecha')
    # Calcular la suma total del movimiento_debe y movimiento_haber
    suma_debe = Transaccion.objects.aggregate(Sum('movimiento_debe'))['movimiento_debe__sum']
    suma_haber = Transaccion.objects.aggregate(Sum('movimiento_haber'))['movimiento_haber__sum']
    cuentas = Cuenta.objects.all()
    cuentas = cuentas.order_by('codigo')
    return redirect('/transacciones', {'transaccion': transaccion, 'transacciones': transacciones, 'suma_debe': suma_debe, 'suma_haber': suma_haber, 'cuentas': cuentas})

@login_required
def actualizar_resumen_cuentas(request):
    cuentas = Cuenta.objects.annotate(
        suma_debe=Sum('transaccion__movimiento_debe'),
        suma_haber=Sum('transaccion__movimiento_haber')
    )
    for cuenta in cuentas:
        ResumenCuentas.objects.update_or_create(
            cuenta=cuenta,
            defaults={
                'debe_total': cuenta.suma_debe or 0,
                'haber_total': cuenta.suma_haber or 0,
            }
        )
    suma_debe_total = ResumenCuentas.objects.aggregate(Sum('debe_total'))['debe_total__sum'] or 0
    suma_haber_total = ResumenCuentas.objects.aggregate(Sum('haber_total'))['haber_total__sum'] or 0

    suma_debe = Transaccion.objects.aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or 0
    suma_haber = Transaccion.objects.aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or 0

    cuentas = Cuenta.objects.all().order_by('codigo')
    transacciones = Transaccion.objects.all().order_by('fecha')

    return render(request, 'transacciones/transacciones.html', {
        'transacciones': transacciones,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'cuentas': cuentas,
        'suma_debe_total': suma_debe_total,
        'suma_haber_total': suma_haber_total,
    })

def libro_mayor(request):
    consulta = Cuenta.objects.filter(resumen_cuentas__isnull=False)
    consulta = consulta.values('codigo', 'nombre', 'resumen_cuentas__debe_total', 'resumen_cuentas__haber_total')
    
    consulta = consulta.annotate(
        saldo=Case(
            When(codigo__range=['1000', '1203'], then=F('resumen_cuentas__debe_total') - F('resumen_cuentas__haber_total')),
            When(codigo__range=['2101', '3102'], then=F('resumen_cuentas__haber_total') - F('resumen_cuentas__debe_total')),
            When(codigo__range=['4101', '4112'], then=F('resumen_cuentas__debe_total') - F('resumen_cuentas__haber_total')),
            When(codigo__range=['510101', '510202'], then=F('resumen_cuentas__haber_total') - F('resumen_cuentas__debe_total')),
            default=Value(0),
            output_field=FloatField()
        )
    )
    
    resultados = consulta.all()
    return render(request, 'transacciones/libromayor.html', {'resultados': resultados})

