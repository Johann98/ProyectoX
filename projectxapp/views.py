from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Proyecto, Tarea, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

# Create your views here.


def crear_cuenta(request):
    if (request.method == 'POST' and 'registrar' in request.POST):
        username=request.POST.get('username', '')
        first_name=request.POST.get('first_name', '')
        last_name=request.POST.get('last_name', '')
        email=request.POST.get('email', '')
        password=request.POST.get('password', '')
        user_obj = User(username=username, first_name=first_name, last_name=last_name, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return HttpResponseRedirect('/')
    else:
        return render(request, 'projectxapp/register.html')


def form_login(request):
    if (request.method == 'POST' and 'login' in request.POST):
        usuario = request.POST.get('usuario', '')
        clave = request.POST.get('password', '')
        print(usuario)
        print(clave)

        u = authenticate(username=usuario, password=clave)
        print("AUTHENTICATION")
        print(u)

        if u is None:
            return HttpResponseRedirect(reverse('e404'))
        else:
            login(request, u)
            return HttpResponseRedirect(reverse('inicio'))
    else:
        return render(request, 'projectxapp/login.html')


def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('form_login'))

def e404(request):
    return render(request, 'projectxapp/404.html')

# def auth_login(request):
#
#     usuario = request.POST['usuario']
#     clave = request.POST['password']
#     print(usuario)
#     print(clave)
#
#     u = authenticate(username=usuario, password=clave)
#     print("AUTHENTICATION")
#     print(u)
#
#     if u is None:
#         return HttpResponseRedirect(reverse('e404'))
#     else:
#         login(request, u)
#         return HttpResponseRedirect(reverse('inicio'))



def forgot_password(request):
    return render(request, 'projectxapp/forgot_password.html')






@login_required
def inicio(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    context = {'first_name':first_name, 'last_name':last_name}
    return render(request, 'projectxapp/inicio.html', context)
####################################PROYECTOS#################################
@login_required
def proyectos(request):
    #Obtiene los nombres de los proyectos de la base de datos
    pryts = Proyecto.objects.all()
    #Agrega los proyectos al contexto
    first_name = request.user.first_name
    last_name = request.user.last_name
    context = {'first_name':first_name, 'last_name':last_name, 'proyectos':pryts}
    #Muestra el template enviando el contexto
    return render(request, 'projectxapp/MisProyectos.html', context)

@login_required
def proyectodetalles(request):

@login_required
def form_proyectos(request):
    if (request.method == 'POST' and 'crearproyecto' in request.POST):
        titulo=request.POST.get('titulo', '')
        descripcion=request.POST.get('descripcion', '')
        arquitecto_id=request.POST.get(request.user.id, '')
        print(request.user.id)
        project_obj = Proyecto(titulo=titulo, descripcion=descripcion, arquitecto_id=request.user.id)
        project_obj.save()
        return HttpResponseRedirect('/proyectos/')
    else:
        first_name = request.user.first_name
        last_name = request.user.last_name
        context = {'first_name':first_name, 'last_name':last_name}
        return render(request, 'projectxapp/form_proyectos.html', context)


@login_required
def crear_proyecto(request):
     return HttpResponseRedirect(reverse('proyectos'))

####################################TAREAS###################################

@login_required
def tareas(request):
    #Obtiene
    t = Tarea.objects.all()
    #Agrega
    contexto = {
        'tareas': t
    }
    #Muestra
    return render(request, 'projectxapp/MisTareas.html', contexto)

@login_required
def form_tareas(request):
    pyrs = Proyecto.objects.all()
    contexto={
        'proyectos': pyrs
    }
    return render(request, 'projectxapp/form_tareas.html', contexto)


@login_required
def crear_tarea(request):
    # #Obtiene el nombre digitado por el usuario
    # titulo = request.POST['nombre_tarea']
    # proyecto_id = request.POST['']
    # desarrolladores =  request.POST['']
    # #Obtiene el id del proyecto de la tarea
    # proyecto_id = Tarea.objects.get(pk=int(tarea_id)) ###Esta linea no estoy seguro
    # #Crea la tarea
    # t = Tarea()
    # t.titulo = titulo
    # t.activo = True
    # t.proyecto_id = proyecto_id
    # t.fecha_creacion = fecha_creacion
    # t.desarrolladores = desarrolladores

    # #Guarda la tarea
    # t.save()
    return HttpResponseRedirect(reverse('tareas'))
