from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Cuenta, Transaccion, ResumenCuentas, Periodo
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db.models import Sum, FloatField, Case, When, F, Value, IntegerField, DecimalField
from decimal import Decimal


# Vista para la página de inicio
@login_required
def inicio(request):
    return render(request, 'index.html')

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    return redirect('/')

# Vista para mostrar el catálogo de cuentas
@login_required
def catalogo(request):
    cuentas = Cuenta.objects.all().order_by('codigo')
    return render(request, 'catalogo/catalogo.html', {'cuentas': cuentas})

# Vistas relacionadas con el control de costos
@login_required
def control(request):
    return render(request, 'controlcostos/controlcostos.html')

@login_required
def indirectos(request):
    return render(request, 'controlcostos/indirectos.html')

@login_required
def manoobra(request):
    return render(request, 'controlcostos/manoobra.html')

# Vistas relacionadas con los estados financieros
@login_required
def estados(request):
    return render(request, 'estadosfinancieros/estadosfinancieros.html')

@login_required
def comprobacion(request, periodo_id=None):
    if request.method == 'POST':
        periodo_id = request.POST.get('periodo')
        
    periodos = Periodo.objects.all()
    periodo_seleccionado = None
    if periodo_id:
        periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)
        if not periodo_seleccionado:
            periodo_seleccionado = None
    
    consulta = Cuenta.objects.filter(resumen_cuentas__isnull=False, resumen_cuentas__periodo=periodo_seleccionado)
    consulta = consulta.values('codigo', 'nombre', 'resumen_cuentas__debe_total', 'resumen_cuentas__haber_total', 'resumen_cuentas__saldo')
    resultados = []
    suma_debe_total = Decimal(0)  # Inicializa la suma del debe
    suma_haber_total = Decimal(0)  # Inicializa la suma del haber
    
    for cuenta in consulta:
        if '1000' <= cuenta['codigo'] <= '1203':
            cuenta['resumen_cuentas__debe_total'] = cuenta['resumen_cuentas__saldo']
            cuenta['resumen_cuentas__haber_total'] = 0
            if(cuenta['resumen_cuentas__debe_total'] < 0):
                cuenta['resumen_cuentas__haber_total'] = -1* (cuenta['resumen_cuentas__debe_total'])
                cuenta['resumen_cuentas__debe_total'] = 0
            if(cuenta['resumen_cuentas__haber_total'] < 0):
                cuenta['resumen_cuentas__debe_total'] = -1* (cuenta['resumen_cuentas__haber_total'])
                cuenta['resumen_cuentas__haber_total'] = 0

        elif '2101' <= cuenta['codigo'] <= '3102':
            cuenta['resumen_cuentas__haber_total'] = cuenta['resumen_cuentas__saldo']
            cuenta['resumen_cuentas__debe_total'] = 0
            if(cuenta['resumen_cuentas__debe_total'] < 0):
                cuenta['resumen_cuentas__haber_total'] = -1* (cuenta['resumen_cuentas__debe_total'])
                cuenta['resumen_cuentas__debe_total'] = 0
            if(cuenta['resumen_cuentas__haber_total'] < 0):
                cuenta['resumen_cuentas__debe_total'] = -1* (cuenta['resumen_cuentas__haber_total'])
                cuenta['resumen_cuentas__haber_total'] = 0

        elif '4101' <= cuenta['codigo'] <= '4112':
            cuenta['resumen_cuentas__debe_total'] = cuenta['resumen_cuentas__saldo']
            cuenta['resumen_cuentas__haber_total'] = 0
            if(cuenta['resumen_cuentas__debe_total'] < 0):
                cuenta['resumen_cuentas__haber_total'] = -1* (cuenta['resumen_cuentas__debe_total'])
                cuenta['resumen_cuentas__debe_total'] = 0
            if(cuenta['resumen_cuentas__haber_total'] < 0):
                cuenta['resumen_cuentas__debe_total'] = -1* (cuenta['resumen_cuentas__haber_total'])
                cuenta['resumen_cuentas__haber_total'] = 0

        elif '510101' <= cuenta['codigo'] <= '510202':
            cuenta['resumen_cuentas__haber_total'] = cuenta['resumen_cuentas__saldo']
            cuenta['resumen_cuentas__debe_total'] = 0
            if(cuenta['resumen_cuentas__debe_total'] < 0):
                cuenta['resumen_cuentas__haber_total'] = -1* (cuenta['resumen_cuentas__debe_total'])
                cuenta['resumen_cuentas__debe_total'] = 0
            if(cuenta['resumen_cuentas__haber_total'] < 0):
                cuenta['resumen_cuentas__debe_total'] = -1* (cuenta['resumen_cuentas__haber_total'])
                cuenta['resumen_cuentas__haber_total'] = 0
        
        resultados.append(cuenta)
        
        suma_debe_total += cuenta['resumen_cuentas__debe_total']
        suma_haber_total += cuenta['resumen_cuentas__haber_total']
    if(suma_debe_total < 0):
        suma_haber_total = -1*(suma_debe_total)
        suma_debe_total=0

    if(suma_haber_total < 0):
        suma_debe_total = -1*(suma_haber_total)
        suma_haber_total=0
    return render(request, 'estadosfinancieros/comprobacion.html', {
            'resultados': resultados,
            'suma_debe_total': suma_debe_total,
            'suma_haber_total': suma_haber_total,
            'periodos': periodos,
            'periodo_seleccionado': periodo_seleccionado,
        })

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

# Vistas relacionadas con las transacciones
@login_required
def transacciones(request, periodo_id=None):
    periodos = Periodo.objects.all()
    periodo_seleccionado = None

    if periodo_id:
        periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

    if not periodo_seleccionado:
        periodo_seleccionado = None

    transacciones = Transaccion.objects.filter(periodo=periodo_seleccionado).order_by('codigo')
    cuentas = Cuenta.objects.all().order_by('codigo')
    suma_debe = Transaccion.objects.filter(periodo=periodo_seleccionado).aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or Decimal(0)
    suma_haber = Transaccion.objects.filter(periodo=periodo_seleccionado).aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or Decimal(0)
    
    return render(request, 'transacciones/transacciones.html', {
        'cuentas': cuentas,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'periodos': periodos,
        'periodo_seleccionado': periodo_seleccionado,
    })

@login_required
def agregar_cuenta(request):
    cuentas = Cuenta.objects.all().order_by('codigo')
    error_message = None

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')

        cuenta_existente = Cuenta.objects.filter(Q(codigo=codigo) | Q(nombre=nombre)).first()

        if cuenta_existente:
            error_message = "Una cuenta con el mismo código o nombre ya existe en la base de datos."
        else:
            nueva_cuenta = Cuenta(codigo=codigo, nombre=nombre)
            nueva_cuenta.save()
    
    return render(request, 'catalogo/catalogo.html', {'cuentas': cuentas, 'error_message': error_message})

@login_required
def agregar_transaccion(request, periodo_id=None):
    periodos = Periodo.objects.all()
    periodo_seleccionado = None
    cuentas = Cuenta.objects.all().order_by('codigo')

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        fecha = request.POST.get('fecha')
        descripcion = request.POST.get('descripcion')
        movimiento_debe = request.POST.get('movimiento_debe', 0)
        movimiento_haber = request.POST.get('movimiento_haber', 0)
        periodo_id = request.POST.get('periodo')

        if periodo_id:
            periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)
        if not periodo_seleccionado:
            periodo_seleccionado = None

        transacciones = Transaccion.objects.filter(periodo_id=periodo_id)
        cuenta = Cuenta.objects.get(codigo=codigo)
        nueva_transaccion = Transaccion(
            codigo=cuenta,
            fecha=fecha,
            descripcion=descripcion,
            movimiento_debe=movimiento_debe,
            movimiento_haber=movimiento_haber,
            periodo_id = periodo_id
        )
        nueva_transaccion.save()

    suma_debe = Transaccion.objects.filter(periodo=periodo_seleccionado).aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or Decimal(0)
    suma_haber = Transaccion.objects.filter(periodo=periodo_seleccionado).aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or Decimal(0)

    return render(request, 'transacciones/transacciones.html', {
        'transacciones': transacciones,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'periodos': periodos,
        'periodo_seleccionado': periodo_seleccionado,
        'cuentas':cuentas
    })

def modificar_transaccion(request, transaccion_id):
    transaccion = get_object_or_404(Transaccion, pk=transaccion_id)
    
    if request.method == 'POST':
        if 'codigo' in request.POST:
            codigo_cuenta = request.POST['codigo']
            cuenta = Cuenta.objects.get(codigo=codigo_cuenta)  # Encuentra la cuenta con el código proporcionado
            transaccion.codigo = cuenta  # Asigna la cuenta a la transacción
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
    
    periodos = Periodo.objects.all()
    periodo_seleccionado = None

    if request.method == 'POST':
        periodo_id = request.POST.get('periodo-select', 'Ninguno')  # Obtén el ID del período desde el formulario
        if periodo_id != 'Ninguno':
            periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

    transacciones = Transaccion.objects.filter(periodo=periodo_seleccionado).order_by('fecha')
    suma_debe = transacciones.aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or Decimal(0)
    suma_haber = transacciones.aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or Decimal(0)
    cuentas = Cuenta.objects.all().order_by('codigo')

    return render(request, 'transacciones/transacciones.html', {
        'transaccion': transaccion,
        'transacciones': transacciones,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'cuentas': cuentas,
        'periodos': periodos,
        'periodo_seleccionado': periodo_seleccionado,
    })



@login_required
def eliminar_transaccion(request, transaccion_id):
    transaccion = Transaccion.objects.get(id=transaccion_id)
    transaccion.delete()

    transacciones = Transaccion.objects.filter(periodo=transaccion.periodo).order_by('fecha')
    suma_debe = Transaccion.objects.filter(periodo=transaccion.periodo).aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or Decimal(0)
    suma_haber = Transaccion.objects.filter(periodo=transaccion.periodo).aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or Decimal(0)
    cuentas = Cuenta.objects.all().order_by('codigo')

    return redirect('/transacciones', {
        'transaccion': transaccion,
        'transacciones': transacciones,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'cuentas': cuentas,
    })


@login_required
def libro_mayor(request, periodo_id=None):
    if request.method == 'POST':
        periodo_id = request.POST.get('periodo')
        periodos = Periodo.objects.all()
        periodo_seleccionado = None

        if periodo_id:
            periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

        if not periodo_seleccionado:
            periodo_seleccionado = None

        consulta = Cuenta.objects.filter(resumen_cuentas__isnull=False, resumen_cuentas__periodo=periodo_seleccionado)
        consulta = consulta.values('codigo', 'nombre', 'resumen_cuentas__debe_total', 'resumen_cuentas__haber_total', 'resumen_cuentas__saldo')
        resultados = consulta.all()
    else:
        periodos = Periodo.objects.all()
        periodo_seleccionado = None

        if periodo_id:
            periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

        if not periodo_seleccionado:
            periodo_seleccionado = None

        consulta = Cuenta.objects.filter(resumen_cuentas__isnull=False, resumen_cuentas__periodo=periodo_seleccionado)
        consulta = consulta.values('codigo', 'nombre', 'resumen_cuentas__debe_total', 'resumen_cuentas__haber_total', 'resumen_cuentas__saldo')
        resultados = consulta.all()
        resultados = resultados.order_by('codigo')

    return render(request, 'transacciones/libromayor.html', {
        'resultados': resultados,
        'periodos': periodos,
        'periodo_seleccionado': periodo_seleccionado,
    })

@login_required
def crear_periodo(request, periodo_id=None):
    if request.method == 'POST':
        nombre_periodo = request.POST.get('nombre_periodo')

        # Encuentra el último período creado
        ultimo_periodo = Periodo.objects.order_by('-codigo').first()
        nuevo_codigo = 1  # Valor predeterminado si no hay ningún período existente

        if ultimo_periodo:
            # Si hay períodos existentes, incrementa el código en 1
            nuevo_codigo = int(ultimo_periodo.codigo) + 1

        # Convierte nuevo_codigo a una cadena
        nuevo_codigo = str(nuevo_codigo)

        # Crea el nuevo período con el código generado
        nuevo_periodo = Periodo(codigo=nuevo_codigo, nombre=nombre_periodo)
        nuevo_periodo.save()

    periodos = Periodo.objects.all()
    periodo_seleccionado = None

    if periodo_id:
        periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

    if not periodo_seleccionado:
        periodo_seleccionado = None

    transacciones = Transaccion.objects.filter(periodo=periodo_seleccionado).order_by('codigo')
    cuentas = Cuenta.objects.all().order_by('codigo')
    suma_debe = Transaccion.objects.filter(periodo=periodo_seleccionado).aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or Decimal(0)
    suma_haber = Transaccion.objects.filter(periodo=periodo_seleccionado).aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or Decimal(0)
    
    return render(request, 'transacciones/transacciones.html', {
        'transacciones': transacciones,
        'cuentas': cuentas,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'periodos': periodos,
        'periodo_seleccionado': periodo_seleccionado,
    })



def filtrar_transacciones(request, periodo_id=None):
    periodos = Periodo.objects.all()
    cuentas = Cuenta.objects.all().order_by('codigo')
    if request.method == 'POST':
        periodo_id = request.POST.get('periodo-select')  # Obtén el ID del período desde el formulario
        suma_debe = Transaccion.objects.filter(periodo=periodo_id).aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or Decimal(0)
        suma_haber = Transaccion.objects.filter(periodo=periodo_id).aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or Decimal(0)
        if periodo_id == 'Ninguno':
            # Si se selecciona "Todos los períodos," muestra todas las transacciones
            return render(request, 'transacciones/transacciones.html', {'periodos'})
        else:
            # De lo contrario, filtra las transacciones por el período seleccionado
            transacciones = Transaccion.objects.filter(periodo_id=periodo_id)

        # Aquí puedes realizar cualquier otro procesamiento necesario antes de mostrar las transacciones

        # A continuación, debes pasar las transacciones filtradas a la plantilla
        return render(request, 'transacciones/transacciones.html', 
                      {'transacciones':transacciones, 
                       'suma_debe':suma_debe, 
                       'suma_haber': suma_haber,
                       'suma_haber': suma_haber,
                       'periodos': periodos,
                       'cuentas': cuentas,
                       })


from decimal import Decimal

@login_required
def actualizar_resumen_cuentas(request, periodo_id=None):
    # Lógica para manejar solicitudes POST
    if request.method == 'POST':
        periodo_id = request.POST.get('periodo')
        periodo_seleccionado = None
        if periodo_id:
            periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

        # Obtén todas las cuentas, incluso las que no tienen transacciones
        cuentas = Cuenta.objects.all()

        # Si hay un periodo seleccionado, realiza los cálculos
        if periodo_seleccionado:
            cuentas = cuentas.annotate(
                suma_debe=Sum(
                    Case(
                        When(transaccion__periodo=periodo_seleccionado, then=F('transaccion__movimiento_debe')),
                        default=Value(0, output_field=DecimalField()),  # Establece output_field como DecimalField
                    )
                ),
                suma_haber=Sum(
                    Case(
                        When(transaccion__periodo=periodo_seleccionado, then=F('transaccion__movimiento_haber')),
                        default=Value(0, output_field=DecimalField()),  # Establece output_field como DecimalField
                    )
                )
            )

            ResumenCuentas.objects.filter(periodo=periodo_seleccionado).delete()

            for cuenta in cuentas:
                suma_debe = float(cuenta.suma_debe)
                suma_haber = float(cuenta.suma_haber)
                saldo = 0

                if '1000' <= cuenta.codigo <= '1203':
                    saldo = suma_debe - suma_haber
                elif '2101' <= cuenta.codigo <= '3102':
                    saldo = suma_haber - suma_debe
                elif '4101' <= cuenta.codigo <= '4112':
                    saldo = suma_debe - suma_haber
                elif '510101' <= cuenta.codigo <= '510202':
                    saldo = suma_haber - suma_debe

                ResumenCuentas.objects.update_or_create(
                    periodo=periodo_seleccionado,
                    cuenta=cuenta,
                    defaults={
                        'debe_total': suma_debe,
                        'haber_total': suma_haber,
                        'saldo': saldo,
                    }
                )
    else:
        # Si no hay periodo seleccionado, establece los valores por defecto
        cuentas = cuentas.annotate(
            suma_debe=Value(0, output_field=DecimalField()),  # Establece output_field como DecimalField
            suma_haber=Value(0, output_field=DecimalField())  # Establece output_field como DecimalField
        )
    # Lógica para manejar solicitudes GET
    periodos = Periodo.objects.all()
    periodo_seleccionado = None

    if periodo_id:
        periodo_seleccionado = get_object_or_404(Periodo, pk=periodo_id)

    consulta = Cuenta.objects.filter(
        resumen_cuentas__isnull=False,
        resumen_cuentas__periodo=periodo_seleccionado
    ).values(
        'codigo', 'nombre', 'resumen_cuentas__debe_total',
        'resumen_cuentas__haber_total', 'resumen_cuentas__saldo'
    )

    resultados = consulta.all()

    suma_debe_total = ResumenCuentas.objects.filter(
        periodo=periodo_seleccionado
    ).aggregate(Sum('debe_total'))['debe_total__sum'] or 0

    suma_haber_total = ResumenCuentas.objects.filter(
        periodo=periodo_seleccionado
    ).aggregate(Sum('haber_total'))['haber_total__sum'] or 0

    suma_debe = Transaccion.objects.filter(
        periodo=periodo_seleccionado
    ).aggregate(Sum('movimiento_debe'))['movimiento_debe__sum'] or 0

    suma_haber = Transaccion.objects.filter(
        periodo=periodo_seleccionado
    ).aggregate(Sum('movimiento_haber'))['movimiento_haber__sum'] or 0

    cuentas = cuentas.order_by('codigo')
    transacciones = Transaccion.objects.filter(
        periodo=periodo_seleccionado
    ).order_by('fecha')

    return render(request, 'transacciones/transacciones.html', {
        'resultados': resultados,
        'periodos': periodos,
        'periodo_seleccionado': periodo_seleccionado,
        'transacciones': transacciones,
        'suma_debe': suma_debe,
        'suma_haber': suma_haber,
        'cuentas': cuentas,
        'suma_debe_total': suma_debe_total,
        'suma_haber_total': suma_haber_total,
    })
