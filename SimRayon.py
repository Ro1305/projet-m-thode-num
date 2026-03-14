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

def trajetRayonEuler(intervalle, y0, dx, profilTemperature):
    x0, xf = intervalle
    z0, i0 = y0
    
    x = [x0]
    Y = [np.array(y0)]
    
    while x[-1] < xf :
        dx2 = min(dx, xf-x[-1])
        pente = odefunction(x[-1], Y[-1], profilTemperature)
        xs = x[-1] + dx2
        ys = Y[-1] + dx2 * pente
        
        x.append(xs)
        Y.append(ys)
    return np.array(x), np.array(Y).T

def profilTemperatureLin(z):
    h = 0.5
    Th = 288.15
    Tsol = 303.15
    if z < h :
        T = ((Th-Tsol)/h)*z+Tsol
        dTdz = (Th-Tsol)/h
    else :
        T = Th
        dTdz = 0
    return T, dTdz

def trajetRayonIVP(intervalle, y0, rtol, profilTemperature):
    sol = integrate.solve_ivp(odefunction, intervalle, y0, rtol=rtol, args=(profilTemperature, ))
    return sol.t, sol.y



#x_ivp, Y_ivp = trajetRayonIVP([0, 1000], [1, np.radians(-0.5)], 10**-10, profilTemperatureLin)

"""for o in np.linspace(-1, 0.1, 20):
    x_eul, Y_eul = trajetRayonEuler([0, 1000], [1, np.radians(o)], 0.01, profilTemperatureLin)
    z_eul = Y_eul[0,:]
    ss = np.where(z_eul<=0)[0]
    if len(ss)>0:
        indice_sol = ss[0]
        x_positif = x_eul[:indice_sol + 1]
        z_positif = z_eul[:indice_sol + 1]
        plt.plot(x_positif, z_positif)
    else:
        plt.plot(x_eul, z_eul)

plt.show()"""
#z_ivp = Y_ivp[0, :]
"""zf_ivp = Y_ivp[0, -1]
zf_eul = Y_eul[0, -1]
erreur = abs(zf_ivp-zf_eul)
print(erreur)"""
#plt.plot(x_ivp, z_ivp)

intervalle = [0, 1000]
z0 = 1
xf = 1000
zf = 1.5
def ecart_altitude(i0_deg, xf, z0, zf):
    i0_rad = np.radians(i0_deg)
    x, Y = trajetRayonEuler(intervalle, [z0, i0_rad], 0.1, profilTemperatureLin)
    zf_fin = Y[0, -1]
    return zf_fin - zf

def f_a_resoudre(angle):
    return ecart_altitude(angle, xf, z0, zf)

resultat1 = bissection(f_a_resoudre, -0.5, 0.0, 10**-10)
resultat2 = bissection(f_a_resoudre, 0, 0.1, 10**-10)
i01 = resultat1[0]
statut1 = resultat1[1]
i02 = resultat2[0]
statut2 = resultat2[1]

x_eul, Y_eul = trajetRayonEuler([0, 1000], [z0, np.radians(i01)], 0.1, profilTemperatureLin)
z_eul = Y_eul[0,:]
print(i01,", statut:",statut1)
plt.plot(x_eul, z_eul)

    
x_eul, Y_eul = trajetRayonEuler([0, 1000], [z0, np.radians(i02)], 0.1, profilTemperatureLin)
z_eul = Y_eul[0,:]
plt.plot(x_eul, z_eul)
plt.plot(x_eul, z_eul)
print(i02,", statut",statut2)
plt.show()

    