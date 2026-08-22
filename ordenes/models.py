from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="vehiculos")
    placa = models.CharField(max_length=10, unique=True)
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=60)

    class Meta:
        ordering = ["placa"]

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"


class Mecanico(models.Model):
    nombre = models.CharField(max_length=120)
    especialidad = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class OrdenServicio(models.Model):
    ESTADOS = [
        ("RECIBIDA", "Recibida"),
        ("DIAGNOSTICO", "En diagnóstico"),
        ("REPARACION", "En reparación"),
        ("LISTA", "Lista para entregar"),
        ("ENTREGADA", "Entregada"),
    ]

    numero_orden = models.CharField(max_length=20, unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="ordenes")
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, related_name="ordenes")
    mecanico = models.ForeignKey(
        Mecanico, on_delete=models.SET_NULL, null=True, blank=True, related_name="ordenes"
    )
    descripcion_problema = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="RECIBIDA")
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_ingreso"]

    def save(self, *args, **kwargs):
        # Número de orden legible y único: OS-101, OS-102, ...
        # Se basa en el último ID autoincremental de la tabla, que en
        # SQLite/MySQL nunca se reutiliza (ni al borrar registros), por lo
        # que no hay riesgo de colisión dentro del alcance de este proyecto.
        # No se agrega un contador ni bloqueos adicionales: para el volumen
        # de datos de esta evidencia académica, esto es suficiente y evita
        # complejidad innecesaria (condiciones de carrera de alta
        # concurrencia no aplican a este alcance).
        if not self.numero_orden:
            ultimo = OrdenServicio.objects.order_by("-id").first()
            siguiente = 101 if not ultimo else 101 + ultimo.id
            self.numero_orden = f"OS-{siguiente}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero_orden
