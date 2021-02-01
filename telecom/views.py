from django.shortcuts import render
import math
import io
import numpy as np
import matplotlib.pyplot as plt
import urllib, base64

def home(request):
    uri = ""
    if request.POST:
	    codificacion = request.POST.get("codificacion", "")
	    binario = request.POST.get("binario", "")
    else:
    	codificacion = "ask"
    	binario = "10101010"
    plt.figure()
    if any(b not in "01" for b in binario):
        error = "Binario incorrecto"
        return render(request, "home.html", locals())
    if codificacion == "qam":
        qam = ""
        if len(binario) % 2 != 0:
            binario += "0"
    c = 0
    for b in binario:
        datos = np.arange(c-1,c+361)
        c+=360
        datos = np.radians(datos)
        if codificacion=="ask":
            if b=="1":
                funcion = 3*np.sin(datos)
            else:
                funcion = np.sin(datos)
        elif codificacion=="fsk":
            if b=="1":
                funcion = np.sin(3*datos)
            else:
                funcion = np.sin(datos)
            plt.axvline(np.radians(c), color='b', linestyle='--')
        elif codificacion=="psk":
            if b=="1":
                funcion = np.sin(datos)
            else:
                funcion = -np.sin(datos)
        elif codificacion=="qam":
            c -= 360
            qam += b
            if len(qam) == 2:
                datos = np.arange(c-1, c+91)
                datos = np.radians(datos)
                if qam == "00":
                    offset = c%360 
                elif qam == "01":
                    offset = c%360 - 90 
                elif qam == "10":
                    offset = c%360 - 180
                elif qam == "11":
                    offset = c%360 - 270
                
                funcion = np.sin(datos - np.radians(offset))
                plt.fill_between(datos,0,funcion, facecolor='lightcoral')
                qam = ""
                c+=90
            else:
                continue
        plt.plot(datos, funcion, "r")
    fig = plt.gcf()
    fig.subplots_adjust(bottom=0.1, top=1, left=0.1, right=1)
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request, "home.html", locals())