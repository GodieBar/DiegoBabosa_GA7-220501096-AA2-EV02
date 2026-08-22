from django.contrib import admin
from .models import Cliente, Vehiculo, Mecanico, OrdenServicio

admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Mecanico)
admin.site.register(OrdenServicio)
