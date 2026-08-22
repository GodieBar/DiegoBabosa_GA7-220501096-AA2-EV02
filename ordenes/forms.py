from django import forms
from .models import OrdenServicio

class OrdenServicioForm(forms.ModelForm):
    class Meta:
        model = OrdenServicio
        fields = ["cliente", "vehiculo", "mecanico", "descripcion_problema", "estado"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-select"}),
            "vehiculo": forms.Select(attrs={"class": "form-select"}),
            "mecanico": forms.Select(attrs={"class": "form-select"}),
            "descripcion_problema": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "estado": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "cliente": "Cliente",
            "vehiculo": "Vehículo",
            "mecanico": "Mecánico",
            "descripcion_problema": "Descripción del problema",
            "estado": "Estado",
        }

    def clean(self):
        cleaned = super().clean()
        cliente = cleaned.get("cliente")
        vehiculo = cleaned.get("vehiculo")
        if cliente and vehiculo and vehiculo.cliente_id != cliente.id:
            raise forms.ValidationError(
                "El vehículo seleccionado no pertenece al cliente seleccionado."
            )
        return cleaned
