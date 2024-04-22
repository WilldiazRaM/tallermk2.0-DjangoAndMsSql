from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from datetime import datetime
from django.core.mail import send_mail ##RESERVA SON 4
from django.views.decorators.csrf import csrf_exempt
from django.views import View #confirmacion de reserva
from django.http import HttpResponseServerError
from django.core.exceptions import PermissionDenied
from django.db.models import Count
import json
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from datetime import timedelta







# Create your views here.
def home(request):
    trabajos = Trabajo.objects.filter(autorizado=True, imagenes__isnull=False)
    publicidades = Publicidad.objects.all()

    context = {
        'trabajos': trabajos,
        'publicidades': publicidades,
        'max_ancho': 800,  # Ajusta este valor según tus preferencias
        'max_alto': 600,   # Ajusta este valor según tus preferencias
    }

    return render(request, 'home.html', context)


def detalle_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, pk=contacto_id)
    return render(request, 'detalle_contacto.html', {'contacto': contacto})


def contacto(request):
    data = {
        'form': ContactoForm(),
        'mensaje': ""
    }

    if request.method == "POST":
        formulario = ContactoForm(data=request.POST)

        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Formulario Enviado Correctamente!"
            messages.success(request, "Formulario Enviado con Éxito. \n Gracias por preferir Garaje Los Hermanos")

            # Obtener datos del formulario
            nombre = formulario.cleaned_data['nombre']
            tipo_contacto = formulario.cleaned_data['tipo_contacto']
            mensaje_usuario = formulario.cleaned_data['mensaje']

            # Asunto del correo dependiendo del tipo de contacto
            if tipo_contacto == 0:
                asunto = 'Sugerencia'
            else:
                asunto = 'Reclamo'

            # Crear el cuerpo del correo con formato HTML
            mensaje_correo = render_to_string('FormatoEmail/contacto_formato.html', {
                'nombre': nombre,
                'tipo_contacto': asunto,
                'mensaje_usuario': mensaje_usuario
            })

            # Enviar correo electrónico a contacto@garajeloshermanos.cl
            send_mail(
                'Nuevo formulario de contacto',
                None,  # El cuerpo ya está incluido en 'mensaje_correo'
                None,  # O deja esto vacío si prefieres
                ['contacto@garajeloshermanos.cl'],  # Reemplaza con la dirección de destino
                html_message=mensaje_correo,
                fail_silently=False,
            )

        else:
            data['form'] = formulario

    return render(request, 'contacto.html', data)





def galeriaMecanicos(request):
    mecanicos = Mecanico.objects.all()
    data = {
        'mecanicos': mecanicos
    }

    if request.method == "POST":
        valor_buscar = request.POST.get("valor_buscar")
        if valor_buscar != "":
            mecanicos_filtrados = Mecanico.objects.filter(nombre=valor_buscar)
            data["mecanicos"] = mecanicos_filtrados
            print(valor_buscar)
        else:
            data["mecanicos"] = Mecanico.objects.all()

    return render(request, 'galeriaMecanicos.html', data)

def agregar_mecanico(request):
    data = {
        'form': MecanicoForm(),
        'mensaje': ""
    }

    if request.method == 'POST':
        formulario = MecanicoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Mecanico Guardado"
            messages.success(request, "Mecanico Agregado Correctamente")
        else:
            data['form'] = formulario
            data['mensaje'] = "-Ocurrió un error-"
            messages.error(request, "No se pudo agregar el Mecanico")

    return render(request, "Mantenedor/mecanico/agregar.html", data)


def listar_mecanico(request):

    mecanicos = Mecanico.objects.all()
    
    data = {
        'mecanicos': mecanicos
        
        
    }

    return render(request, "Mantenedor/mecanico/listar.html", data)



def modificar_mecanico(request, rut):

    mecanico = get_object_or_404(Mecanico, rut=rut)

    data= {
        "form": MecanicoForm(instance=mecanico)
    }

    if request.method == "POST":
        formulario = MecanicoForm(data=request.POST, instance=mecanico, files=request.FILES)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Mecanido modificado con Exito")
            return redirect(to="listar_mecanico")
        else:
            data['form'] = formulario
            data['mensaje'] = "Ocurrio un error"

    return render(request, "Mantenedor/mecanico/modificar.html", data)


def eliminar_mecanico(request, rut):
    mecanico = get_object_or_404(Mecanico, rut=rut)

    mecanico.delete()
    messages.success(request, "Mecanido Eliminado")

    return redirect(to=listar_mecanico)


def login_usuario(request):
    print("Bienvenido: " + request.user.username)
    print("este es el login")

    # Obtener todos los grupos al que pertenece el usuario
    print('grupos:', request.user.groups.all())

    # Validar si un usuario pertenece a un grupo determinado
    if request.user.groups.filter(name='Mecanico').exists():
        print("Es un Mecanico")
    else:
        print("Es administrador")

    return redirect('home')  # Reemplaza 'home' con el nombre de la URL de tu página principal


def registro_mecanico(request):
    data = {
        "mensaje": ""
    }
    if request.POST:
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        correo = request.POST.get("correo")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            data["mensaje"] = "Las contraseñas deben ser iguales."
        else:
            try:
                usu = User()
                usu.set_password(password1)
                usu.email = correo
                usu.username = nombre
                usu.last_name = apellido
                usu.first_name = nombre
                usu.save()

                grupo = Group.objects.get(name="mecanico")
                usu.groups.add(grupo)

                data['mensaje'] = 'Usuario creado con éxito'

                user = authenticate(username=usu.username, password=password1)
                login(request, user)
                return redirect(to='home')
            except Exception as e:
                data['mensaje'] = 'Error al registrar: {}'.format(str(e))

    return render(request, "registration/registro.html", data)

def detalle_mecanico(request, pk):
    mecanico = get_object_or_404(Mecanico, pk=pk)
    # Aquí puedes realizar cualquier lógica adicional necesaria para mostrar los detalles del mecánico
    return render(request, 'detalle_mecanico.html', {'mecanico': mecanico})


def agregar_trabajo(request):

    data = {
        'form': AgregarTrabajoForm,
        'mensaje':""

    }
    if request.method == "POST":
        formulario = AgregarTrabajoForm(data=request.POST, files=request.FILES)

        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Trabajo Guardado con Exito ")
            data['mensaje']= "Trabajo Guardado"
        else:
            data['form'] = formulario
            data['mensaje'] = "Ocurrio un error al agregar El trabajo"

    return render(request, "Mantenedor/Trabajo/agregarTrabajo.html", data)


def listar_trabajos (request):

    trabajos = Trabajo.objects.all()

    data = {
            'trabajos': trabajos
            }

    return render(request, "Mantenedor/Trabajo/listarTrabajo.html", data)



def listar_trabajo4Mecanico(request):   

    trabajos = Trabajo.objects.all()

    data = { 
        'trabajos' : trabajos
    } 
        
    return render(request, "Mantenedor/Trabajo/listarTrabajoMecanico.html", data)






def modificar_trabajo(request, titulo):
    trabajo = get_object_or_404(Trabajo, titulo=titulo)

    data = {
        "form": AgregarTrabajoForm(instance=trabajo)
    }

    return render(request, "Mantenedor/Trabajo/modificarTrabajo.html", data)    

def autorizar_trabajo(request, pk):
    trabajo = get_object_or_404(Trabajo, pk=pk)
    trabajo.autorizado = True
    trabajo.save()
    return redirect('listar_trabajo')

def rechazar_trabajo(request, pk):
    trabajo = get_object_or_404(Trabajo, pk=pk)
    trabajo.autorizado = False
    trabajo.save()
    return redirect('listar_trabajo')


def trabaja_con_nosotros(request):

    data = {

        'form': CurriculumForm,
        'mensaje':""
        
    }
    if request.method == "POST":
        formulario = CurriculumForm(data=request.POST, files=request.FILES)

        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Curriculum Enviado con Exito!"
            messages.success(request, "Postulacion enviada correctamente")
        else:
            data['form'] = formulario
            data['mensaje'] = "Ocurrio un error"

    
    return render(request, "TrabajaConNosotros.html", data)


def listarTrabajoHome(request, titulo):
    trabajos = Trabajo.objects.filter(titulo=titulo)

    data = {
        "trabajos": trabajos,
        "titulo": titulo
    }

    return render(request, "Mantenedor/Trabajo/listarTrabajoHome.html", data)

def listarCurriculums(request):
    curriculums = Curriculum.objects.all()
    
    data = {
        'curriculums': curriculums
    }

    return render(request, "Mantenedor/Curriculum/listarCurriculum.html", data)

def verPostulacion(request, pk):

    curriculum = get_object_or_404(Curriculum,pk=pk)

    data = {
        'curriculum' : curriculum
    }


    return render(request, "Mantenedor/Curriculum/detalleCurriculum.html", data)

def eliminarCurriculum(request, pk):

    curriculum = get_object_or_404(Curriculum, pk=pk)
    curriculum.delete()
    messages.success(request, "Postulacion Eliminada Correctamente")

    return redirect(to=listarCurriculums)






##ViEWS DE LOS SERVICIOS:
    
def mecanica_autos(request):
    automotrices = Automotriz.objects.all()  # Obtener todos los objetos de Automotriz
    return render(request, 'Servicios/mecanicaAutos.html', {'automotrices': automotrices})
    
def mecanica_motos(request):
    motos = Motos.objects.all()
    return render(request, 'Servicios/mecanicaMotos.html', {'motos': motos})

def pintura_automotriz(request):
    pinturas = Pintura.objects.all()
    return render(request, 'Servicios/PinturaA.html', {'pinturas': pinturas})
    

def restauracion(request):
    restauraciones = Restauracion.objects.all()
    return render(request, 'Servicios/restauracion.html', {'restauraciones': restauraciones})

## END VIEWS DE SERVICIOS
##RESERVAs


def custom_validation_function(reserva):
    # Convierte la hora de la reserva a un objeto de fecha y hora
    fecha_hora_seleccionada = datetime.combine(reserva.fecha, reserva.hora)

    # Convierte la fecha y hora a la zona horaria de Django (America/Santiago)
    fecha_hora_seleccionada = timezone.make_aware(fecha_hora_seleccionada, timezone=timezone.get_current_timezone())

    if fecha_hora_seleccionada < timezone.now():
        raise ValidationError("No se pueden reservar fechas y horas pasadas.")

    # Verifica si ya existe una reserva para la misma fecha y hora exacta
    reservas_existente = Reserva.objects.filter(fecha=reserva.fecha, hora=reserva.hora)
    if reservas_existente.exists():
        raise ValidationError("Ya existe una reserva para la misma fecha y hora.")

    # Calcula la hora siguiente sumando media hora a la hora actual
    hora_siguiente = timezone.now() + timedelta(minutes=30)

    # Verifica si existe alguna reserva para la hora siguiente
    reservas_siguiente_hora = Reserva.objects.filter(fecha=hora_siguiente.date(), hora=hora_siguiente.time())
    if reservas_siguiente_hora.exists():
        raise ValidationError("Ya existe una reserva para la hora siguiente.")

    # Si todo está bien, retorna True
    return True


@csrf_protect
@csrf_exempt
def reserva_view(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)

            if not custom_validation_function(reserva):
                form.add_error(None, "Error en la reserva. Por favor, verifica la información.")
                return render(request, 'reserva/reserva.html', {'form': form})

            reserva.save()
            messages.success(request, "Hora agendada")
            # Establece una variable de sesión para indicar que la reserva se ha completado
            request.session['reserva_realizada'] = reserva.id

            html_message = render_to_string('FormatoEmail/reservas_formato.html', {'reserva': reserva})
            
            email_subject = 'Confirmación de Reserva GarajelosHermanos.cl'
            email_body = 'Tu reserva ha sido confirmada. Te esperamos! Garajeloshermanos.cl'
            sender_email = settings.EMAIL_HOST_USER
            recipient_email = [reserva.correo_usuario]
            send_mail(email_subject, email_body, sender_email, recipient_email, fail_silently=False, html_message=html_message)

            send_mail(
                'Nueva Reserva',
                'Se ha realizado una nueva reserva.',
                settings.EMAIL_HOST_USER,
                ['jefedetaller@garajeloshermanos.cl'],
                fail_silently=False,
            )

            # Redirecciona a la vista de confirmación de reserva con el ID de la reserva
            return redirect('reservconfirmed', reserva_id=reserva.id)

    else:
        form = ReservaForm()

    return render(request, 'reserva/reserva.html', {'form': form})

class ConfirmacionView(View):
    def get(self, request, *args, **kwargs):
        try:
            reserva_id = kwargs['reserva_id']

            # Verifica la variable de sesión antes de mostrar la página
            if request.session.get('reserva_realizada') != reserva_id:
                raise PermissionDenied("Acceso no autorizado. Vuelve a <a href='https://www.garajeloshermanos.cl/'>Garajeloshermanos.cl .</a> \n Si ya realizaste una reserva, revisa tu correo electrónico. atte. Equipo de Garaje los Hermanos.")

            reserva = Reserva.objects.get(pk=reserva_id)

            # Limpia la variable de sesión después de mostrar la página de confirmación
            del request.session['reserva_realizada']

            return render(request, 'reserva/confirmed.html', {'reserva': reserva})
        except (PermissionDenied, Reserva.DoesNotExist):
            return HttpResponseNotFound("Acceso no autorizado. Vuelve a <a href='https://www.garajeloshermanos.cl/'>Garajeloshermanos.cl .</a> \n Si ya realizaste una reserva, revisa tu correo electrónico. atte. Equipo de Garaje los Hermanos.")
        except Exception as e:
            return HttpResponseServerError(f"Error en la confirmación: {str(e)}")





def error_404(request, exception):
    return render(request, '404.html', status=404)

