from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import datetime, time
from datetime import timedelta
from django.core.exceptions import ValidationError

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        exclude = ['fecha']



class MecanicoForm(forms.ModelForm):

    class Meta:
        model = Mecanico
        fields = "__all__"
        widgets = {"fecha_nacimiento" : forms.DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d'))}


class AgregarTrabajoForm(forms.ModelForm):

    class Meta:
        model = Trabajo
        fields = "__all__"

class ModificarTrabajoForm(forms.ModelForm):
    autorizado = forms.BooleanField(required=False)

    class Meta:
        model = Trabajo
        fields = "__all__"


class CurriculumForm(forms.ModelForm):
    
    
    class Meta:
        model = Curriculum
        fields ="__all__"
        widgets = {"fecha_nacimiento" : forms.DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d'))}




class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha', 'hora', 'correo_usuario', 'nombre_cliente', 'apellido_cliente', 'telefono_cliente', 'tipo_vehiculo', 'marca_vehiculo', 'modelo_vehiculo', 'informacion_adicional']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < timezone.localdate():
            raise forms.ValidationError("No se pueden reservar fechas pasadas.")
        
        # Verifica si la fecha seleccionada es un día de la semana de lunes a viernes
        if fecha.weekday() not in [0, 1, 2, 3, 4, 5]:  
            raise forms.ValidationError("Por favor, elige un día de la semana de lunes a sabado.")

        return fecha

    def clean_hora(self):
        hora = self.cleaned_data['hora']
        fecha = self.cleaned_data.get('fecha')

        if not hora:
            return hora

        # Verifica si la hora está fuera del rango de 9 am a 6 pm
        if not (time(9, 0) <= hora <= time(18, 0)):
            raise forms.ValidationError("Por favor, selecciona una hora entre las 9 am y las 6 pm.")

        # Verifica si la fecha seleccionada es un sábado
        if fecha and fecha.weekday() == 5:  # 5 es sábado
            # Verifica si la hora está fuera del rango de 9:30 am a 3 pm para los sábados
            if not (time(9, 30) <= hora <= time(15, 0)):
                raise forms.ValidationError("El horario de los sábados es de 9:30 am a 3 pm.")

        if fecha and hora:
            # Combina la fecha y la hora para obtener una fecha y hora completas
            fecha_hora_seleccionada = datetime.combine(fecha, hora)

            # Convierte la fecha y hora a la zona horaria de Django (America/Santiago)
            fecha_hora_seleccionada = timezone.make_aware(fecha_hora_seleccionada, timezone=timezone.get_current_timezone())

            if fecha_hora_seleccionada < timezone.now():
                raise forms.ValidationError("No se pueden reservar fechas y horas pasadas.")
            
            # Verifica si la fecha y la hora ya existen en la base de datos
            reservas_existente = Reserva.objects.filter(fecha=fecha, hora=hora)
            if reservas_existente.exists():
                raise forms.ValidationError("La hora seleccionada ya está reservada. Por favor, elige otra.")

            # Verifica si hay una reserva dentro de un intervalo de media hora antes o después
            intervalo_inicio = fecha_hora_seleccionada - timedelta(minutes=30)
            intervalo_fin = fecha_hora_seleccionada + timedelta(minutes=30)
            reservas_cercanas = Reserva.objects.filter(fecha=fecha, hora__range=[intervalo_inicio.time(), intervalo_fin.time()])
            if reservas_cercanas.exists():
                raise forms.ValidationError("Ya existe una reserva dentro de un intervalo de media hora antes o después de la hora seleccionada.")

        return hora


