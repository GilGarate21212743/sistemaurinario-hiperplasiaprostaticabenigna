"""
Proyecto: Sistema urinario masculino (Hiperplasia Prostática Benigna)

Departamento de Ingenierí­a Eléctrica y Electrónica, Ingenierí­a Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Delgado Soto José Sebastián, Escalante Esquivel Diana Ivana, Gil Garate Carlos Andrés
Número de control: C20212281, 21212151, 21212743
Correo institucional: l20212281@tectijuana.edu.mx, l21212151@tectijuana.edu.mx, l21212743@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Instalar librerías en consola
#!pip install control
#!pip install slycot

# Librerí­as para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0, t0, tF, dt, w, h = 0 , 0, 30, 1E-3, 6, 3
N = round((tF-t0)/dt)+1
t = np.linspace(t0,tF,N)
u = np.sin(m.pi/2*t) #Funcion sinusoidal, 1.5708 rad/s = 250 mHz
signal = ['Control', 'Caso']

# Componentes del circuito de control y función de transferencia
Ri = 10E3
Rd = 10E3
Li = 2E-3
Ld = 2E-3
Cv = 10E-6
Rp = 1E3
numControl = [(Cv*Ld*Rp)+(Cv*Li*Rp),Ld+Li+(Cv*Rd*Rp)+(Cv*Ri*Rp),Rd+Ri]
denControl = [Cv*Ld*Li, (Cv*Ld*Ri)+(Cv*Li*Rd)+(Cv*Ld*Rp)+(Cv*Li*Rp), Ld+Li+(Cv*Rd*Ri)+(Cv*Rd*Rp)+(Cv*Ri*Rp), Rd+Ri]
sysControl = ctrl.tf(numControl, denControl)
print(sysControl)

# Componentes del circuito del caso y función de transferencia
Ri = 50E3
Rd = 50E3
Li = 2E-3
Ld = 2E-3
Cv = 150E-6
Rp = 20E3
numCaso = [(Cv*Ld*Rp)+(Cv*Li*Rp),Ld+Li+(Cv*Rd*Rp)+(Cv*Ri*Rp),Rd+Ri]
denCaso = [Cv*Ld*Li, (Cv*Ld*Ri)+(Cv*Li*Rd)+(Cv*Ld*Rp)+(Cv*Li*Rp), Ld+Li+(Cv*Rd*Ri)+(Cv*Rd*Rp)+(Cv*Ri*Rp), Rd+Ri]
sysCaso = ctrl.tf(numCaso, denCaso)
print(sysCaso)

# Componentes del controlador
Rr = 51.851
Re = 2222.3
Cr = 1E-6
Ce = 0
numPID = [Rr*Cr, 1]
denPID = [Re*Cr, 0]
PID = ctrl.tf(numPID,denPID)
print(PID)

# Sistema de control en lazo cerrado
X = ctrl.series(PID, sysCaso)
sysPID = ctrl.feedback(X, 1, sign = -1)
print(sysPID)
sysTratamiento = ctrl.series(sysControl, sysPID)

def plotsignals(u, sysControl, sysCaso, sysTratamiento):    
    fig = plt.figure()
    #plt.rcParams['text.usetext'] = True
    
    ts, Ppx = ctrl.forced_response(sysControl, t, u, x0)
    plt.plot(t, Ppx, '-', color = [0.6350, 0.0780, 0.1840], label = '$Control$')
    
    ts, Ppy = ctrl.forced_response(sysCaso, t, u, x0)
    plt.plot(t, Ppy, '-', color = [0.4660, 0.6740, 0.1880], label = '$Caso$')
    
    ts, Ppz = ctrl.forced_response(sysTratamiento, t, u, x0)
    plt.plot(t,Ppz,':', linewidth = 3, color = [0.3010, 0.7450, 0.9330], label = '$Tratamiento$')
    
    plt.grid(False)
    
    plt.xlim(0, 30)
    plt.xticks(np.arange(0, 30.1, 5))
    plt.ylim(-1.1, 1.1)
    plt.yticks(np.arange(-1, 1.1, 0.25))

    plt.xlabel('$t$ $[s]$', fontsize = 11)
    plt.ylabel('$V_i(t)$ $[V]$', fontsize = 11)
    plt.legend(bbox_to_anchor = (0.5,-0.3), loc = 'center', ncol = 4, fontsize = 8, frameon = False)
    plt.show()
    fig.set_size_inches(w, h)
    fig.tight_layout()
    namepng = 'python_' + 'SistemaUrinario' + '.png'
    namepdf = 'python_' + 'SistemaUrinario' + '.pdf'
    fig.savefig(namepng, dpi = 600, bbox_inches = 'tight')
    fig.savefig(namepdf, bbox_inches = 'tight')
    
# Respuesta del sistema en lazo abierto y en lazo cerrado
plotsignals(u, sysControl, sysCaso, sysTratamiento)