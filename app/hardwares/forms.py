from django import forms


class AvaliacaoForms(forms.Form):
    texto = forms.CharField(label="Texto", max_length=1000, required=False)
    url = forms.URLField(label="URL", max_length=1000, required=False)
