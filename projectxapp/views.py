from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Proyecto, Tarea, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
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

@login_required
def perfil(request):
    if (request.method == 'POST' and 'modificar' in request.POST):
        first_name=request.POST.get('first_name', '')
        last_name=request.POST.get('last_name', '')
        username=request.POST.get('username', '')
        email=request.POST.get('email', '')
        password=request.POST.get('password', '')

        user_obj = User.objects.get(id=request.user.id)

        if(first_name!=''):
            user_obj.first_name=first_name
        if(last_name!=''):
            user_obj.last_name=last_name
        if(username!=''):
            user_obj.username=username
        if(email!=''):
            user_obj.email=email
        if(password!=''):
            user_obj.set_password(password)
        user_obj.save()
        update_session_auth_hash(request, user_obj)
        # if (password!=''):
        #     return HttpResponseRedirect('/login/')
        # else:
        return HttpResponseRedirect('/perfil/')
    else:
        first_name = request.user.first_name
        last_name = request.user.last_name
        username = request.user.username
        email = request.user.email
        context = {'first_name':first_name, 'last_name':last_name, 'username':username, 'email':email}
        return render(request, 'projectxapp/perfil.html', context)
####################################PROYECTOS#################################
@login_required
def proyectos(request):
    #Obtiene los nombres de los proyectos de la base de datos
    pryts = Proyecto.objects.all().filter(arquitecto_id=request.user.id)
    #Agrega los proyectos al contexto
    first_name = request.user.first_name
    last_name = request.user.last_name
    context = {'first_name':first_name, 'last_name':last_name, 'proyectos':pryts}
    #Muestra el template enviando el contexto
    return render(request, 'projectxapp/MisProyectos.html', context)

@login_required
def proyectodetalles(request, id):
    project_obj = Proyecto.objects.get(id=id)
    arquitecto = User.objects.get(id=project_obj.arquitecto_id)
    tasks = Tarea.objects.all().filter(proyecto_id=id)
    first_name = request.user.first_name
    last_name = request.user.last_name
    print(tasks)
    context = {'first_name':first_name, 'last_name':last_name, 'proyecto':project_obj, 'tareas':tasks, 'arquitecto':arquitecto}
    return render(request, 'projectxapp/proyecto.html', context)

@login_required
def borrartarea(request, tareaid, proyectoid):
    Tarea.objects.filter(id=tareaid).delete()
    return HttpResponseRedirect('/proyectodetalles/'+proyectoid)

@login_required
def borrarproyecto(request, id):
    Proyecto.objects.filter(id=id).delete()
    return HttpResponseRedirect('/proyectos/')


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



@login_required
def form_tareas(request, id):
    if (request.method == 'POST' and 'creartarea' in request.POST):
        titulo=request.POST.get('titulo', '')
        descripcion=request.POST.get('descripcion', '')
        developers=request.POST.getlist('developers')
        print("developers")
        print(developers)
        desarrolladores=""
        print("dev length")
        print(len(developers))
        for i in developers:
            desarrolladores=desarrolladores+i+","
        desarrolladores = desarrolladores[:-1]
        j=0
        estados=""
        while(j<len(developers)):
            estados=estados+"activo,"
            j=j+1
        estados = estados[:-1]
        print(estados)
        tarea_obj = Tarea(titulo=titulo, descripcion=descripcion, desarrolladores=desarrolladores, estados=estados, avance=0, proyecto_id=id)
        tarea_obj.save()

        return HttpResponseRedirect('/proyectodetalles/'+ id)
    else:
        first_name = request.user.first_name
        last_name = request.user.last_name
        users = User.objects.all()
        users2=[]
        for user in users:
            if (user.id!=request.user.id):
                users2.append(user)
        context = {'first_name':first_name, 'last_name':last_name, 'users':users2}
        return render(request, 'projectxapp/form_tareas.html', context)

@login_required
def tareadetalles(request, id):
    if (request.method == 'POST' and 'actualizarprogreso' in request.POST):
        print("id")
        print(id)
        progreso=request.POST.get('progreso', '')
        tarea_obj = Tarea.objects.get(id=id)
        tarea_obj.avance=progreso
        tarea_obj.save()
        return HttpResponseRedirect('/tareadetalles/'+ id)
    elif (request.method == 'POST' and 'agregar' in request.POST):
        newdevs=request.POST.getlist('newdevelopers')
        print("newdevs")
        print(newdevs)
        if newdevs:
            ndes=""
            for i in newdevs:
                ndes=ndes+i+","
            ndes = ndes[:-1]
            tarea_obj=Tarea.objects.get(id=id)
            olddevs=tarea_obj.desarrolladores
            oldstates=tarea_obj.estados
            if(olddevs==""):
                newdevs=ndes
            else:
                newdevs=olddevs+","+ndes
            if(oldstates==""):
                j=0
                newstates=""
                while(j<len(newdevs)):
                    newstates=newstates+"activo,"
                    j=j+1
                newstates = newstates[:-1]
            else:
                newstates=oldstates+","
                j=0
                while(j<len(newdevs)):
                    newstates=newstates+"activo,"
                    j=j+1
                newstates = newstates[:-1]
            tarea_obj.desarrolladores=newdevs
            tarea_obj.estados=newstates
            tarea_obj.save()
        return HttpResponseRedirect('/tareadetalles/'+ id)
    else:
        tarea_obj = Tarea.objects.get(id=id)
        proyecto_obj = Proyecto.objects.get(id=tarea_obj.proyecto_id)
        owner_obj= User.objects.get(id=proyecto_obj.arquitecto_id)
        developers=tarea_obj.desarrolladores
        desarrolladores=[]
        desarrolladoreslist=developers.split(",")
        for x in desarrolladoreslist:
            usuario = User.objects.get(id=int(x))
            desarrolladores.append(usuario)
        states=tarea_obj.estados
        estados=[]
        estadoslist=states.split(",")
        for x in estadoslist:
            estados.append(x)
        if (request.user.id!=owner_obj.id):
            numf=desarrolladoreslist.index(str(request.user.id))
            estado=estadoslist[numf]
        else:
            estado=""
        tasks = Tarea.objects.all().filter(id=id)
        first_name = request.user.first_name
        last_name = request.user.last_name

        newusers=[]
        users = User.objects.all()
        users2=[]
        for user in users:
            if (user.id!=request.user.id):
                users2.append(user)
        for user in users2:
            if str(user.id) not in desarrolladoreslist:
                newusers.append(user)

        desarrolladoresdata=zip(desarrolladores,estados)
        context = {'first_name':first_name, 'last_name':last_name, 'tarea':tarea_obj, 'proyecto':proyecto_obj,
        'desarrolladoresdata':desarrolladoresdata, 'newusers':newusers, 'desarrolladores':desarrolladores, 'owner':owner_obj, 'estado':estado}
        return render(request, 'projectxapp/tarea.html', context)

@login_required
def borrardev(request, tareaid, devid):
    tarea_obj = Tarea.objects.get(id=tareaid)
    devs=tarea_obj.desarrolladores
    states=tarea_obj.estados
    devlist=devs.split(",")
    statelist=states.split(",")
    numf=devlist.index(devid)
    devlist.pop(numf)
    statelist.pop(numf)
    ndevs=""
    nstates=""
    for i in devlist:
        ndevs=ndevs+i+","
    for i in statelist:
        nstates=nstates+i+","
    ndevs = ndevs[:-1]
    nstates = nstates[:-1]
    tarea_obj.desarrolladores=ndevs
    tarea_obj.estados=nstates
    tarea_obj.save()
    return HttpResponseRedirect('/tareadetalles/'+ tareaid)

@login_required
def activar(request, tareaid, devid):
    tarea_obj = Tarea.objects.get(id=tareaid)
    devs=tarea_obj.desarrolladores
    states=tarea_obj.estados
    devlist=devs.split(",")
    statelist=states.split(",")
    numf=devlist.index(devid)
    statelist[numf]="activo"
    nstates=""
    for i in statelist:
        nstates=nstates+i+","
    nstates = nstates[:-1]
    tarea_obj.estados=nstates
    tarea_obj.save()
    return HttpResponseRedirect('/tareadetalles/'+ tareaid)

@login_required
def desactivar(request, tareaid, devid):
    tarea_obj = Tarea.objects.get(id=tareaid)
    devs=tarea_obj.desarrolladores
    states=tarea_obj.estados
    devlist=devs.split(",")
    statelist=states.split(",")
    numf=devlist.index(devid)
    statelist[numf]="desactivado"
    nstates=""
    for i in statelist:
        nstates=nstates+i+","
    nstates = nstates[:-1]
    tarea_obj.estados=nstates
    tarea_obj.save()
    return HttpResponseRedirect('/tareadetalles/'+ tareaid)

@login_required
def tareas(request):
    tareas = Tarea.objects.all()
    mistareas=[]
    for tarea in tareas:
        devs=tarea.desarrolladores
        devlist=devs.split(",")
        if str(request.user.id) in devlist:
            mistareas.append(tarea)
    print(request.user.id)
    #print(devlist)
    print(mistareas)
    first_name = request.user.first_name
    last_name = request.user.last_name
    context = {'first_name':first_name, 'last_name':last_name, 'tareas':mistareas}
    return render(request, 'projectxapp/MisTareas.html', context)


####################################TAREAS###################################

# @login_required
# def tareas(request):
#     #Obtiene
#     t = Tarea.objects.all()
#     #Agrega
#     contexto = {
#         'tareas': t
#     }
#     #Muestra
#     return render(request, 'projectxapp/MisTareas.html', contexto)

# @login_required
# def form_tareas(request):
#     pyrs = Proyecto.objects.all()
#     contexto={
#         'proyectos': pyrs
#     }
#     return render(request, 'projectxapp/form_tareas.html', contexto)


# @login_required
# def crear_tarea(request):
#     # #Obtiene el nombre digitado por el usuario
#     # titulo = request.POST['nombre_tarea']
#     # proyecto_id = request.POST['']
#     # desarrolladores =  request.POST['']
#     # #Obtiene el id del proyecto de la tarea
#     # proyecto_id = Tarea.objects.get(pk=int(tarea_id)) ###Esta linea no estoy seguro
#     # #Crea la tarea
#     # t = Tarea()
#     # t.titulo = titulo
#     # t.activo = True
#     # t.proyecto_id = proyecto_id
#     # t.fecha_creacion = fecha_creacion
#     # t.desarrolladores = desarrolladores
#
#     # #Guarda la tarea
#     # t.save()
#     return HttpResponseRedirect(reverse('tareas'))
