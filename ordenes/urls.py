from django.urls import path
from . import views

app_name = "ordenes"

urlpatterns = [
    path("", views.lista_ordenes, name="lista"),
    path("nueva/", views.crear_orden, name="crear"),
    path("<int:pk>/editar/", views.editar_orden, name="editar"),
    path("<int:pk>/eliminar/", views.eliminar_orden, name="eliminar"),
]
