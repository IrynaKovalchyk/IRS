import numpy as np
import cv2
from matplotlib import pyplot as plt
img = cv2.imread('coins.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


'''plt.subplot(2,3,1),plt.imshow(thresh,'gray')
plt.show()'''

# Noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

# Sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)

'''plt.subplot(2,3,1),plt.imshow(sure_bg,'gray')
plt.show()'''

# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)


#plt.subplot(2,3,1),plt.imshow(sure_fg,'gray')
#plt.show()

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

#plt.subplot(2,3,1),plt.imshow(unknown,'gray')
#plt.show()

# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)

'''plt.subplot(2,3,1),plt.imshow(markers,'gray')
plt.show()'''
# Add one to all labels so that sure background 
markers = markers+1
# Mark the region of unknown with zero
markers[unknown==255] = 0

'''plt.subplot(2,3,1),plt.imshow(markers,'gray')
plt.show()'''

markers = cv2.watershed(img,markers)
img[markers == -1] = [255,0,0]

'''plt.subplot(2,3,1),plt.imshow(markers,'gray')
plt.show()'''

plt.subplot(2,3,2),plt.imshow(img,'gray')
plt.show()

cv2.destroyAllWindows()
