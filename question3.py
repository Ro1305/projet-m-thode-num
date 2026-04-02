import numpy as np 
from SimRayon import trajetRayonEuler,profilTemperatureLin,trajetRayonIVP
from RechercheRacine import bissection

def nomcool(intervalle , z0 , xf , zf):
    # angle direct
    # atan2 arc tangent of x1/x2
    i02= np.atan2(zf-z0, xf)

    def ecart_altitude(i0, z0, zf):
        # _ pour ne pas prendre en compte x
        _, Y = trajetRayonIVP(intervalle, [z0, i0], 1e-7, profilTemperatureLin,sol=True)
        zf_fin = Y[0, -1]
        pomme=  zf_fin - zf
        return pomme

    def f_a_resoudre(angle):
        return ecart_altitude(angle, z0, zf)
    decalage= 1e-5
    seuil= np.pi/2 - decalage
    # on suppose que le phenomene a lieu en dessous de 1 degree
    x= - np.pi

    k= 1
    max =0
    intervalle_inf = [-seuil , i02 -decalage ]
    resultat = None
    # on test differentes valeurs de x jusqu a en avoir un qui est positif 
    # cf le graph
    while(k== 1 and max <100):
        x/=2
        resultat= bissection(f_a_resoudre,x,intervalle_inf[1],1e-7)
        k= resultat[1]
        max+=1
    
    print(resultat)
    
    if resultat[1] == 1:
        # todo reimplementer la meme approche ici pour une déflexion par le haut
        intervalle_supp= [i02-decalage,seuil]
        resultat= bissection(f_a_resoudre,intervalle_supp[0],intervalle_supp[1],1e-7)


    return [i02,resultat[0]]
def q32(intervalle , z0 , xf , zf):
    direct, indirect=nomcool(intervalle , z0 , xf , zf)
    x, Y2 = trajetRayonEuler(intervalle, [z0, indirect], 1e-3, profilTemperatureLin)
    ooo = Y2[1]-direct
    # todo plot les 2 euler au meme point
    # todo plot ooo (delta i) et abs
    # todo fixer les noms de variables dégeu
    print(ooo)
    from matplotlib import pyplot as plt
    plt.plot(ooo)
    plt.show()
    return np.max(np.asb(ooo))

    

intervalle = [0, 1000]
z0 = 1
xf = 1000
zf = 1.5

print(q32(intervalle, z0 , xf, zf))
"""

def ecart_altitude(i0, z0, zf):
    # _ pour ne pas prendre en compte x
    _, Y = trajetRayonIVP(intervalle, [z0, i0], 1e-7, profilTemperatureLin,sol=True)
    zf_fin = Y[0, -1]
    pomme=  zf_fin - zf
    return pomme
AAAAAAAAAA = np.linspace(-0.01,0.01,100)
BB = np.empty_like(AAAAAAAAAA)
for i in range(len(AAAAAAAAAA)):
    BB[i]=ecart_altitude(AAAAAAAAAA[i] , z0 ,zf )

from matplotlib import pyplot as plt
i02= np.atan2(zf-z0, xf)
decalage= 1e-5
plt.axhline(0)
plt.plot(AAAAAAAAAA,BB)
u = nomcool(intervalle, z0 , xf, zf)
plt.axvline(u[0])
plt.axvline(u[1])
plt.show()

i01 = resultat1[0]
statut1 = resultat1[1]
#########################

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
