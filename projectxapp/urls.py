# from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [


    url(r'^$', views.form_login, name='form_login'),
    url(r'^crear_cuenta/', views.crear_cuenta, name='crear_cuenta'),
    url(r'^forgot_password/', views.forgot_password, name='forgot_password'),
    url(r'^404/', views.e404, name='e404'),
    # url(r'^login/auth', views.auth_login, name='auth_login'),
    url(r'^logout/', views.auth_logout, name='auth_logout'),
    url(r'^inicio/', views.inicio, name='inicio'),
    url(r'^proyectos/', views.proyectos, name='proyectos'),
    url(r'^proyectodetalles/(?P<id>\d+)/$', views.proyectodetalles, name='proyectodetalles'),
    url(r'^tareadetalles/(?P<id>\d+)/$', views.tareadetalles, name='tareadetalles'),
    url(r'^proyectos/crear_proyecto', views.crear_proyecto, name='crear_proyecto'),
    url(r'^peliculas/crear/', views.form_proyectos, name='form_proyectos'),
    url(r'^tareas/', views.tareas, name='tareas'),
    url(r'^tareas/crear/(?P<id>\d+)/$', views.form_tareas, name='form_tareas'),

    url(r'^activar/(?P<tareaid>\d+)/(?P<devid>\d+)/$', views.activar, name='activar'),
    url(r'^desactivar/(?P<tareaid>\d+)/(?P<devid>\d+)/$', views.desactivar, name='desactivar'),
    url(r'^borrardev/(?P<tareaid>\d+)/(?P<devid>\d+)/$', views.borrardev, name='borrardev'),
    # url(r'^tareas/crear/', views.crear_tarea, name='crear_tarea'),


    # path('login/', views.form_login, name='form_login'),
    # path('crear_cuenta/', views.crear_cuenta, name='crear_cuenta'),
    # path('forgot_password/', views.forgot_password, name='forgot_password'),
    # path('404/', views.e404, name='e404'),
    # path('login/auth', views.auth_login, name='auth_login'),
    # path('logout/', views.auth_logout, name='auth_logout'),
    # path('inicio/', views.inicio, name='inicio'),
    # path('proyectos/', views.proyectos, name='proyectos'),
    # path('proyectos/crear_proyecto', views.crear_proyecto, name='crear_proyecto'),
    # path('peliculas/crear/', views.form_proyectos, name='form_proyectos'),
    # path('tareas/', views.tareas, name='tareas'),
    # path('tareas/crear_tarea/', views.crear_tarea, name='crear_tarea'),

]
