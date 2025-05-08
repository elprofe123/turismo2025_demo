from django import forms
from .models import Evento,Categoria

class EventoForm(forms.ModelForm):
   class Meta:
        model= Evento
        fields=['titulo','descripción','categorias','imagen']
        