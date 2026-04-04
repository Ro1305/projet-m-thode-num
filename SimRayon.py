import numpy as np 
from scipy import integrate
import matplotlib.pyplot as plt
from RechercheRacine import bissection

def odefunction(x, y, profilTemperature):
    Ts = 288.15
    ns = 1.000272983820855
    z = y[0]
    i = y[1]
    T, dTdz = profilTemperature(z)
    dy = np.zeros(2)
    dy[0] = np.tan(i)
    dy[1] = (-(ns-1)*(Ts/T**2)*dTdz)*(1/(1+(ns-1)*(Ts/T)))
    return dy

def trajetRayonEuler(intervalle, y0, dx, profilTemperature, sol = False):
    x0, xf = intervalle
    
    x = [x0]
    Y = [np.array(y0)]

    while x[-1] < xf :
        dx2 = min(dx, xf-x[-1])
        pente = odefunction(x[-1], Y[-1], profilTemperature)
        xs = x[-1] + dx2
        ys = Y[-1] + dx2 * pente
        if sol and ys[0] < 0:
            break
        x.append(xs)
        Y.append(ys)
    return np.array(x), np.array(Y).T

def profilTemperatureLin(z):
    h = 0.5
    Th = 15+273.15
    Tsol = 30+273.15
    if z < h :
        T = ((Th-Tsol)/h)*z+Tsol
        dTdz = (Th-Tsol)/h
    else :
        T = Th
        dTdz = 0
    return T, dTdz

def profilTemperatureLin2(z):
    h = 0.5
    Th = 25+273.15
    Tsol = 50+273.15
    if z < h :
        T = ((Th-Tsol)/h)*z+Tsol
        dTdz = (Th-Tsol)/h
    else :
        T = Th
        dTdz = 0
    return T, dTdz

def trajetRayonIVP(intervalle, y0, rtol, profilTemperature,sol=False):
    # crée un évenement pour solve_ivp qui va stop la simu si on est dans le sol
    def evenement(t,y,args):
        return y[0]
    # si on tombe au sol , on arrete le code
    evenement.terminal=True
    if sol == False:
        solu = integrate.solve_ivp(odefunction, intervalle, y0, rtol=rtol, args=(profilTemperature, ))
    else :
        solu = integrate.solve_ivp(odefunction, intervalle, y0, rtol=rtol,events=evenement, args=(profilTemperature, ))
    return solu.t, solu.y


if __name__ == '__main__': 
    #Trajet Rayons Lumineux
    for o in np.linspace(-1, 0.1, 70):
        x_eul, Y_eul = trajetRayonEuler([0, 1000], [1, np.radians(o)], 0.1, profilTemperatureLin, sol=True)
        z_eul = Y_eul[0,:]
        """ss = np.where(z_eul<=0)[0]
        if len(ss)>0:
            indice_sol = ss[0]
            x_positif = x_eul[:indice_sol + 1]
            z_positif = z_eul[:indice_sol + 1]
            plt.plot(x_positif, z_positif, color = 'blue')
        else:
            plt.plot(x_eul, z_eul, color = 'blue')"""
        plt.plot(x_eul, z_eul)
    plt.title("Trajet Rayons Lumineux")
    plt.xlabel("distance (m)")
    plt.ylabel("hauteur (m)")
    plt.savefig("cool.png")
    plt.show()
    
#analyse du pas
"""
import time
x_ivp, Y_ivp = trajetRayonIVP([0, 1000], [1, np.radians(-0.5)], 10**-10, profilTemperatureLin)
z_ivp = Y_ivp[0, :]
zf_ivp = Y_ivp[0, -1]
for dx in [100, 10, 1, 0.1, 0.01]:
    debut = time.time()
    x_eul, Y_eul = trajetRayonEuler([0, 1000], [1, np.radians(-0.5)], dx, profilTemperatureLin)
    fin = time.time()
    temps_ecoule = fin - debut
    print("Temps écoulé pour dx =",dx,":", temps_ecoule, " secondes")
    zf_eul = Y_eul[0, -1]
    erreur = abs(zf_ivp-zf_eul)
    print("Erreur relative a dx =", dx,":", erreur)
#plt.plot(x_ivp, z_ivp)
"""
#question 3.1
"""
intervalle = [0, 1000]
z0 = 1
xf = 1000
zf = 1.5

def ecart_altitude(i0_deg, xf, z0, zf):
    i0_rad = np.radians(i0_deg)
    x, Y = trajetRayonEuler(intervalle, [z0, i0_rad], 1, profilTemperatureLin)
    zf_fin = Y[0, -1]
    return zf_fin - zf

def f_a_resoudre(angle):
    return ecart_altitude(angle, xf, z0, zf)

resultat1 = bissection(f_a_resoudre, -0.135, 0.0, 10**-4)
resultat2 = bissection(f_a_resoudre, 0.02, 0.03, 10**-4)
i01 = resultat1[0]
statut1 = resultat1[1]
i02 = resultat2[0]
statut2 = resultat2[1]

x_eul, Y_eul = trajetRayonEuler([0, 1000], [z0, np.radians(i01)], 1, profilTemperatureLin)
z_eul = Y_eul[0,:]
print(i01,", statut:",statut1)
plt.plot(x_eul, z_eul, color='red')

    
x_eul, Y_eul = trajetRayonEuler([0, 1000], [z0, np.radians(i02)], 1, profilTemperatureLin)
z_eul = Y_eul[0,:]
plt.plot(x_eul, z_eul, color = 'red')
print(i02,", statut:",statut2)
plt.show()

distance_angulaire = abs(i01 - i02)
print("La distance angulaire entre les deux images vaut:", distance_angulaire)
"""