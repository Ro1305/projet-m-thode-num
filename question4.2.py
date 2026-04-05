import matplotlib.pyplot as plt
import numpy as np
from SimRayon import trajetRayonEuler
from SimRayon import profilTemperatureLin2
from question3 import recherche_angles, recherche_angles2


def generer_image(intervalle, xf, z0, zf, image):
    
    z_percues = []
    h_img, w_img,_=image.shape
    ppm = h_img/z0
    i01, i02 = recherche_angles2([0, xf], z0, xf, zf)
    angles = np.linspace(i02, i01, 1000)
    img_mirage = np.zeros((len(angles), w_img, 3), dtype=image.dtype)
    for idx, i in enumerate(angles):
        x, Y = trajetRayonEuler([0, xf], [zf, i], 1, profilTemperatureLin2, sol=True)
        zp = zf + xf * np.tan(i)
        z_percues.append(zp)
        if x[-1] == xf:
            z_final = Y[0, -1]
            if 0 <= z_final <= z0:
                pixel_y = int((z0 - z_final) * ppm)
                img_mirage[idx, :]=image[pixel_y,:]
    somme_lignes = np.sum(img_mirage, axis=(1, 2))
    indices_valides = np.where(somme_lignes > 0)[0]
    
    img_finale = img_mirage[indices_valides[0] : indices_valides[-1]+1, :, :]
    z_percues_final = np.array(z_percues)[indices_valides[0]:indices_valides[-1]+1]

    
    plt.imshow(img_finale, aspect='auto', extent=[0, w_img/ppm, z_percues_final.min(), z_percues_final.max()])
    
    plt.axhline(0, color='white', linestyle='--', linewidth=1, label="Ligne du sol")
    plt.ylabel("Altitude perçue z_perçu (m)")
    plt.xlabel("Largeur (m)")
    plt.title("Image du point de vue de l'observateur")
    plt.legend()
    plt.show()
    
    
image = plt.imread("/Users/gerardrobin/Downloads/peugeot-208-route.png")

#generer_image([0, 1000], 1000, 1.5, 2.7, image)
def tracer_courbe_percue(xf, z0, zf):
    i01, i02 = recherche_angles2([0, xf], z0, xf, zf)
    angles = np.radians(np.linspace(i02, i01, 1000))
    #angles = np.radians(np.linspace(-2, 1, 1000))
    z_reelles = []
    z_percues = []

    for i0 in angles:
        
        x, Y = trajetRayonEuler([0, xf], [zf, i0], 1, profilTemperatureLin2, sol=True)
        
        if x[-1] == xf:
            z_fin = Y[0, -1]
            z_p = zf + xf * np.tan(i0)
            
            z_reelles.append(z_fin)
            z_percues.append(z_p)

    plt.plot(z_reelles, z_percues)
    plt.xlabel("Position réelle z (m)")
    plt.ylabel("Position perçue z perçu (m)")
    plt.title("Positions perçues vs réelles")
    plt.grid(True)
    plt.ylim([-6, 2]) 
    plt.show()

tracer_courbe_percue(1000, 1.5, 1)