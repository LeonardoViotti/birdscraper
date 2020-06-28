import numpy
import os
import matplotlib.pyplot as plt
from skimage import io

os.chdir("C:/Users/wb519128/Dropbox/Work/Pessoal/Pokedex/Sabia-cica")

# Import photo
photo = io.imread("Pokedeximg_64.jpg")

# descriptives
photo.shape
type(photo)

# Plot
plt.imshow(photo)
plt.show()

# Reverse the image
plt.imshow(photo[:,::-1])
plt.show()

# Crop
plt.imshow(photo[0:75,120:250])
plt.show()

# Take every other row and every other column
plt.imshow(photo[::2,::2])
plt.show()