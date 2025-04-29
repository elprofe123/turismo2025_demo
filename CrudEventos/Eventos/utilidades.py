from django.contrib.admin.models import LogEntry
#from django.contrib.auth.models import Permission

# Aqui pondremos algunas funciones que nos ayden con la logica


# esta funcion es para traducir el action_flag del historial del admin
def traducirActionFlag(flag):
    if flag == 1:
        return "Añadido"
    elif flag == 2:
        return "Modificado"
    elif flag == 3:
        return "Borrado"
    return "Acción desconocida"



