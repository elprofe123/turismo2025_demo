from django.shortcuts import render, redirect
from .forms import EventoForm
from .models import Evento
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
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
            return redirect('eventos')
        except ValueError:
            return render(request, 'evento_detail.html', {'form': form, 'evento': evento, 'error': 'Error al editar el evento'})

# eliminar evento


def evento_delete(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    if request.method == 'POST':
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


def cerrar_sesion(request):
    logout(request)
    return redirect('home')