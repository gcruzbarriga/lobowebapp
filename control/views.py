from django.shortcuts import render, redirect
from django.db.models import Q

import control.models as modelos
import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from control.forms import PersonalForm, ControlHorasForm
from django.contrib import messages
import datetime

from django import forms

@login_required
def index(request):
    
    listPersonal = []
    
    # equipoTrabajo = modelos.Personal.objects.values('pk','nombre','apellido_pat','alias').order_by('nombre')
    equipoTrabajo = modelos.Personal.objects.values('pk','nombre','apellido_pat','alias').filter(activo = True).order_by('nombre')
    
    for eqTr in equipoTrabajo:
        horas = modelos.ControlHoras.objects.values('hora_entrada','hora_salida').filter(
            Q(fecha = str(datetime.datetime.today().date())) & Q(trabajador = eqTr['pk']))
        if not horas:
            eqTr['horaLlegada'] = None
            eqTr['horaSalida'] = None
        elif horas[0]['hora_salida'] is None:
            eqTr['horaLlegada'] = str(horas[0]['hora_entrada'].strftime('%H:%M'))
            hora = horas[0]['hora_entrada']
            h = hora.hour
            m = hora.minute
            dif_min = (datetime.datetime.now().hour*60 + datetime.datetime.now().minute) - ((h*60) + m)
            eqTr['difMin'] = dif_min
        else:
            eqTr['horaLlegada'] = str(horas[0]['hora_entrada'].strftime('%H:%M'))
            eqTr['horaSalida'] = str(horas[0]['hora_salida'].strftime('%H:%M'))
        listPersonal.append(eqTr)
    
    if request.method == 'POST':
        
        request.session['entrada'] = False
        request.session['salida'] = False
        
        es = modelos.ControlHoras.objects.values('pk','hora_entrada','hora_salida').filter(
            Q(fecha = str(datetime.datetime.today().date())) & Q(trabajador = request.POST.get("seleccion","")))
        if not es:
            request.session['entrada'] = True
        elif es[0]['hora_salida'] is None:
            request.session['salida'] = True
            request.session['regId'] = es[0]['pk']
        
        request.session['personaId'] = request.POST.get("seleccion","")
        return redirect('confirmacion')

    return render(request, "index.html", {
        'listPersonal':listPersonal,
    })

@login_required
def comida(request):
    
    listPersonal = []
    
    # equipoTrabajo = modelos.Personal.objects.values('pk','nombre','apellido_pat','alias').order_by('nombre')
    equipoTrabajo = modelos.Personal.objects.values('pk','nombre','apellido_pat','alias').filter(activo = True).order_by('nombre')
    
    for eqTr in equipoTrabajo:
        horas = modelos.ControlHoras.objects.values('hora_comidai','hora_comidaf').filter(
            Q(fecha = str(datetime.datetime.today().date())) & Q(trabajador = eqTr['pk']))
        if not horas or horas[0]['hora_comidai'] is None:
            eqTr['comidaIni'] = None
            eqTr['comidaFin'] = None
        elif horas[0]['hora_comidaf'] is None:
            eqTr['comidaIni'] = str(horas[0]['hora_comidai'].strftime('%H:%M'))
            hora = horas[0]['hora_comidai']
            h = hora.hour
            m = hora.minute
            dif_min = (datetime.datetime.now().hour*60 + datetime.datetime.now().minute) - ((h*60) + m)
            eqTr['difMin'] = dif_min
        else:
            eqTr['comidaIni'] = str(horas[0]['hora_comidai'].strftime('%H:%M'))
            eqTr['comidaFin'] = str(horas[0]['hora_comidaf'].strftime('%H:%M'))
        listPersonal.append(eqTr)
    
    if request.method == 'POST':
        
        request.session['noAsis'] = False
        request.session['ini'] = False
        request.session['fin'] = False
        request.session['bloqueo'] = False
        
        es = modelos.ControlHoras.objects.values('pk','hora_comidai','hora_comidaf','hora_salida').filter(
            Q(fecha = str(datetime.datetime.today().date())) & Q(trabajador = request.POST.get("seleccion","")))
        if not es:
            request.session['noAsis'] = True
        elif es[0]['hora_salida'] is not None:
            request.session['bloqueo'] = True
            request.session['regId'] = es[0]['pk']
        elif es[0]['hora_comidai'] is None:
            request.session['ini'] = True
            request.session['regId'] = es[0]['pk']
        elif es[0]['hora_comidaf'] is None:
            request.session['fin'] = True
            request.session['regId'] = es[0]['pk']
        
        request.session['personaId'] = request.POST.get("seleccion","")
        return redirect('confirmacionComida')

    return render(request, "horas/comida.html", {
        'listPersonal':listPersonal,
    })

@login_required
def confirmacion(request):
    if request.session['entrada']:
        accion = 'entrada'
    elif request.session['salida']:
        accion = 'salida'       
    persona = modelos.Personal.objects.get(pk=request.session['personaId'])
    
    if request.method == 'POST':
        if request.session['entrada']:
            form = ControlHorasForm(request.POST)
            if form.is_valid():
                if request.POST.get("nip","") == persona.nip:
                    registro = form.save(commit=False)
                    
                    fechahora = datetime.datetime.now()
                    fecha = fechahora.date()
                    hora_entrada = fechahora.strftime('%H:%M')
                    
                    registro.trabajador = persona
                    registro.fecha = fecha
                    registro.hora_entrada = hora_entrada
                    
                    registro.save()
                    return redirect('home')
                else:
                    messages.warning(request, 'NIP incorrecto')
            else:
                messages.warning(request, form.errors)
        elif request.session['salida']:
            if request.POST.get("nip","") == persona.nip:
                registro = modelos.ControlHoras.objects.get(id=request.session['regId'])
                fechahora = datetime.datetime.now()
                registro.hora_salida = fechahora.strftime('%H:%M')
                registro.save()
                return redirect('home')
            else:
                    messages.warning(request, 'NIP incorrecto')

    return render(request, "horas/confirmacion.html", {
        'persona': persona,
        'accion': accion,
        })

@login_required
def confirmacionComida(request):
    if request.session['bloqueo']:
        accion = 'bloqueo'
    elif request.session['noAsis']:
        accion = 'noAsis'
    elif request.session['ini']:
        accion = 'ini'
    elif request.session['fin']:
        accion = 'fin'
    persona = modelos.Personal.objects.get(pk=request.session['personaId'])
    
    if request.method == 'POST':
        if request.session['ini']:
            if request.POST.get("nip","") == persona.nip:
                registro = modelos.ControlHoras.objects.get(id=request.session['regId'])
                fechahora = datetime.datetime.now()
                registro.hora_comidai = fechahora.strftime('%H:%M')
                registro.save()
                return redirect('comida')
            else:
                messages.warning(request, 'NIP incorrecto')
        elif request.session['fin']:
            if request.POST.get("nip","") == persona.nip:
                registro = modelos.ControlHoras.objects.get(id=request.session['regId'])
                fechahora = datetime.datetime.now()
                registro.hora_comidaf = fechahora.strftime('%H:%M')
                registro.save()
                return redirect('comida')
            else:
                messages.warning(request, 'NIP incorrecto')

    return render(request, "horas/confirmacionComida.html", {
        'persona': persona,
        'accion': accion,
        })

@login_required
def reporte(request):
    
    if request.method == 'POST':
        
        if request.POST.get("fechahoraini","") == "" or request.POST.get("fechahorafin","") == "":
            messages.warning(request, "Selecciona las dos fechas")
            return redirect('reporte')
        
        fecha1 = datetime.datetime.strptime(request.POST.get("fechahoraini",""), '%d/%m/%Y')
        fechaIni = fecha1.date()
        fecha2 = datetime.datetime.strptime(request.POST.get("fechahorafin",""), '%d/%m/%Y')
        fechaFin = fecha2.date()
        
        if fechaIni > fechaFin:
            messages.warning(request, "La fecha de inicio debe ser menor a la fecha fin")
            return redirect('reporte')
        else:
            request.session['fechaIni'] = datetime.datetime.strftime(fechaIni, '%Y-%m-%d')
            request.session['fechaFin'] = datetime.datetime.strftime(fechaFin, '%Y-%m-%d')
            return redirect('export_users_csv')

    return render(request, "horas/reporte.html", {
    })

        
@login_required        
def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Reporte_Horas.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID','NOMBRE','APELLIDO','FECHA','HORA ENTRADA','HORA SALIDA','INICIO COMIDA','FIN COMIDA'])
    
    registros = modelos.ControlHoras.objects.values_list('pk','trabajador__nombre','trabajador__apellido_pat','fecha','hora_entrada','hora_salida','hora_comidai','hora_comidaf').filter(
            fecha__range = (request.session['fechaIni'],request.session['fechaFin']))
    
    for registro in registros:
        writer.writerow(registro)

    return response