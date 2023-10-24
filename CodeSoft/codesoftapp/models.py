from django.db import models
from django.db.models import Sum

class Periodo(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class Cuenta(models.Model):
    class Meta:
        app_label = 'codesoftapp'
    codigo = models.CharField(max_length=10, unique=True, primary_key=True)  # El campo de código es único
    nombre = models.CharField(max_length=100, unique=True)  # El campo de nombre es único

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Transaccion(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    codigo = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=200)
    movimiento_debe = models.DecimalField(max_digits=10, decimal_places=2)
    movimiento_haber = models.DecimalField(max_digits=10, decimal_places=2)
    # Relación con la cuenta (cada transacción está relacionada con una cuenta)
    
    def __str__(self):
        return f"Transacción {self.id} - {self.codigo}"

class ResumenCuentas(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='resumen_cuentas')
    debe_total = models.DecimalField(max_digits=10, decimal_places=2)
    haber_total = models.DecimalField(max_digits=10, decimal_places=2)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)  # Agrega el campo saldo

    def __str__(self):
        return "Resumen de Cuentas"
