from django import forms
from .models import MonthlyCapex, Transferencia

class PrevisaoMesForm(forms.ModelForm):
    class Meta:
        model = MonthlyCapex
        fields = ["previsto"]
        widgets = {
            "previsto": forms.NumberInput(attrs={"step": "0.001", "class": "num-input"}),
        }

PrevisaoMesFormSet = forms.modelformset_factory(
    MonthlyCapex, form=PrevisaoMesForm, extra=0
)

class TransferenciaForm(forms.ModelForm):
    class Meta:
        model = Transferencia
        fields = ["valor", "de_para"]
        widgets = {
            "valor": forms.NumberInput(attrs={"step": "0.001", "class": "num-input"}),
            "de_para": forms.Textarea(attrs={"rows": 2}),
        }
