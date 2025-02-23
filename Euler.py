# Aufgabe 3d
# python.exe -m pip install odf odfpy pandas matplotlib

from datetime import datetime
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Starte den Timer nach den Importen
sim_start = time.time()

# Initialisiere ein leeres DataFrame zum Speichern der Daten
data = pd.DataFrame(columns=['t', 'x mit Luftwiderstand', 'z mit Luftwiderstand',
                           'vel_x mit Luftwiderstand', 'vel_z mit Luftwiderstand',
                           'Resultierende Geschwindigkeit mit Luftwiderstand',
                           'x ohne Luftwiderstand', 'z ohne Luftwiderstand',
                           'vel_x ohne Luftwiderstand', 'vel_z ohne Luftwiderstand',
                           'Resultierende Geschwindigkeit ohne Luftwiderstand'])

# Auswahl der Darstellung: Koordinaten (1) oder Geschwindigkeit (0)
Koordinaten = 1

# Definition physikalischer Konstanten und Anfangsbedingungen
m = 2              # Masse (kg)
C = 0.45           # Spezieller Luftwiderstandskoeffizient ((0;2])
A = 0.1963         # Querschnittsfläche (m²) - Formel: 2*pi*r für r=2,5cm
vel_x = 15         # Anfangsgeschwindigkeit in X-Richtung (m/s)
vel_z = 0          # Anfangsgeschwindigkeit in Z-Richtung (m/s)
d_t = 0.00001       # Zeitschritt (s)
t_max = 2.5        # Maximale Simulationszeit (s)

# Definition der Schwerkraft und der Luftdichte
g = 9.81           # Erdbeschleunigung (m/s²)
ρ = 1.29           # Luftdichte (kg/m³)
x = 0              # Position in X-Richtung (m)
z = 0              # Position in Z-Richtung (m)
x_FF = 0           # Position in X-Richtung ohne Luftwiderstand (m)
z_FF = 0           # Position in Z-Richtung ohne Luftwiderstand (m)
F = g*m            # Gravitationskraft (N)
a_x = 0            # Beschleunigung in X-Richtung (m/s²)
a_z = 0            # Beschleunigung in Z-Richtung (m/s²)
F_Luft_x = 0       # Luftwiderstandskraft in X-Richtung (N)
F_Luft_z = 0       # Luftwiderstandskraft in Z-Richtung (N)
k = C*A*ρ/2        # Luftwiderstandskoeffizient ohne v²

# Initialisierung der Zeitvariablen
t = 0              # Aktuelle Zeit (s)

# Listen für die Datenspeicherung
t_list = [t]       # Zeitleiste
X_Punkte = [x]     # X-Koordinaten mit Luftwiderstand
Z_Punkte = [z]     # Z-Koordinaten mit Luftwiderstand
X_Punkte_FF = [x]  # X-Koordinaten ohne Luftwiderstand
Vel_X = [vel_x]    # X-Geschwindigkeit mit Luftwiderstand
Vel_Z = [vel_z]    # Z-Geschwindigkeit mit Luftwiderstand
Vel_X_FF = [vel_x] # X-Geschwindigkeit ohne Luftwiderstand
vel_z_FF = vel_z   # Momentane Z-Geschwindigkeit ohne Luftwiderstand
Vel_Z_FF = [vel_z] # Z-Geschwindigkeit ohne Luftwiderstand

# Resultierende Geschwindigkeiten
Vel_Res = [np.sqrt(vel_x**2+vel_z**2)]
Vel_Res_FF = [np.sqrt(vel_x**2+vel_z**2)]
vel_x_start = vel_x
vel_z_start = vel_z


# Berechnen der Trajektorie mit Luftwiderstand
while t <= 2.5:
    t += d_t        # Inkrementieren der Zeit

    # Berechnen der Bewegung in X-Richtung
    F_Luft_x = k * vel_x * abs(vel_x)
    a_x = - F_Luft_x / m
    vel_x = a_x * d_t + vel_x
    x = x + vel_x * d_t
    X_Punkte.append(x)
    Vel_X.append(vel_x)
    
    # Berechnen der Bewegung in Z-Richtung
    F_Luft_z = k * vel_z * abs(vel_z)
    a_z = (F - F_Luft_z) / m
    vel_z = a_z * d_t + vel_z
    z = z + vel_z * d_t
    Z_Punkte.append(z)
    Vel_Z.append(vel_z)
    
    Vel_Res.append(np.sqrt(vel_x**2+vel_z**2))
    
    t_list.append(t)

# Verschiebung nach oben, sodass es auf Z = 0 endet
height = max(Z_Punkte)
for i in range(len(Z_Punkte)):
    Z_Punkte[i] = (-Z_Punkte[i] + height)

# Initialisierung der Listen für die Berechnung des freien Falls

X_Punkte_FF = [0]
Z_Punkte_FF = [height]
Vel_Z_FF = [vel_z_FF]   # Startgeschwindigkeit vertikal ist Null #todo: 
t_FF = [0]              # Zeitleiste für freien Fall
x_FF = 0
z_FF = height

# Berechne der Trajektorie beim freien Fall
for t_current in t_list[1:]:   # Überspringe ersten Punkt, da bereits hinzugefügt
    x_FF += vel_x_start * d_t
    vel_z_FF = g * d_t + Vel_Z_FF[-1]
    z_FF = Z_Punkte_FF[-1] - vel_z_FF * d_t
    
    # Füge Punkte nur bis zum Aufprall hinzu
    if z_FF > 0:
        X_Punkte_FF.append(x_FF)
        Z_Punkte_FF.append(z_FF)
        Vel_X_FF.append(vel_x_start)
        Vel_Z_FF.append(vel_z_FF)
        t_FF.append(t_current)
        Vel_Res_FF.append(np.sqrt(vel_x_start**2+vel_z_FF**2))
        
    # Füge letzten Punkt beim Aufprall hinzu
    else:
        X_Punkte_FF.append(x_FF)
        Z_Punkte_FF.append(0)
        Vel_X_FF.append(vel_x_start)
        Vel_Z_FF.append(vel_z_FF)
        t_FF.append(t_current)
        Vel_Res_FF.append(np.sqrt(vel_x_start**2+vel_z_FF**2))
        break

# Füge Daten zum DataFrame hinzu
for i in range(len(t_list)):
    data_row = {
        't': t_list[i],
        'x mit Luftwiderstand': X_Punkte[i],
        'z mit Luftwiderstand': Z_Punkte[i],
        'vel_x mit Luftwiderstand': Vel_X[i],
        'vel_z mit Luftwiderstand': Vel_Z[i],
        'Resultierende Geschwindigkeit mit Luftwiderstand': Vel_Res[i],
        'x ohne Luftwiderstand': X_Punkte_FF[i] if i < len(X_Punkte_FF) else X_Punkte_FF[-1],
        'z ohne Luftwiderstand': Z_Punkte_FF[i] if i < len(Z_Punkte_FF) else 0,
        'vel_x ohne Luftwiderstand': Vel_X_FF[i] if i < len(Vel_X_FF) else Vel_X_FF[-1],
        'vel_z ohne Luftwiderstand': Vel_Z_FF[i] if i < len(Vel_Z_FF) else Vel_Z_FF[-1],
        'Resultierende Geschwindigkeit ohne Luftwiderstand': 
            Vel_Res_FF[i] if i < len(Vel_Res_FF) else Vel_Res_FF[-1]
    }
    data.loc[i] = data_row

# Exportieren des DataFrames in eine .ods-Datei
data.to_excel('Waagerechter_Wurf.ods', engine='odf', index=False)

# Stoppe den Timer nach den Simulationsberechnungen und vor dem Plotten
sim_end = time.time()
sim_duration = sim_end - sim_start
print("Simulationsdauer: {:.2f} s".format(sim_duration))

plt.title('Simulierter waagerechter Wurf mit Luftwiderstand')

if Koordinaten == 1:
    # Einrichten von Matplotlib für das Zeichnen der Trajektorie
    plt.xlabel('X-Richtung in Metern ->')
    plt.ylabel('Z-Richtung in Metern ->')

    # Anzeigen des Trajektorie-Plots
    plt.plot(X_Punkte, Z_Punkte, 'r-', label='Trajektorie des Körpers mit Luftwiderstand')
    plt.plot(X_Punkte_FF, Z_Punkte_FF, 'b:', label='Trajektorie des Körpers ohne Luftwiderstand')
    plt.legend()

    xmin, xmax, ymin, ymax = plt.axis()
    xmin, xmax, ymin, ymax = plt.axis([0, xmax, 0, ymax])

    plt.annotate('Abwurfhöhe: {:.2f}'.format(Z_Punkte[0]) + 'm', 
        horizontalalignment='center', verticalalignment='center', 
        xy=(0, Z_Punkte[0]), xytext=(xmax*0.1, ymax*0.7),
        bbox=dict(boxstyle="round", fc="0.8"), 
        arrowprops=dict(arrowstyle="->", facecolor='blue'), fontsize=18,)

    plt.annotate('Wurfweite: {:.2f}'.format(X_Punkte[len(X_Punkte)-1]) + 'm', 
        horizontalalignment='center', verticalalignment='center', 
        xy=(X_Punkte[len(X_Punkte)-1], 0), xytext=(0.7*xmax,0.2*ymax), 
        bbox=dict(boxstyle="round", fc="0.8"), 
        arrowprops=dict(arrowstyle="->", facecolor='red'), fontsize=18,)

    # Parameterangabe
    textstr_konst = '\n'.join((
        'Parameter:\n'
        r'Masse: %.2f' % (m, )+" kg",
        r'Querschnittsfläche: %.2f' % (A, )+" m²",
        r'Luftdichte: %.2f' % (ρ, )+" kg/m³",
        r'Spezieller Luftwiderstandskoeffizient: %.2f' % (C, ),
        r'Horizontale Startgeschwindigkeit: %.2f' % (vel_x_start, )+" m/s",
        r'Vertikale Startgeschwindigkeit: %.2f' % (vel_z_start, )+" m/s",
        r'Effektive Startgeschwindigkeit: %.2f' % (np.sqrt(vel_x_start**2+vel_z_start**2),)+" m/s",))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.75*xmax, 0.82*ymax, textstr_konst, fontsize=14, verticalalignment='baseline', bbox=props)

    # Variablenausgabe
    textstr_konst = '\n'.join((
        'Ergebnisse für den Fall mit Luftwiderstand:\n'
        r'Horizontale Endgeschwindigkeit: %.2f' % (vel_x, )+ " m/s",
        r'Vertikale Endgeschwindigkeit: %.3f' % (vel_z, )+" m/s",
        r'Effektive Endgeschwindigkeit: %.2f' % (np.sqrt(vel_x**2+vel_z**2),)+" m/s",
        r'Vertikale Durchschnittsgeschwindigkeit: %.2f' % (np.average(Vel_Z),)+" m/s",
        r'Durchschnittsgeschwindigkeit: %.2f' % (np.average(Vel_Res),)+" m/s",
        r'Falldauer: %.2f' % (t, )+" s",))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.75*xmax, 0.72*ymax, textstr_konst, fontsize=14, verticalalignment='center', bbox=props)

    # Abweichung der Fallweite Realität vs. Simulation
    Weite_errechnet_FF = vel_x_start * (np.sqrt(2*height/g))
    last_positive_index = next((i for i in range(len(Z_Punkte_FF)-1, -1, -1) if Z_Punkte_FF[i] > 0), 0)
    textstr_konst = '\n'.join((
        'Abweichungen:\n'
        r'Simulierte Fallweite (Euler): %.2f' % (X_Punkte_FF[last_positive_index], )+" m",
        r'Errechnete Fallweite (Formel): %.2f' % (Weite_errechnet_FF, )+" m",
        r'Effektive Abweichung in die horizontale Richtung: %.2f' % 
            (Weite_errechnet_FF-X_Punkte_FF[last_positive_index],),
        r'Relative Abweichung in die horizontale Richtung: %.2f' % 
            ((Weite_errechnet_FF-X_Punkte_FF[last_positive_index])/Weite_errechnet_FF*100, ) + " %",))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.003*xmax, 0.005*ymax, textstr_konst, fontsize=14, 
        horizontalalignment='left', verticalalignment='bottom', bbox=props)

else:
    # Einrichten von Matplotlib für das Zeichnen der Trajektorie (Zeit vs. Geschwindigkeit)
    plt.xlabel('Zeit in Sekunden ->')
    plt.ylabel('Geschwindigkeit in Metern pro Sekunde ->')

    # Anzeigen des Trajektorie-Plots
    plt.plot(t_list, Vel_X, 'r-', label='Horizontale Geschwindigkeit mit Luftwiderstand')
    plt.plot(t_list, Vel_Z, 'b-', label='Vertikale Geschwindigkeit mit Luftwiderstand')
    plt.plot(t_list, Vel_Res, 'g-', label='Effektive Geschwindigkeit mit Luftwiderstand')
    plt.plot(t_FF, Vel_X_FF, 'r:', label='Horizontale Geschwindigkeit ohne Luftwiderstand')
    plt.plot(t_FF, Vel_Z_FF, 'b:', label='Vertikale Geschwindigkeit ohne Luftwiderstand')
    plt.plot(t_FF, Vel_Res_FF, 'g:', label='Effektive Geschwindigkeit ohne Luftwiderstand') 

    xmin, xmax, ymin, ymax = plt.axis()
    xmin, xmax, ymin, ymax = plt.axis([0, xmax, 0, ymax])
    
    plt.plot([t_list[-1],t_list[-1]],[0, ymax], 'k-', 
        label='Aufprallzeitpunkt mit Luftwiderstand ' + "{:1.2f}".format(t_list[-1]) + 's')
    plt.plot([t_FF[-1],t_FF[-1]],[0, ymax], 'k:', 
        label='Aufprallzeitpunkt ohne Luftwiderstand ' + "{:1.2f}".format(t_FF[-1]) + 's')
    
    #get handles and labels
    handles, labels = plt.gca().get_legend_handles_labels()

    #specify order of items in legend
    order = [0,1,2,6,3,4,5,7]

    #add legend to plot
    plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order]) 

    # Parameterangabe
    textstr_konst = '\n'.join((
        'Parameter:\n'
        r'Masse: %.2f' % (m, )+" kg",
        r'Querschnittsfläche: %.2f' % (A, )+" m²",
        r'Luftdichte: %.2f' % (ρ, )+" kg/m³",
        r'Spezieller Luftwiderstandskoeffizient: %.2f' % (C, ),
        r'Horizontale Startgeschwindigkeit: %.2f' % (vel_x_start, )+" m/s",
        r'Vertikale Startgeschwindigkeit: %.2f' % (vel_z_start, )+" m/s",
        r'Effektive Startgeschwindigkeit: %.2f' % (np.sqrt(vel_x_start**2+vel_z_start**2),)+" m/s",))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    plt.text(0.75*xmax, 0.805*ymax, textstr_konst, fontsize=14, 
verticalalignment='baseline', bbox=props)

    # Variablenausgabe
    textstr_konst = '\n'.join((
        'Ergebnisse für den Fall mit Luftwiderstand:\n'
        r'Horizontale Endgeschwindigkeit: %.2f' % (vel_x, )+ " m/s",
        r'Vertikale Endgeschwindigkeit: %.3f' % (vel_z, )+" m/s",
        r'Effektive Endgeschwindigkeit: %.2f' % (np.sqrt(vel_x**2+vel_z**2),)+" m/s",
        r'Vertikale Durchschnittsgeschwindigkeit: %.2f' % (np.average(Vel_Z),)+" m/s",
        r'Durchschnittsgeschwindigkeit: %.2f' % (np.average(Vel_Res),)+" m/s",
        r'Fallweite: %.2f' % (x, )+" m",
        r'Falldauer: %.2f' % (t, )+" s",
        r'Fallhöhe: %.2f' % (z, )+" m",))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)    
    plt.text(0.75*xmax, 0.66*ymax, textstr_konst, fontsize=14, verticalalignment='center', bbox=props)

textstr_konst = '\n'.join((
'Iteratives Euler-Verfahren mit '+ "{:1.0f}".format(t/d_t)+ ' Iterationen in '+ 
    "{:1.3f}".format(sim_duration)+ 's von Julius Breitner (' + str(datetime.now().strftime("%d-%m-%Y"))+')',))
plt.text(0.5*xmax, -0.1*ymax, textstr_konst, fontsize=14, verticalalignment='center', bbox=props)

plt.grid(True)
plt.show()