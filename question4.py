import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from SimRayon import trajetRayonEuler
from SimRayon import profilTemperatureLin
from RechercheRacine import bissection

def generer_image():
    image_path = "/Users/gerardrobin/Downloads/peugeot-208-route.png" 
    img_source = mpimg.imread(image_path)
    if img_source.max() > 1: img_source = img_source / 255.0
    h_img, w_img, _ = img_source.shape
    h_sortie = 2 * h_img 
    z_max_obj = 1.5
    xf, z0 = 1000, 1
    ratio_origine = h_img / w_img
    angles = np.linspace(-0.4, 0.2, h_sortie) 
    img_mirage = np.zeros((h_sortie, w_img, 3))
    for i, angle_deg in enumerate(angles):
        x, Y = trajetRayonEuler([0, xf], [z0, np.radians(angle_deg)], 1, profilTemperatureLin)
        z_final = Y[0, -1]
        
        if 0 <= z_final <= z_max_obj:
            j = int((1 - (z_final / z_max_obj)) * (h_img - 1))
            j = np.clip(j, 0, h_img - 1)
            img_mirage[i, :, :] = img_source[j, :, :3]
    somme_lignes = np.sum(img_mirage, axis=(1, 2))
    indices_valides = np.where(somme_lignes > 0)[0]
    
    if len(indices_valides) > 0:
        img_finale = img_mirage[indices_valides[0] : indices_valides[-1]+1, :, :]
    else:
        img_finale = img_mirage
    
    aspect_correct = w_img / img_finale.shape[0] * ratio_origine
    plt.imshow(img_finale, origin='lower', aspect=aspect_correct)
    #plt.axis('off')
    plt.show()
    
generer_image()

"""
def tracerRayons(xf, zf, intervalle):
    for z0 in np.linspace(-6, 2, 100):
        def ecart_altitude(i0_deg, xf, z0, zf):
            i0_rad = np.radians(i0_deg)
            x, Y = trajetRayonEuler(intervalle, [z0, i0_rad], 1, profilTemperatureLin)
            zf_fin = Y[0, -1]
            return zf_fin - zf
        def f_a_resoudre(angle):
            return ecart_altitude(angle, xf, z0, zf)
        resultat1 = bissection(f_a_resoudre, -100.135, 2.0, 10**-4)
        #resultat2 = bissection(f_a_resoudre, 0.00, 2, 10**-4)
        i01 = resultat1[0]
        statut1 = resultat1[1]
        #i02 = resultat2[0]
        #statut2 = resultat2[1]

        x_eul, Y_eul = trajetRayonEuler([0, 1000], [z0, np.radians(i01)], 1, profilTemperatureLin)
        z_eul = Y_eul[0,:]
        
        if statut1 == 0 and np.all(z_eul >= -6):
            plt.plot(x_eul, z_eul, color='red')

    
       # x_eul, Y_eul = trajetRayonEuler([0, 1000], [z0, np.radians(i02)], 1, profilTemperatureLin)
       # z_eul = Y_eul[0,:]
       # if statut2 == 0 and np.all(z_eul >= -6):
           # plt.plot(x_eul, z_eul, color = 'red')
        
    plt.show()

tracerRayons(1000, 1.5, [0, 1000])"""
"""
def tracerRayons(xf, zf, intervalle):
    plt.figure(figsize=(10, 6))
    
    # On balaie de -6 à 2
    for z0 in np.linspace(-6, 2, 40): 
        
        def f_a_resoudre(angle):
            i0_rad = np.radians(angle)
            _, Y = trajetRayonEuler(intervalle, [z0, i0_rad], 1, profilTemperatureLin)
            return Y[0, -1] - zf

        recherche1 = bissection(f_a_resoudre, -2.0, 0.4, 10**-4)
        recherche2 = bissection(f_a_resoudre, -0.1, 5.0, 10**-4)

        for res in [recherche1, recherche2]:
            if res[1] == 0: # Si statut OK
                angle_trouve = res[0]
                x_e, Y_e = trajetRayonEuler(intervalle, [z0, np.radians(angle_trouve)], 1, profilTemperatureLin)
            if res[1] != 0 and res[1] != 0:
                print(f"Alerte : Aucune solution trouvée pour z0 = {z0}")
                # On trace tout ce qui est au-dessus de -6 (consigne)
                if np.all(Y_e[0,:] >= -6):
                    plt.plot(x_e, Y_e[0,:], color = 'red')

    plt.axhline(0, label="Sol (Physique)") 
    plt.title("Rayons lumineux de z0 = -6m à 2m")
    plt.legend()
    plt.show()
"""
def tracerRayons(xf, zf, intervalle):
    plt.figure(figsize=(10, 6))
    for z0 in np.linspace(0, 2, 30): 
        
        def f_a_resoudre(angle):
            i0_rad = np.radians(angle)
            _, Y = trajetRayonEuler(intervalle, [z0, i0_rad], 1, profilTemperatureLin)
            return Y[0, -1] - zf
        
        rayon_direct = bissection_interne(f_a_resoudre, -0.1, 0.5) 
        
        rayon_mirage = bissection_interne(f_a_resoudre, -1.0, -0.1)

        # On trace les résultats trouvés
        for rayon in [rayon_direct, rayon_mirage]:
            if rayon is not None:
                x_e, Y_e = trajetRayonEuler(intervalle, [z0, np.radians(rayon)], 1, profilTemperatureLin)
                if np.all(Y_e[0,:] >= -6):
                    plt.plot(x_e, Y_e[0,:], color='red')

    plt.axhline(0)
    plt.title("Simulation complète entre [-6, 2]")
    plt.show()

def bissection_interne(f, a, b):
        if f(a) * f(b) < 0:
            return bissection(f, a, b, 10**-4)[0]

tracerRayons(1000, 1.5, [0, 1000])