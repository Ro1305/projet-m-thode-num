import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from SimRayon import trajetRayonEuler
from SimRayon import profilTemperatureLin

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
    plt.axis('off')
    plt.show()
    
generer_image()