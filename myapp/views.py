from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse
from . import forms
import sqlite3
import requests
from .models import Curso
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages


def index(request):
    f = open("index.html", "r", encoding="utf8")
    texto = f.read()
    f.close()
    return HttpResponse(texto)


def acerca_de(request):
    return HttpResponse("¡Curso de Python y Django!")


def cursos(request):
    conn = sqlite3.connect("cursos.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, inscriptos FROM curso")
    html = """
    <html>
    <title>Lista de cursos</title>
    <table style="border: 1px solid">
    <thead>
    <tr>
    <th>Curso</th>
    <th>Inscriptos</th>
    </tr>
    </thead>
    """
    for (nombre, inscriptos) in cursor.fetchall():  # [("JAVA",8),("PYTHON",10),("PHP",12)]
        html += f"""
        <tr>
        <td> { nombre } </td>
        <td> { inscriptos } </td>
        </tr>
        """
    html += "</table></html>"
    conn.close()
    return HttpResponse(html)


def dolar_visto(request):
    try:
        r = requests.get(
            "https://www.dolarsi.com/api/api.php?type=valoresprincipales")
        d = r.json()
        compra = d[0]["casa"]["compra"]
        venta = d[0]["casa"]["venta"]
    except:
        r = requests.get("http://www.bna.com.ar/Cotizador/MonedasHistorico")
        texto = r.text
        compra = texto[491:499]
        venta = texto[539:547]
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Precio dolar</title>
    </head>
    <body>
    <H1>Valor principal Dolar</H1>
    <h2> <strong>Dolar compra:</strong>{compra}</h2>
    <h2> <strong>Dolar venta:</strong>{venta}</h2>
    </body>
    </html>
    """
    return HttpResponse(html)


def servicio_dolar(request):
    r = requests.get(
        "https://www.dolarsi.com/api/api.php?type=valoresprincipales")
    d = r.json()
    compra = d[0]["casa"]["compra"]
    venta = d[0]["casa"]["venta"]
    return JsonResponse({"Compra": compra, "Venta": venta})


def aeropuertos(request):
    f = open("aeropuertos.csv", encoding="utf8")
    data = f.readlines()
    f.close()
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tp2</title>
    <body>
    <table>
    <tr>
    <td>Aeropuerto</td>
    <td>Ciudad</td>
    <td>Pais</td>
    </tr>
    """
    for renglon in data:
        # print(renglon)
        lista = renglon.split(",")
        # print(lista)
        a = lista[1].replace('"', '')
        c = lista[2].replace('"', '')
        p = lista[3].replace('"', '')
        html += f"""
        <tr>
        <td>{a}</td>
        <td>{c}</td>
        <td>{p}</td>
        </tr>
        """
    html += """
        </table>
        </body>
        </html>
    """
    return HttpResponse(html)


def servicio_aeropuertos(request):
    f = open("aeropuertos.csv", encoding="utf8")
    data = f.readlines()
    f.close()
    info = []
    for renglon in data:
        lista = renglon.split(",")
        a = lista[1].replace('"', '')
        c = lista[2].replace('"', '')
        p = lista[3].replace('"', '')
        d = {"nombre": a, "ciudad": c, "pais": p}
        info.append(d)
    return JsonResponse(info, safe=False)


def nuevo_index(request):
    return render(request, "myapp/index_render.html")


def pasando(request):
    # ctx = {"nombre": "Juan"}
    """
    ctx = {
        "nombre": "Juan",
        "cursos": 5,
        "curso_actual": "Python & Django"
    }
    """
    ctx = {
        "nombre": "Juan",
        "cursos": 5,
        "curso_actual": {"nombre": "Python & Django", "turno": "Noche"},
        "cursos_anteriores": ["Java", "PHP", "JavaScript", "Python"]
    }

    return render(request, "myapp/data.html", ctx)


def sentencias(request):
    ctx = {
        "nombre": "Juan",
        "cursos": 2,
        "alumnos": ["Juan", "Sofía", "Matias"]
    }
    return render(request, "myapp/sentencias.html", ctx)


def nueva_cursos(request):
    conn = sqlite3.connect("cursos.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, inscriptos FROM curso")
    cursos = cursor.fetchall()
    conn.close()
    ctx = {"cursos": cursos}
    return render(request, "myapp/cursos.html", ctx)


def capturar(request, nombre_curso):
    conn = sqlite3.connect("cursos.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, inscriptos FROM curso WHERE nombre=?",
                   [nombre_curso])
    curso = cursor.fetchone()  # [JAVA,5]
    ctx = {"curso": curso}
    conn.close()
    return render(request, "myapp/curso.html", ctx)


def nuevo_curso(request):
    if request.method == "POST":
        form = forms.FormularioCurso(request.POST)
        if form.is_valid():
            conn = sqlite3.connect("cursos.sqlite3")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO curso VALUES (?, ?)",
                           (form.cleaned_data["nombre"], form.cleaned_data["inscriptos"]))
            conn.commit()
            conn.close()
            return render(request, "myapp/mensaje.html")
    else:
        form = forms.FormularioCurso()
        ctx = {"form": form}
        return render(request, "myapp/nuevo_curso.html", ctx)


def cursos_orm(request):
    cursos = Curso.objects.all()
    print(cursos[0].get_turno_display())
    ctx = {"cursos": cursos}
    return render(request, "myapp/cursos_orm.html", ctx)


def cursos_json(request):
    response = JsonResponse(list(Curso.objects.values()), safe=False)
    return response


def nuevo_curso_mf(request):
    if request.method == "POST":
        form = forms.FormularioCursoDos(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("cursos-orm"))
    else:
        form = forms.FormularioCursoDos()
        ctx = {"form": form}
        return render(request, "myapp/nuevo_curso.html", ctx)


@login_required
def cursos_orm_log(request):
    cursos = Curso.objects.all()
    # print(cursos[0].get_turno_display())
    ctx = {"cursos": cursos}
    return render(request, "myapp/cursos_log.html", ctx)


def registrar(request):
    if request.method == "POST":
        formulario = forms.FormularioRegistro(request.POST)
        if formulario.is_valid():
            formulario.save()
            usuario = authenticate(
                username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user=usuario)
            messages.success(request, "Te has registrado correctamente!")
            return HttpResponseRedirect(reverse("nuevo"))
        else:
            messages.warning(
                request, 'Error.Respeta las indicaciones al crear un nuevo usuario')
    form = forms.FormularioRegistro()
    ctx = {"form": form}
    return render(request, "registration/registro.html", ctx)
