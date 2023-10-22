from django.db import models

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
    saldo_deudor = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_acreedor = models.DecimalField(max_digits=10, decimal_places=2)
    # Relación con la cuenta (cada transacción está relacionada con una cuenta)
    
    def __str__(self):
        return f"Transacción {self.id} - {self.codigo}"
