from django.core.management import call_command
from django.test import TestCase
from .forms import OrdenServicioForm
from .models import Cliente, Vehiculo, Mecanico, OrdenServicio


class BaseOrdenesTestCase(TestCase):
    """Datos base compartidos por las pruebas de modelo, formulario y vistas."""

    def setUp(self):
        self.cliente1 = Cliente.objects.create(nombre="Juan Pérez", telefono="3000000000")
        self.cliente2 = Cliente.objects.create(nombre="Ana Gómez", telefono="3010000000")
        self.vehiculo1 = Vehiculo.objects.create(
            cliente=self.cliente1, placa="ABC123", marca="Mazda", modelo="2"
        )
        self.vehiculo2 = Vehiculo.objects.create(
            cliente=self.cliente2, placa="XYZ789", marca="Renault", modelo="Logan"
        )
        self.mecanico = Mecanico.objects.create(nombre="Carlos Mecánico")

    def datos_orden_validos(self, **overrides):
        datos = {
            "cliente": self.cliente1.id,
            "vehiculo": self.vehiculo1.id,
            "mecanico": self.mecanico.id,
            "descripcion_problema": "No enciende",
            "estado": "RECIBIDA",
        }
        datos.update(overrides)
        return datos


class ModeloYFormularioTests(BaseOrdenesTestCase):
    """Pruebas de reglas de negocio a nivel de modelo y formulario."""

    def test_numero_orden_se_genera_automaticamente(self):
        orden = OrdenServicio.objects.create(
            cliente=self.cliente1,
            vehiculo=self.vehiculo1,
            mecanico=self.mecanico,
            descripcion_problema="Revisión general",
        )
        self.assertEqual(orden.numero_orden, "OS-101")

    def test_numero_orden_es_unico_para_varias_ordenes(self):
        orden_a = OrdenServicio.objects.create(
            cliente=self.cliente1, vehiculo=self.vehiculo1,
            descripcion_problema="Falla 1",
        )
        orden_b = OrdenServicio.objects.create(
            cliente=self.cliente2, vehiculo=self.vehiculo2,
            descripcion_problema="Falla 2",
        )
        self.assertNotEqual(orden_a.numero_orden, orden_b.numero_orden)

    def test_formulario_valido_con_datos_correctos(self):
        form = OrdenServicioForm(data=self.datos_orden_validos())
        self.assertTrue(form.is_valid())

    def test_formulario_rechaza_sin_cliente(self):
        datos = self.datos_orden_validos()
        datos.pop("cliente")
        form = OrdenServicioForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn("cliente", form.errors)

    def test_formulario_rechaza_sin_descripcion(self):
        datos = self.datos_orden_validos(descripcion_problema="")
        form = OrdenServicioForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn("descripcion_problema", form.errors)

    def test_formulario_rechaza_vehiculo_de_otro_cliente(self):
        datos = self.datos_orden_validos(vehiculo=self.vehiculo2.id)
        form = OrdenServicioForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn("El vehículo seleccionado no pertenece", str(form.errors))


class VistasOrdenesTests(BaseOrdenesTestCase):
    """Pruebas de las vistas: acceso, CRUD completo, paginación y confirmación."""

    def test_lista_ordenes_responde_200(self):
        response = self.client.get("/ordenes/")
        self.assertEqual(response.status_code, 200)

    def test_formulario_crear_responde_200_en_get(self):
        response = self.client.get("/ordenes/nueva/")
        self.assertEqual(response.status_code, 200)

    def test_editar_orden_inexistente_devuelve_404(self):
        response = self.client.get("/ordenes/9999/editar/")
        self.assertEqual(response.status_code, 404)

    def test_crear_orden_sin_cliente_no_guarda_y_muestra_error(self):
        datos = self.datos_orden_validos()
        datos.pop("cliente")
        response = self.client.post("/ordenes/nueva/", datos)
        # No debe redirigir (no se guardó); debe volver a mostrar el formulario.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrdenServicio.objects.count(), 0)
        # No se compara el texto exacto del mensaje porque LANGUAGE_CODE="es-co"
        # hace que Django traduzca los mensajes de validación al español;
        # lo relevante es que el campo "cliente" quede marcado como inválido.
        self.assertTrue(response.context["form"].errors.get("cliente"))

    def test_crear_orden_con_vehiculo_de_otro_cliente_no_guarda(self):
        datos = self.datos_orden_validos(vehiculo=self.vehiculo2.id)
        response = self.client.post("/ordenes/nueva/", datos)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrdenServicio.objects.count(), 0)
        self.assertContains(response, "no pertenece")

    def test_flujo_crud_completo(self):
        # CREATE
        response = self.client.post("/ordenes/nueva/", self.datos_orden_validos())
        self.assertEqual(response.status_code, 302)
        orden = OrdenServicio.objects.get()

        # READ (listado)
        response = self.client.get("/ordenes/")
        self.assertContains(response, orden.numero_orden)

        # UPDATE
        response = self.client.post(
            f"/ordenes/{orden.pk}/editar/",
            self.datos_orden_validos(estado="REPARACION"),
        )
        self.assertEqual(response.status_code, 302)
        orden.refresh_from_db()
        self.assertEqual(orden.estado, "REPARACION")

        # DELETE
        response = self.client.post(f"/ordenes/{orden.pk}/eliminar/")
        self.assertEqual(response.status_code, 302)
        self.assertFalse(OrdenServicio.objects.filter(pk=orden.pk).exists())

    def test_eliminar_requiere_confirmacion_get_no_borra(self):
        orden = OrdenServicio.objects.create(
            cliente=self.cliente1,
            vehiculo=self.vehiculo1,
            mecanico=self.mecanico,
            descripcion_problema="Cambio de aceite",
        )
        # GET debe mostrar la página de confirmación y NO debe eliminar la orden.
        response = self.client.get(f"/ordenes/{orden.pk}/eliminar/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, orden.numero_orden)
        self.assertTrue(OrdenServicio.objects.filter(pk=orden.pk).exists())

        # POST sí elimina la orden.
        response = self.client.post(f"/ordenes/{orden.pk}/eliminar/")
        self.assertEqual(response.status_code, 302)
        self.assertFalse(OrdenServicio.objects.filter(pk=orden.pk).exists())

    def test_eliminar_orden_inexistente_devuelve_404(self):
        response = self.client.get("/ordenes/9999/eliminar/")
        self.assertEqual(response.status_code, 404)

    def test_paginacion_lista_10_por_pagina(self):
        for i in range(15):
            OrdenServicio.objects.create(
                cliente=self.cliente1,
                vehiculo=self.vehiculo1,
                mecanico=self.mecanico,
                descripcion_problema=f"Revisión {i}",
            )
        response = self.client.get("/ordenes/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["ordenes"]), 10)
        self.assertTrue(response.context["ordenes"].has_next())

        response_pag2 = self.client.get("/ordenes/?page=2")
        self.assertEqual(response_pag2.status_code, 200)
        self.assertEqual(len(response_pag2.context["ordenes"]), 5)
        self.assertFalse(response_pag2.context["ordenes"].has_next())


class ComandoDatosPruebaTests(TestCase):
    """Verifica el comando 'generar_datos_prueba' usado para poblar la
    base de datos con datos de prueba de forma reproducible."""

    def test_genera_la_cantidad_de_ordenes_solicitada(self):
        call_command("generar_datos_prueba", ordenes=20)
        self.assertEqual(OrdenServicio.objects.count(), 20)
        self.assertTrue(Cliente.objects.exists())
        self.assertTrue(Vehiculo.objects.exists())
        self.assertTrue(Mecanico.objects.exists())

    def test_respeta_regla_vehiculo_pertenece_a_cliente(self):
        call_command("generar_datos_prueba", ordenes=20)
        for orden in OrdenServicio.objects.all():
            self.assertEqual(orden.vehiculo.cliente_id, orden.cliente_id)
