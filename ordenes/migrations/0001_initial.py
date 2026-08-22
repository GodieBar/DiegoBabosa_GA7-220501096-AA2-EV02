# Generated manually to make the submitted project migration-ready.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Cliente",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=120)),
                ("telefono", models.CharField(blank=True, max_length=30)),
            ],
            options={"ordering": ["nombre"]},
        ),
        migrations.CreateModel(
            name="Mecanico",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=120)),
                ("especialidad", models.CharField(blank=True, max_length=100)),
            ],
            options={"ordering": ["nombre"]},
        ),
        migrations.CreateModel(
            name="Vehiculo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("placa", models.CharField(max_length=10, unique=True)),
                ("marca", models.CharField(max_length=60)),
                ("modelo", models.CharField(max_length=60)),
                ("cliente", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="vehiculos", to="ordenes.cliente")),
            ],
            options={"ordering": ["placa"]},
        ),
        migrations.CreateModel(
            name="OrdenServicio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("numero_orden", models.CharField(editable=False, max_length=20, unique=True)),
                ("descripcion_problema", models.TextField()),
                ("estado", models.CharField(choices=[("RECIBIDA", "Recibida"), ("DIAGNOSTICO", "En diagnóstico"), ("REPARACION", "En reparación"), ("LISTA", "Lista para entregar"), ("ENTREGADA", "Entregada")], default="RECIBIDA", max_length=20)),
                ("fecha_ingreso", models.DateTimeField(auto_now_add=True)),
                ("cliente", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="ordenes", to="ordenes.cliente")),
                ("mecanico", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="ordenes", to="ordenes.mecanico")),
                ("vehiculo", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="ordenes", to="ordenes.vehiculo")),
            ],
            options={"ordering": ["-fecha_ingreso"]},
        ),
    ]
