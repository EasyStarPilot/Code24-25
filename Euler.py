#Aufgabe 3b
#python.exe -m pip install odf odfpy pandas matplotlib

from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#Initialisieren eines leeren DataFrames zum Speichern der Daten
data = pd.DataFrame(columns=['t', 'x mit Luftwiderstand', 'y mit Luftwiderstand','vel_y mit Luftwiderstand', 'Resultierende Geschwindigkeit mit Luftwiderstand', 'x ohne Luftwiderstand', 'y ohne Luftwiderstand'])

#Koordinaten(#t/1) oder Geschwindigkeit(#f/0)
Koordinaten = 1

#Definition physikalischer Konstanten und Anfangsbedingungen
m = 2               #Masse (kg)
C = 0.45            #Spezieller Luftwiderstandskoeffizient ((0;2])
A = 0.1963          #Querschnittsfläche (m²) Formel: 2*pi*r #A=0.1963 für r=2,5cm
vel_x = 20          #X-Anfangsgeschwindigkeit (m/sec)
vel_y = 0           #Y-Anfangsgeschwindigkeit (m/sec)
d_t = 0.001           #Zeitschritt (sec)
t_max = 2.5         #Maximale Zeit (sec)

#Definition der Schwerkraft und der Luftdichte
g = 9.81            #Schwerkraft (m/s²)
S = 1.29            #Luftdichte (kg/m³)

#Initialisierung von Variablen
x = 0               #Strecke in X-Richtung (m)
y = 0               #Strecke in Y-Richtung (m)
x_FF = 0            #Strecke in X-Richtung (m) FF
y_FF = 0            #Strecke in Y-Richtung (m) FF
F = g*m             #Anziehungskraft der Erde
a_x = 0             #Beschleunigung in X-Richtung (m/s²)
a_y = 0             #Beschleunigung in Y-Richtung (m/s²)
F_Luft_x = 0        #Luftwiderstandskraft in X-Richtung
F_Luft_y = 0        #Luftwiderstandskraft in Y-Richtung
k = C*A*S/2         #Luftwiderstandskoeffizient ohne Velocity^2
t = 0               #Zeit (sec)
X_Punkte = [x]      #Liste für X-Koordinaten für Matplotlib
Y_Punkte = [y]      #Liste für Y-Koordinaten für Matplotlib
X_Punkte_FF = [x]   #Liste für X-Koordinaten für Matplotlib FF
t_list = [t]        #Liste für die Zeit
Vel_Y  = [vel_y]    #Liste für Y-Geschwindigkeit für Matplotlib
vel_y_FF = vel_y    #Y-Geschwindigkeit FF
Vel_Y_FF = [vel_y]  #Liste für Y-Geschwindigkeit für Matplotlib FF
Vel_Res = [np.sqrt(vel_x**2+vel_y**2)]
vel_x_start = vel_x
vel_y_start = vel_y


#Berechnen der Trajektorie
while x < 25:
    t += d_t                    #Inkrementieren der Zeit
#Berechnen der Trajektorie mit Luftwiderstand

    #Berechnen der Bewegung in X-Richtung
    F_Luft_x = k * vel_x * abs(vel_x)     # Sign correction for air resistance
    a_x = - F_Luft_x / m
    vel_x = a_x * d_t + vel_x
    x = x + vel_x * d_t
    X_Punkte.append(x)
    
    #Berechnen der Bewegung in Y-Richtung
    F_Luft_y = k * vel_y * abs(vel_y)     # Sign correction for air resistance
    a_y = (F - F_Luft_y) / m
    vel_y = a_y * d_t + vel_y
    y = y + vel_y * d_t
    Y_Punkte.append(y)
    Vel_Y.append(vel_y)
    Vel_Res.append(np.sqrt(vel_x**2+vel_y**2))
    
    
    
    t_list.append(t)

#Verschiebung nach oben, sodass es auf Y = 0 endet
hight = max(Y_Punkte)
for i in range(len(Y_Punkte)):
    Y_Punkte[i] = (-Y_Punkte[i] + hight)

# Initialize lists for free fall trajectory
Y_Punkte_FF = [hight]
X_Punkte_FF = [0]
Vel_Y_FF = [0]  # Start with zero vertical velocity
t_FF = [0]      # Add time list for free fall
x_FF = 0
y_FF = hight

# Calculate free fall trajectory points
for t_current in t_list[1:]:  # Skip first point since it's already added
    x_FF += vel_x_start * d_t
    vel_y_FF = g * d_t + Vel_Y_FF[-1]
    y_FF = Y_Punkte_FF[-1] - vel_y_FF * d_t
    
    # Only add points until ground impact
    if y_FF > 0:
        X_Punkte_FF.append(x_FF)
        Y_Punkte_FF.append(y_FF)
        Vel_Y_FF.append(vel_y_FF)
        t_FF.append(t_current)
    else:
        # Add final point at ground impact
        X_Punkte_FF.append(x_FF)
        Y_Punkte_FF.append(0)
        Vel_Y_FF.append(vel_y_FF)
        t_FF.append(t_current)
        break

# Add data to DataFrame
for i in range(len(t_list)):
    data_row = {
        't': t_list[i],
        'x mit Luftwiderstand': X_Punkte[i],
        'y mit Luftwiderstand': Y_Punkte[i],
        'vel_y mit Luftwiderstand': Vel_Y[i],
        'Resultierende Geschwindigkeit mit Luftwiderstand': Vel_Res[i],
        'x ohne Luftwiderstand': X_Punkte_FF[i] if i < len(X_Punkte_FF) else X_Punkte_FF[-1],
        'y ohne Luftwiderstand': Y_Punkte_FF[i] if i < len(Y_Punkte_FF) else 0
    }
    data.loc[i] = data_row

#Exportieren des DataFrames in eine .ods-Datei
data.to_excel('Waagerechter_Wurf.ods', engine='odf', index=False)

plt.title('Simulierter waagerechter Wurf mit Luftwiderstand')
if Koordinaten == 1:
    #Einrichten von Matplotlib für das Zeichnen der Trajektorie
    plt.xlabel('X-Richtung in Metern ->')
    plt.ylabel('Y-Richtung in Metern ->')

    #Anzeigen des Trajektorie-Plots
    plt.plot(X_Punkte, Y_Punkte, 'r-', label='Trajektorie des Körpers mit Luftwiderstand')
    plt.plot(X_Punkte_FF, Y_Punkte_FF, 'b:', label='Trajektorie des Körpers ohne Luftwiderstand')
    plt.legend()

    xmin, xmax, ymin, ymax = plt.axis()
    xmin, xmax, ymin, ymax = plt.axis([0, xmax, 0, ymax])

    plt.annotate('Abwurfhöhe:'+ "{:10.2f}".format(Y_Punkte[0]) + 'm', horizontalalignment='center', verticalalignment='center', xy=(0, Y_Punkte[0]), xytext=(xmax*0.1, ymax*0.7),
                bbox=dict(boxstyle="round", fc="0.8"), arrowprops=dict(arrowstyle="->", facecolor='blue'), fontsize=20,)
    plt.annotate('Wurfweite:'+ "{:10.2f}".format(X_Punkte[len(X_Punkte)-1]) + 'm' , horizontalalignment='center', verticalalignment='center', xy=(X_Punkte[len(X_Punkte)-1], 0), xytext=(0.7*xmax,0.2*ymax), 
                bbox=dict(boxstyle="round", fc="0.8"), arrowprops=dict(arrowstyle="->", facecolor='red'), fontsize=20,)

    #Parameterenangabe
    textstr_konst = '\n'.join((
        'Parameter:\n'
        r'Masse: %.2f' % (m, )+" kg",
        r'Querschnittsfläche: %.2f' % (A, )+" m²",
        r'Luftdichte: %.2f' % (S, )+" kg/m³",
        r'Spezieller Luftwiderstandskoeffizient: %.2f' % (C, ),))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.75*xmax, 0.84*ymax, textstr_konst, fontsize=14, verticalalignment='baseline', bbox=props)

    #Veränerungsausgabe
    textstr_konst = '\n'.join((
        'Variablen:\n'
        r'Horizontale Startgeschwindigkeit: %.2f' % (vel_x_start, )+" m/s",
        r'Vertikale Startgeschwindigkeit: %.2f' % (vel_y_start, )+" m/s",
        r'Effektive Startgeschwindigkeit: %.2f' % (np.sqrt(vel_x_start**2+vel_y_start**2),)+" m/s",
        r'Horizontale Endgeschwindigkeit: %.2f' % (vel_x, )+ " m/s",
        r'Vertikale Endgeschwindigkeit: %.3f' % (vel_y, )+" m/s",
        r'Effektive Endgeschwindigkeit: %.2f' % (np.sqrt(vel_x**2+vel_y**2),)+" m/s",
        r'Vertikale Durchschnittsgeschwindigkeit: %.2f' % (np.average(Vel_Y ),)+" m/s",
        r'Durchschnittsgeschwindigkeit: %.2f' % (np.average(Vel_Res ),)+" m/s",
        r'Falldauer: %.2f' % (t, )+" s",))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.75*xmax, 0.72*ymax, textstr_konst, fontsize=14, verticalalignment='center', bbox=props)

else:
    #Einrichten von Matplotlib für das Zeichnen der Trajektorie
    plt.title('Simulierter waagerechter Wurf mit Luftwiderstand')
    plt.xlabel('Zeit in Sekunden ->')
    plt.ylabel('Geschwindigkeit in Metern pro Sekunde ->')

    #Anzeigen des Trajektorie-Plots
    plt.plot(t_list, Vel_Y,'r-', label='Vertikale Geschwindigkeit mit Luftwiderstand')
    plt.plot(t_list, Vel_Res,'g-', label='Effektive Geschwindigkeit mit Luftwiderstand')
    # Only plot free fall velocity until impact
    plt.plot(t_FF, Vel_Y_FF, 'b:', label='Vertikale Geschwindigkeit ohne Luftwiderstand')
    plt.legend()

    xmin, xmax, ymin, ymax = plt.axis()
    xmin, xmax, ymin, ymax = plt.axis([0, xmax, 0, ymax])

    #Parameterenangabe
    textstr_konst = '\n'.join((
        'Parameter:\n'
        r'Masse: %.2f' % (m, )+" kg",
        r'Querschnittsfläche: %.2f' % (A, )+" m²",
        r'Luftdichte: %.2f' % (S, )+" kg/m³",
        r'Spezieller Luftwiderstandskoeffizient: %.2f' % (C, ),))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.75*xmax, 0.805*ymax, textstr_konst, fontsize=14, verticalalignment='baseline', bbox=props)

    #Veränerungsausgabe
    textstr_konst = '\n'.join((
        'Variablen:\n'
        r'Horizontale Startgeschwindigkeit: %.2f' % (vel_x_start, )+" m/s",
        r'Vertikale Startgeschwindigkeit: %.2f' % (vel_y_start, )+" m/s",
        r'Effektive Startgeschwindigkeit: %.2f' % (np.sqrt(vel_x_start**2+vel_y_start**2),)+" m/s",
        r'Horizontale Endgeschwindigkeit: %.2f' % (vel_x, )+ " m/s",
        r'Vertikale Endgeschwindigkeit: %.3f' % (vel_y, )+" m/s",
        r'Effektive Endgeschwindigkeit: %.2f' % (np.sqrt(vel_x**2+vel_y**2),)+" m/s",
        r'Vertikale Durchschnittsgeschwindigkeit: %.2f' % (np.average(Vel_Y ),)+" m/s",
        r'Durchschnittsgeschwindigkeit: %.2f' % (np.average(Vel_Res ),)+" m/s",
        r'Fallweite: %.2f' % (x, )+" m",
        r'Fallhöhe: %.2f' % (y, )+" m",
        r'Falldauer: %.2f' % (t, )+" s",))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)    
    plt.text(0.75*xmax, 0.66*ymax, textstr_konst, fontsize=14, verticalalignment='center', bbox=props)

#Fehler
Weite_errechnet_FF = vel_x_start * (np.sqrt(2*hight/g))
last_positive_index = next((i for i in range(len(Y_Punkte_FF)-1, -1, -1) if Y_Punkte_FF[i] > 0), 0)

textstr_konst = '\n'.join((
    'Abweichungen:\n'
    r'Simulierte Fallweite (Euler): %.2f' % (X_Punkte_FF[last_positive_index], )+" m",
    r'Errechnete Fallweite (Formel): %.2f' % (Weite_errechnet_FF, )+" m",
    r'Effektive Abweichung in die horizontale Richtung: %.2f' % (Weite_errechnet_FF-X_Punkte_FF[last_positive_index],),
    r'Relative Abweichung in die horizontale Richtung: %.2f' % ((Weite_errechnet_FF-X_Punkte_FF[last_positive_index])/Weite_errechnet_FF*100, ) + " %",))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.003*xmax, 0.005*ymax, textstr_konst, fontsize=14, horizontalalignment='left', verticalalignment='bottom', bbox=props)

textstr_konst = '\n'.join((
    'Iteratives Euler-Verfahren mit '+ "{:1.0f}".format(t/d_t)+ ' Iterationen von Julius Breitner (' + str(datetime.now().strftime("%d-%m-%Y"))+')',))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.7*xmax, -0.1*ymax, textstr_konst, fontsize=14, verticalalignment='center', bbox=props)

plt.grid(True)
plt.show()