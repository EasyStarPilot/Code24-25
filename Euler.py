#Aufgabe 3b
#python.exe -m pip install odf odfpy pandas matplotlib

from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#Initialisieren eines leeren DataFrames zum Speichern der Daten
data = pd.DataFrame(columns=['t', 'x mit Luftwiderstand', 'y mit Luftwiderstand','vel_y mit Luftwiderstand', 'Resultierende Geschwindigkeit mit Luftwiderstand', 'x ohne Luftwiderstand', 'y ohne Luftwiderstand'])

#Definition physikalischer Konstanten und Anfangsbedingungen
m = 2               #Masse (kg)
C = 0.45            #Spezieller Luftwiderstandskoeffizient ((0;2])
A = 0.1963          #Querschnittsfläche (m²) Formel: 2*pi*r #A=0.1963 für r=2,5cm
vel_x = 20          #X-Anfangsgeschwindigkeit (m/sec)
vel_y = 0           #Y-Anfangsgeschwindigkeit (m/sec)
d_t = 0.01          #Zeitschritt (sec)
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
Y_Punkte_FF = [y]   #Liste für Y-Koordinaten für Matplotlib FF
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
    F_Luft_x = k * vel_x**2     #Berechnung der Luftwiderstandskraft in X-Richtung
    a_x = - F_Luft_x / m        #Berechnung der Beschleunigung in X-Richtung
    vel_x = a_x * d_t + vel_x   #Berechnung der Änderung der Geschwindigkeit in X-Richtung
    x = x + vel_x * d_t         #Berechnung der Strecke in X-Richtung
    X_Punkte.append(x)
    
    #Berechnen der Bewegung in Y-Richtung
    F_Luft_y = k * vel_y**2     #Berechnung der Luftwiderstandskraft in Y-Richtung
    a_y = (F - F_Luft_y) / m    #Berechnung der Beschleunigung in Y-Richtung
    vel_y = a_y * d_t + vel_y   #Berechnung der Änderung der Geschwindigkeit in Y-Richtung
    y = y + vel_y * d_t         #Berechnung der Strecke in Y-Richtung
    Y_Punkte.append(y)
    Vel_Y.append(vel_y)
    Vel_Res.append(np.sqrt(vel_x**2+vel_y**2))
    
    
#Berechnen der Trajektorie ohne Luftwiderstand
  
    x_FF= vel_x_start * d_t + x_FF      #Berechnung der Strecke in X-Richtung FF
    X_Punkte_FF.append(x_FF)

    vel_y_FF = g * d_t + Vel_Y_FF[-1]   #Berechnung der Beschleunigung in Y-Richtung
    y_FF = vel_y_FF * d_t + y_FF        #Berechnung der Strecke in Y-Richtung FF
    Y_Punkte_FF.append(y_FF)
    Vel_Y_FF.append(vel_y_FF)
    
    t_list.append(t)

#Verschiebung nach oben, sodass es auf Y = 0 endet
hight = max(Y_Punkte)
for i in range(len(Y_Punkte)):
    Y_Punkte[i] = (-Y_Punkte[i] + hight)

#Verschiebung nach oben, sodass es auf Y = 0 endet FF
hight_FF = max(Y_Punkte_FF)
for i in range(len(Y_Punkte_FF)):
    Y_Punkte_FF[i] = (-Y_Punkte_FF[i] + hight_FF)

   
    #Ausgeben der aktuellen Zeit, Position und Geschwindigkeit
    print(f"Zeit:","{:10.4f}".format(t_list[i]), "  x mit Luftwiderstand:", "{:10.4f}".format(X_Punkte[i]), "    y mit Luftwiderstand:", "{:10.4f}".format(Y_Punkte[i]),
          "    vel_y mit Luftwiderstand:","{:10.4f}".format(Vel_Y[i]), "    Resultierende Geschwindigkeit mit Luftwiderstand:""{:10.4f}".format(Vel_Res[i]),
          "    x ohne Luftwiderstand:", "{:10.4f}".format(X_Punkte_FF[i]), "    y ohne Luftwiderstand:", "{:10.4f}".format(Y_Punkte_FF[i])  )

    #Hinzufügen der aktuellen Werte von t, x, y zum DataFrame
    data = data._append({'t': t_list[i], 'x mit Luftwiderstand': X_Punkte[i], 'y mit Luftwiderstand': Y_Punkte[i],'vel_y mit Luftwiderstand': Vel_Y[i], 'Resultierende Geschwindigkeit mit Luftwiderstand': Vel_Res[i],
                         'x ohne Luftwiderstand': X_Punkte_FF[i], 'y ohne Luftwiderstand': Y_Punkte_FF[i]}, ignore_index=True)

#Exportieren des DataFrames in eine .ods-Datei
data.to_excel('Waagerechter_Wurf.ods', engine='odf', index=False)

#Koordinaten(#t/1) oder Geschwindigkeit(#f/0)
Koordinaten = 1

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
                bbox=dict(boxstyle="round", fc="0.8"), arrowprops=dict(arrowstyle="->", facecolor='blue'),fontsize=20,)
    plt.annotate('Wurfweite:'+ "{:10.2f}".format(X_Punkte[len(X_Punkte)-1]) + 'm' , horizontalalignment='center', verticalalignment='center', xy=(X_Punkte[len(X_Punkte)-1], 0), xytext=(0.7*xmax,0.2*ymax), 
                bbox=dict(boxstyle="round", fc="0.8"), arrowprops=dict(arrowstyle="->", facecolor='red'),fontsize=20,)

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
    plt.plot(t_list, Vel_Y_FF,'b:', label='Vertikale Geschwindigkeit ohne Luftwiderstand')
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
Weite_errechnet_FF = vel_x_start * t
Tiefe_errechnet_FF = 0.5 * g * t ** 2 + vel_y_start * t
textstr_konst = '\n'.join((
    'Fehler:\n'_FF
    r'Simulierte Weite: %.2f' % (X_Punkte_FF[-1], )+" m",
    r'Errechnete Weite: %.2f' % (Weite_errechnet_FF, )+" m",
    r'Effektive Fehlerquote in die horizontale Richtung: %.2f' % (Weite_errechnet_FF-X_Punkte_FF[-1],),
    r'Relative Fehlerquote in die horizontale Richtung: %.2f' % ((Weite_errechnet_FF-X_Punkte_FF[-1])/Weite_errechnet_FF, ) + " %",
    r'Simulierte Tiefe: %.2f' % (Y_Punkte_FF[0], )+" m",
    r'Errechnete Tiefe: %.2f' % (Tiefe_errechnet_FF, )+" m",
    r'Effektive Fehlerquote in die vertikale Richtung: %.2f' % (Y_Punkte_FF[0]-Tiefe_errechnet_FF,),
    r'Relative Fehlerquote in die vertikale Richtung: %.2f' % ((Y_Punkte_FF[0]-Tiefe_errechnet_FF)/Tiefe_errechnet_FF, ) + " %",))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.003*xmax, 0.005*ymax, textstr_konst, fontsize=14, horizontalalignment='left', verticalalignment='bottom', bbox=props)

textstr_konst = '\n'.join((
    'Iteratives Euler-Verfahren mit '+ "{:1.0f}".format(t/d_t)+ ' Iterationen von Julius Breitner (' + str(datetime.now().strftime("%d-%m-%Y"))+')',))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.7*xmax, -0.1*ymax, textstr_konst, fontsize=14, verticalalignment='center', bbox=props)

plt.grid(True)
plt.show()