"""
Comando de gestión: genera datos de prueba (clientes, vehículos,
mecánicos y órdenes de servicio) para demostrar el CRUD y la paginación
con volumen real de datos.

Uso:
    python manage.py generar_datos_prueba
    python manage.py generar_datos_prueba --ordenes 50
    python manage.py generar_datos_prueba --reset
"""
import random

from django.core.management.base import BaseCommand
from django.db import transaction

from ordenes.models import Cliente, Mecanico, OrdenServicio, Vehiculo

NOMBRES = [
    "Juan", "Ana", "Carlos", "María", "Luis", "Laura", "Andrés", "Camila",
    "Diego", "Valentina", "Jorge", "Paula", "Miguel", "Daniela", "Santiago",
    "Sofía", "Julián", "Isabella", "Felipe", "Carolina", "Sebastián", "Mariana",
    "Nicolás", "Natalia", "Alejandro", "Gabriela", "Ricardo", "Lucía",
    "Fernando", "Adriana",
]

APELLIDOS = [
    "Pérez", "Gómez", "Rodríguez", "Martínez", "López", "García", "Hernández",
    "Ramírez", "Torres", "Díaz", "Vargas", "Castro", "Rojas", "Moreno",
    "Suárez", "Muñoz", "Jiménez", "Ortiz", "Reyes", "Cárdenas", "Mendoza",
    "Guerrero", "Sánchez", "Romero", "Silva", "Cruz", "Peña", "Salazar",
    "Zapata", "Acosta",
]

MARCAS_MODELOS = [
    ("Mazda", "2"), ("Mazda", "3"), ("Chevrolet", "Spark"), ("Chevrolet", "Sail"),
    ("Renault", "Logan"), ("Renault", "Sandero"), ("Toyota", "Corolla"),
    ("Toyota", "Hilux"), ("Kia", "Picanto"), ("Kia", "Rio"), ("Nissan", "Versa"),
    ("Nissan", "Sentra"), ("Hyundai", "Accent"), ("Hyundai", "Tucson"),
    ("Ford", "Fiesta"), ("Ford", "EcoSport"), ("Volkswagen", "Gol"),
    ("Volkswagen", "Polo"), ("Suzuki", "Swift"), ("Suzuki", "Vitara"),
]

ESPECIALIDADES = [
    "Mecánica general", "Motor", "Frenos", "Suspensión",
    "Aire acondicionado", "Sistema eléctrico", "Transmisión",
]

DESCRIPCIONES = [
    "No enciende", "Ruido extraño en el motor", "Revisión general",
    "Cambio de aceite y filtros", "Los frenos chillan", "Falla eléctrica",
    "El aire acondicionado no enfría", "Vibración al frenar",
    "Fuga de aceite", "Batería descargada", "Las luces no encienden",
    "Sobrecalentamiento del motor", "Cambio de llantas",
    "Alineación y balanceo", "Revisión de la suspensión",
    "Olor a quemado al frenar", "El vehículo no arranca en frío",
    "Chequeo previo a viaje largo",
]

ESTADOS = [estado for estado, _ in OrdenServicio.ESTADOS]

LETRAS_PLACA = "ABCDEFGHJKLMNPQRSTUVWXYZ"


class Command(BaseCommand):
    help = (
        "Genera datos de prueba (clientes, vehículos, mecánicos y órdenes "
        "de servicio) para demostrar el CRUD y la paginación con volumen "
        "de datos realista. Por defecto crea 100 órdenes de servicio."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--ordenes",
            type=int,
            default=100,
            help="Cantidad de órdenes de servicio a crear (por defecto: 100).",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help=(
                "Elimina TODOS los clientes, vehículos, mecánicos y "
                "órdenes existentes antes de generar los nuevos datos."
            ),
        )

    @transaction.atomic
    def handle(self, *args, **options):
        cantidad_ordenes = options["ordenes"]

        if options["reset"]:
            OrdenServicio.objects.all().delete()
            Vehiculo.objects.all().delete()
            Cliente.objects.all().delete()
            Mecanico.objects.all().delete()
            self.stdout.write(self.style.WARNING(
                "Se eliminaron los datos existentes de Cliente, Vehiculo, "
                "Mecanico y OrdenServicio."
            ))

        # Semilla fija: los datos generados son reproducibles entre
        # ejecuciones (útil para comparar capturas o depurar).
        random.seed(42)

        mecanicos = [
            Mecanico.objects.create(
                nombre=f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}",
                especialidad=random.choice(ESPECIALIDADES),
            )
            for _ in range(8)
        ]

        clientes = [
            Cliente.objects.create(
                nombre=f"{random.choice(NOMBRES)} {random.choice(APELLIDOS)}",
                telefono=f"3{random.randint(0, 9)}{random.randint(1000000, 9999999)}",
            )
            for _ in range(30)
        ]

        vehiculos = []
        placa_num = 100
        for cliente in clientes:
            for _ in range(random.randint(1, 2)):
                marca, modelo = random.choice(MARCAS_MODELOS)
                letras = "".join(random.choices(LETRAS_PLACA, k=3))
                placa = f"{letras}{placa_num}"
                placa_num += 1
                vehiculos.append(Vehiculo.objects.create(
                    cliente=cliente, placa=placa, marca=marca, modelo=modelo,
                ))

        vehiculos_por_cliente = {}
        for vehiculo in vehiculos:
            vehiculos_por_cliente.setdefault(vehiculo.cliente_id, []).append(vehiculo)

        creadas = 0
        for _ in range(cantidad_ordenes):
            cliente = random.choice(clientes)
            vehiculo = random.choice(vehiculos_por_cliente[cliente.id])
            OrdenServicio.objects.create(
                cliente=cliente,
                vehiculo=vehiculo,
                mecanico=random.choice(mecanicos) if random.random() > 0.1 else None,
                descripcion_problema=random.choice(DESCRIPCIONES),
                estado=random.choice(ESTADOS),
            )
            creadas += 1

        self.stdout.write(self.style.SUCCESS(
            f"Datos de prueba generados: {len(clientes)} clientes, "
            f"{len(vehiculos)} vehículos, {len(mecanicos)} mecánicos y "
            f"{creadas} órdenes de servicio."
        ))
