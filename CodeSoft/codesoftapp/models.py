from django.db import models
from django.db.models import Sum

class Cuenta(models.Model):
    class Meta:
        app_label = 'codesoftapp'
    codigo = models.CharField(max_length=10, unique=True, primary_key=True)  # El campo de código es único
    nombre = models.CharField(max_length=100, unique=True)  # El campo de nombre es único

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Transaccion(models.Model):
    codigo = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=200)
    movimiento_debe = models.DecimalField(max_digits=10, decimal_places=2)
    movimiento_haber = models.DecimalField(max_digits=10, decimal_places=2)
    # Relación con la cuenta (cada transacción está relacionada con una cuenta)
    
    def __str__(self):
        return f"Transacción {self.id} - {self.codigo}"

class ResumenCuentas(models.Model):
    debe_total = models.DecimalField(max_digits=10, decimal_places=2)
    haber_total = models.DecimalField(max_digits=10, decimal_places=2)

    @classmethod
    def actualizar_resumen(cls):
        # Obtener la suma total de movimientos de debe y haber por cuenta
        resumen = Cuenta.objects.annotate(
            debe_total=Sum('transaccion__movimiento_debe'),
            haber_total=Sum('transaccion__movimiento_haber')
        )

        # Calcular la suma total de movimientos de debe y haber en todas las cuentas
        suma_debe_total = resumen.aggregate(Sum('debe_total'))['debe_total__sum'] or 0
        suma_haber_total = resumen.aggregate(Sum('haber_total'))['haber_total__sum'] or 0

        # Crear o actualizar la instancia de ResumenCuentas
        resumen_cuentas, created = cls.objects.get_or_create(pk=1)
        resumen_cuentas.debe_total = suma_debe_total
        resumen_cuentas.haber_total = suma_haber_total
        resumen_cuentas.save()

    def __str__(self):
        return "Resumen de Cuentas"