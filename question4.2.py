import matplotlib.pyplot as plt
import numpy as np
from SimRayon import trajetRayonEuler
from SimRayon import profilTemperatureLin2


def generer_image(intervalle, xf, z0, zf, image, hauteur_img, hauteur_voiture):
    h_img, w_img,_=image.shape
    ppm = h_img/hauteur_img
    angles = np.radians(np.linspace(0.1, -0.25, 1000))
    img_mirage = np.zeros((len(angles), w_img, 3), dtype=image.dtype)
    for idx, i in enumerate(angles):
        x, Y = trajetRayonEuler([0, xf], [zf, i], 1, profilTemperatureLin2, sol=True)
        if x[-1] == xf:
            z_final = Y[0, -1]
            if 0 <= z_final <= hauteur_voiture:
                pixel_y = int((hauteur_voiture - z_final) * ppm)
                img_mirage[idx, :]=image[pixel_y,:]
    somme_lignes = np.sum(img_mirage, axis=(1, 2))
    indices_valides = np.where(somme_lignes > 0)[0]
    
    if len(indices_valides) > 0:
        img_finale = img_mirage[indices_valides[0] : indices_valides[-1]+1, :, :]
    plt.imshow(img_finale)
    plt.show()
    
image = plt.imread("/Users/gerardrobin/Downloads/peugeot-208-route.png")

generer_image([0, 1000], 1000, 1, 1.5, image, 3.5, 2.8)
