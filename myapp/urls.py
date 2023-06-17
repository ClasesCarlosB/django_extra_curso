from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("acerca", views.acerca_de, name="acerca"),
    path("cursos", views.cursos, name="cursos"),
    path("servicio-dolar", views.servicio_dolar, name="dolar"),
    path("dolar-visto", views.dolar_visto, name="dolar_visto"),
    path("aeropuertos", views.aeropuertos, name="aeropuertos"),
    path("servicio-aeropuertos", views.servicio_aeropuertos,
         name="servicio_aeropuertos"),
    path("nuevo", views.nuevo_index,
         name="nuevo"),
    path("pasando", views.pasando,
         name="pasando"),
    path("sentencias", views.sentencias,
         name="sentencias"),
    path("nueva-cursos", views.nueva_cursos, name="nueva_cursos"),
    path("capturar/<str:nombre_curso>", views.capturar, name="capturar"),
    path("nuevo-curso", views.nuevo_curso, name="nuevo-curso"),
    path("cursos-orm", views.cursos_orm, name="cursos-orm"),
    path("cursos-json", views.cursos_json, name="cursos-json"),
    path("nuevo-curso-mf", views.nuevo_curso_mf, name="nuevo-curso-mf"),
    path("cursos-orm-log", views.cursos_orm_log, name="cursos-orm-log"),
]
