from django.shortcuts import render, redirect
from .forms import EventoForm
from .models import Evento
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.models import LogEntry
from django.contrib.admin.models import ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from .utilidades import traducirActionFlag

# Create your views here.


def home(request):
    return render(request, 'home.html')

# pagina de administrador


def administrador(request):
    return render(request, 'administrador.html')

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
            form = EventoForm(request.POST)
            new_task = form.save(commit=False)  # para guardar la nueva tarea
            new_task.save()

            # Registrar la acción en el historial
            LogEntry.objects.log_action(
                user_id=request.user.id,  # Usuario que realiza la acción
                content_type_id=ContentType.objects.get_for_model(
                    new_task).pk,  # Tipo de contenido
                object_id=new_task.id,  # ID del evento
                object_repr=str(new_task),  # Representación del evento
                action_flag=ADDITION,  # Acción: Añadido
                change_message="Evento Creado"  # Mensaje opcional
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
                change_message="Evento Modificado"
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
            change_message="Evento Eliminado"  # Mensaje opcional
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


# historial
def historial(request):
    historial = LogEntry.objects.all()
    for registro in historial:
        registro.traduccion = traducirActionFlag(registro.action_flag)
    return render(request, 'historial.html', {'historial': historial})


# crear usuario
def crear_usuario(request):
    if request.method == 'GET':
        return render(request, 'crear_usuario.html', {
        })
