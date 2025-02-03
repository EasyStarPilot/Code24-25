#Aufgabe 3d
#python.exe -m pip install odf odfpy pandas matplotlib

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


#Initialisieren eines leeren DataFrames zum Speichern der Daten
data = pd.DataFrame(columns=['t', 'x', 'y'])

#Definition physikalischer Konstanten und Anfangsbedingungen
m = 2               #Masse (kg)
C = 0.45            #Spezieller Luftwiderstandskoeffizient ((0;2])
A = 0.1963          #Querschnittsfläche (m²) Formel: 2*pi*r #A=0.1963 für r=2,5cm
vel_x = 5           #X-Anfangsgeschwindigkeit (m/sec)
vel_y = 0           #Y-Anfangsgeschwindigkeit (m/sec)
d_t = 0.01          #Zeitschritt (sec)
t_max = 2.5         #Maximale Zeit (sec)

#Definition der Schwerkraft und der Luftdichte
g = 9.81            #Schwerkraft (m/s²)
S = 1.29            #Luftdichte (kg/m³)

#Initialisierung von Variablen
x = 0               #Strecke in X-Richtung (m)
y = 0               #Strecke in Y-Richtung (m)
F = g*m             #Anziehungskraft der Erde
a_x = 0             #Beschleunigung in X-Richtung (m/s²)
a_y = 0             #Beschleunigung in Y-Richtung (m/s²)
F_Luft_x = 0        #Luftwiderstandskraft in X-Richtung
F_Luft_y = 0        #Luftwiderstandskraft in Y-Richtung
k = C*A*S/2         #Luftwiderstandskoeffizient ohne Velocity^2
t = 0               #Zeit (sec)
X_Punkte = []       #Liste für X-Koordinaten für Matplotlib
Y_Punkte = []       #Liste für Y-Koordinaten für Matplotlib
t_list = []         #Liste für die Zeit
vel_x_start = vel_x
vel_y_start = vel_y

#Berechnen der Trajektorie
while t < t_max:

    #Berechnen der Bewegung in X-Richtung
    F_Luft_x = k * vel_x**2     #Berechnung der Luftwiderstandskraft in X-Richtung
    a_x = (F - F_Luft_x) / m    #Berechnung der Beschleunigung in X-Richtung
    vel_x = a_x * d_t + vel_x   #Berechnung der Änderung der Geschwindigkeit in X-Richtung
    x = x + vel_x * d_t         #Berechnung der Strecke in X-Richtung
    X_Punkte.append(x)

    #Berechnen der Bewegung in Y-Richtung
    F_Luft_y = k * vel_y**2     #Berechnung der Luftwiderstandskraft in Y-Richtung
    a_y = (F - F_Luft_y) / m    #Berechnung der Beschleunigung in Y-Richtung
    vel_y = a_y * d_t + vel_y   #Berechnung der Änderung der Geschwindigkeit in Y-Richtung
    y = y + vel_y * d_t         #Berechnung der Strecke in Y-Richtung
    Y_Punkte.append(y)
    
    t_list.append(t)
    t += d_t                    #Inkrementieren der Zeit

#Verschiebung nach oben, sodass es auf Y = 0 endet
hight = max(Y_Punkte)
for i in range(len(Y_Punkte)):
    Y_Punkte[i] = (-Y_Punkte[i] + hight)
    
    #Ausgeben der aktuellen Zeit, Position und Geschwindigkeit
    print(f"Zeit:","{:10.4f}".format(t_list[i]), "  x:", "{:10.4f}".format(X_Punkte[i]), "    y:", "{:10.4f}".format(Y_Punkte[i]))

    #Hinzufügen der aktuellen Werte von t, x, y zum DataFrame
    data = data._append({'t': t_list[i], 'x': X_Punkte[i], 'y': Y_Punkte[i]}, ignore_index=True)

#Exportieren des DataFrames in eine .ods-Datei
data.to_excel('Waagerechter_Wurf.ods', engine='odf', index=False)

#Einrichten von Matplotlib für das Zeichnen der Trajektorie
plt.title('Waagerechter Wurf mit Luftwiderstand')
plt.xlabel('X-Richtung in Metern ->')
plt.ylabel('Y-Richtung in Metern ->')
plt.annotate('Abwurfhöhe:'+ "{:10.2f}".format(Y_Punkte[0]) + 'm', xy=(0, Y_Punkte[0]), xytext=(-1.45, Y_Punkte[0]-3), 
            bbox=dict(boxstyle="round", fc="0.8"), arrowprops=dict(arrowstyle="->", facecolor='blue'),)
plt.annotate('Wurfweite:'+ "{:10.2f}".format(X_Punkte[len(X_Punkte)-1]) + 'm' , xy=(X_Punkte[len(X_Punkte)-1], 0), xytext=(X_Punkte[len(X_Punkte)-1]-5, -0.15), 
            bbox=dict(boxstyle="round", fc="0.8"), arrowprops=dict(arrowstyle="->", facecolor='red'),)

#Legende
red_line = mlines.Line2D([], [], color='red', marker='_', markersize=15, label='Trajektorie des Körpers')
plt.legend('upper right',handles=[red_line])

#Konstantenangabe
textstr_konst = '\n'.join((
    'Konstanten:\n'
    r'Masse in kg=%.2f' % (m, ),
    r'Querschnittsfläche in m²=%.2f' % (A, ),
    r'Luftdichte in kg/m²=%.2f' % (S, ),
    r'Spezieller Luftwiderstandskoeffizient=%.2f' % (t, ),))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(26, 22, textstr_konst, fontsize=14, verticalalignment='baseline', bbox=props)

#Veränerungsausgabe
textstr_konst = '\n'.join((
    'Veränderungen:\n'
    r'Horizontale Startgeschwindigkeit=%.3f' % (vel_x_start, ),
    r'Vertikale Startgeschwindigkeit=%.2f' % (vel_y_start, ),
    r'Startgeschwindigkeit=%.2f' % (np.sqrt(vel_x_start**2+vel_y_start**2),),
    r'Horizontale Endgeschwindigkeit=%.2f' % (vel_x, ),
    r'Vertikale Endgeschwindigkeit=%.3f' % (vel_y, ),
    r'Endgeschwindigkeit=%.2f' % (np.sqrt(vel_x**2+vel_y**2),),
    r'Falldauer in Sekunden=%.2f' % (t, ),))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(26, 19, textstr_konst, fontsize=14, verticalalignment='center', bbox=props)

#Anzeigen des Trajektorie-Plots
plt.plot(X_Punkte, Y_Punkte, 'r-')
plt.grid(True)
plt.show()