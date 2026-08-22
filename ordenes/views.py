from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .forms import OrdenServicioForm
from .models import OrdenServicio

def lista_ordenes(request):
    """Lista paginada (10 por página) de órdenes de servicio."""
    qs = OrdenServicio.objects.select_related("cliente", "vehiculo", "mecanico")
    paginator = Paginator(qs, 10)
    ordenes = paginator.get_page(request.GET.get("page"))
    return render(request, "ordenes/lista.html", {"ordenes": ordenes})

def crear_orden(request):
    """GET muestra el formulario vacío. POST valida y crea la orden."""
    if request.method == "POST":
        form = OrdenServicioForm(request.POST)
        if form.is_valid():
            orden = form.save()
            messages.success(request, f"Orden {orden.numero_orden} creada correctamente.")
            return redirect("ordenes:lista")
        messages.error(request, "Revisa los datos del formulario: hay errores de validación.")
    else:
        form = OrdenServicioForm()
    return render(request, "ordenes/formulario.html", {"form": form, "titulo": "Nueva orden"})

def editar_orden(request, pk):
    """GET muestra el formulario con los datos actuales. POST valida y guarda cambios."""
    orden = get_object_or_404(OrdenServicio, pk=pk)
    if request.method == "POST":
        form = OrdenServicioForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            messages.success(request, f"Orden {orden.numero_orden} actualizada correctamente.")
            return redirect("ordenes:lista")
        messages.error(request, "Revisa los datos del formulario: hay errores de validación.")
    else:
        form = OrdenServicioForm(instance=orden)
    return render(
        request,
        "ordenes/formulario.html",
        {"form": form, "titulo": f"Editar orden {orden.numero_orden}"},
    )

def eliminar_orden(request, pk):
    """GET muestra una página de confirmación. Solo POST (con CSRF) elimina."""
    orden = get_object_or_404(OrdenServicio, pk=pk)
    if request.method == "POST":
        numero = orden.numero_orden
        orden.delete()
        messages.success(request, f"Orden {numero} eliminada correctamente.")
        return redirect("ordenes:lista")
    return render(request, "ordenes/eliminar_confirmar.html", {"orden": orden})
