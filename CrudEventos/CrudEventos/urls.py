"""
URL configuration for CrudEventos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Eventos import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('administrador/',views.administrador,name='administrador'),
    path('eventos/',views.eventos,name='eventos'),
    path('eventos/crear',views.crear_evento,name='crear_evento'),
    path('eventos/<int:evento_id>/editar',views.evento_detail,name='evento_detail'),
    path('eventos/<int:evento_id>/eliminar',views.evento_delete,name='evento_delete'),
    path('login/',views.iniciar_sesion,name='login'),
    path('logout/',views.cerrar_sesion,name='logout'),
    path('historial/',views.historial,name='historial'),
    path('crear_usuario/',views.crear_usuario,name='crear_usuario'),
    path('eventos/confirmar/<int:evento_id>/', views.confirmar_evento, name='evento_confirmar'),
    path('eventos/confirmar/<int:evento_id>/eliminar', views.desconfirmar_evento, name='evento_desconfirmar'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil/<int:user_id>/eliminar', views.eliminar_perfil, name='eliminar_perfil'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
