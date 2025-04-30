from django.db import IntegrityError
from django.shortcuts import render, redirect
from .forms import EventoForm
from .models import Evento, Perfil
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm, User
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.models import LogEntry
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from .utilidades import  traducirActionFlag
from django.shortcuts import get_object_or_404

# Create your views here.


def home(request):
    return render(request, 'home.html')

# pagina de administrador
def administrador(request):
    eventos_pendientes = Evento.objects.filter(checked=False)  # Eventos no confirmados
    eventos_confirmados = Evento.objects.filter(checked=True)  # Eventos confirmados
    return render(request, 'administrador.html', {
        'eventos_pendientes': eventos_pendientes,
        'eventos_confirmados': eventos_confirmados
    })

# pagina de eventos
def eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos.html', {'eventos': eventos})

# crear evento
def crear_evento(request):
    if request.method == 'GET':
        return render(request, 'crear_evento.html', {
            'form': EventoForm
        })
    else:
        try:
            # guarda los datos en un nuevo formulario
            form = EventoForm(request.POST,request.FILES)
            new_task = form.save(commit=False)  # para guardar la nueva tarea
            new_task.save()

            # Registrar la acción en el historial
            LogEntry.objects.log_action(
                user_id=request.user.id,  # Usuario que realiza la acción
                content_type_id=ContentType.objects.get_for_model(new_task).pk,  # Tipo de contenido
                object_id=new_task.id,  # ID del evento
                object_repr=str(new_task),  # Representación del evento
                action_flag=ADDITION,  # Acción: Añadido
                change_message="Evento creado"  # Mensaje opcional
            )
            return redirect('eventos')
        except ValueError:
            return render(request, 'crear_evento.html', {
                'form': EventoForm,
                'error': 'Por favor prove datos validos'
            })


# editar evento
def evento_detail(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    if request.method == 'GET':
        form = EventoForm(instance=evento)
        return render(request, 'evento_detail.html', {'form': form, 'evento': evento})
    else:
        try:
            form = EventoForm(request.POST, instance=evento)
            form.save()
            
            # Registrar la acción en el historial
            LogEntry.objects.log_action(
            user_id=request.user.id,  
            content_type_id=ContentType.objects.get_for_model(evento).pk, 
            object_id=evento.id,  
            object_repr=str(evento),  
            action_flag=CHANGE,  
            change_message="Evento modificado"  
            )


            return redirect('eventos')
        except ValueError:
            return render(request, 'evento_detail.html', {'form': form, 'evento': evento, 'error': 'Error al editar el evento'})

# eliminar evento
def evento_delete(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    if request.method == 'POST':
        # Registrar la acción en el historial
         LogEntry.objects.log_action(
            user_id=request.user.id,  # Usuario que realiza la acción
            content_type_id=ContentType.objects.get_for_model(evento).pk,  # Tipo de contenido
            object_id=evento.id,  # ID del evento
            object_repr=str(evento),  # Representación del evento
            action_flag=DELETION,  # Acción: Añadido
            change_message="Evento eliminado"  # Mensaje opcional
            )

    evento.delete()
    return redirect('eventos')

    
# login
def iniciar_sesion(request):
    if request.method == "GET":
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o Contraseña no encontrados'
            })
        else:
            login(request, user)
            return redirect('administrador')

# cerrar sesion
def cerrar_sesion(request):
    logout(request)
    return redirect('home')


#historial
def historial(request):
    historial = LogEntry.objects.all()
    for registro in historial:
        registro.traduccion = traducirActionFlag(registro.action_flag)
    return render(request, 'historial.html' , {'historial': historial})


#crear usuario 
def crear_usuario(request):
    if request.method == 'GET':
        return render(request, 'crear_usuario.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:   

            try:
                user = User.objects.create_user(
                        username=request.POST['username'], password=request.POST['password1'])
                user.save()

                 # Crear el perfil asociado
                perfil = Perfil.objects.create(user=user)
                if 'profile_picture' in request.FILES:
                    perfil.imagen = request.FILES['profile_picture']
                perfil.save()

                login(request, user)  # para autenticar usuario
                # usuario creado y se redirecciona a esta pagina
                return redirect('perfil')
            except IntegrityError:
                # return HttpResponse('Username already exits') # usuario ya existente
                return render(request, 'crear_usuario.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        # contraseñas no coinciden
        return render(request, 'crear_usuario.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })
    
# Confirmar evento
def confirmar_evento(request, evento_id):
     # Definir el código de acción para la confirmación
    if request.method == 'POST' and request.user.is_authenticated:
        evento = get_object_or_404(Evento, id=evento_id)
        evento.checked = True  # Cambiar el estado a confirmado
        evento.save()

        LogEntry.objects.log_action(
                user_id=request.user.id,  # Usuario que realiza la acción
                content_type_id=ContentType.objects.get_for_model(evento).pk,  # Tipo de contenido
                object_id=evento.id,  # ID del evento
                object_repr=str(evento),  # Representación del evento
                action_flag=CHANGE,  # Acción: Añadido
                change_message="Evento confirmado"  # Mensaje opcional
            )
        return redirect('eventos')  # Redirigir a la lista de eventos
    return redirect('login')  # Si no está autenticado, redirigir al login

# desconfirmar evento
def desconfirmar_evento(request,evento_id):
    if request.method == 'POST' and request.user.is_authenticated:
        evento = get_object_or_404(Evento,id=evento_id)
        evento.checked = False
        evento.save()

        LogEntry.objects.log_action(
                user_id=request.user.id,  # Usuario que realiza la acción
                content_type_id=ContentType.objects.get_for_model(evento).pk,  # Tipo de contenido
                object_id=evento.id,  # ID del evento
                object_repr=str(evento),  # Representación del evento
                action_flag=CHANGE,  # Acción: Añadido
                change_message="Evento desconfirmado"  # Mensaje opcional
            )
        return redirect('eventos')  # Redirigir a la lista de eventos
    return redirect('login')  # Si no está autenticado, redirigir al login


# vista de perfil de usuario
def perfil_usuario(request):
    if request.method == 'GET':
        perfil = Perfil.objects.filter(user=request.user).first() 
        return render(request, 'perfil_usuario.html', {
            'user': request.user,
            'imagen': perfil.imagen.url if perfil and perfil.imagen else None
        })


def eliminar_perfil(request, user_id):
    user = get_object_or_404(Perfil,user_id=user_id)
    if request.method == 'POST':
        #user = request.user
        user.user.delete()
        return redirect('home')  # Redirigir a la página de administrador después de eliminar el usuario