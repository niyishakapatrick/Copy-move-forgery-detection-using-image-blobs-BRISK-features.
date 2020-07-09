#!/usr/bin/env python
#To run the program: python3 cmfd_blob_brisk.py

from datetime import datetime
from skimage.feature import blob_dog
from math import sqrt
import cv2
import numpy as np
import scipy
from scipy import ndimage
from scipy.spatial import distance
import glob, os



# Initiate BRISK detector
brisk = cv2.BRISK_create(27)
# create BFMatcher object
matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)


def sobel_f(im1):
	image =im1.astype (int)
	# derivatives
	dx=ndimage.sobel(image, 1)
	dy=ndimage.sobel(image, 0)
	mag=np.hypot(dx, dy)
	# normalization
	mag*= 255.0 / np.max(mag)
	sobel_im1 = np.uint8(mag)
	return sobel_im1

#DoG
def dog_f(im1_gray):
	blobs_dog = blob_dog(im1_gray, max_sigma=40, threshold=.1)
	blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)
	return blobs_dog

#Blobs
def show_f(blobs_all):
	blob_area =[]
	blobs_list = [blobs_all]
	for blobs in blobs_list:
		for blob in blobs:
			y, x, r = blob
			area = [y,x,r]           
			if 2*r > 1:
				#print area
				blob_area.append(area)              
	return blob_area

if __name__=='__main__':
	i = 0
	images = [image for image in glob.glob('*.jpg')]
	for im in images:
		start_time = datetime.now()
		print(im)
		#print('time :',start_time)
		im1 = cv2.imread (im)
		sobel = sobel_f(im1)
		sobel_gray =cv2.cvtColor(sobel, cv2.COLOR_BGR2GRAY)
		im2_gray =cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
		blobs_all = dog_f(sobel_gray)
		output = show_f(blobs_all)
		clone1 = im1.copy()
		key,des = brisk.detectAndCompute(im2_gray, None)
		print(len(key),'...',len(des))
 
		ll =[]
		for b0 in range(0,len(output)):
			b0y,b0x,b0r = output[b0]
			cv2.circle(clone1, (int(b0x),int(b0y)), int(b0r), (0, 0, 200), 1)             
			l =[]
			kp_1 =[]
			ds_1 =[]
			l3 =[]
			index= 0
			for  k,d in zip(key,des):
				if (k.pt[0] - b0x)**2 + (k.pt[1] - b0y)**2 <= (b0r **2):
					l.append(index)
					#print('l :',len(l))
					kp_1.append(k)
					ds_1.append(d)
				index+=1
			if l:
				kp_2= np.delete(key,l,axis=0)
				ds_2 = np.delete(des,l,axis=0)
				#print('k :',len(kp),'...',len(ds))
				nn_matches = matcher.knnMatch(np.array(ds_1), ds_2, 2)
				#print(nn_matches)
				matched1 = []
				matched2 = []
				nn_match_ratio = 0.43 # Nearest neighbor matching ratio
				for m, n in nn_matches:
					if m.distance < nn_match_ratio * n.distance:
						matched1.append(kp_1[m.queryIdx])
						matched2.append(kp_2[m.trainIdx])
					if len(matched1)>=4 :
						for k1,k2 in zip(matched1,matched2):
								cv2.line(clone1,(int(k1.pt[0]),int(k1.pt[1])),(int(k2.pt[0]),int(k2.pt[1])),(50,200,50),2)
           
		#cv2.imshow('image',clone1)
		cv2.imwrite(str(i)+'.png',clone1)    
		end_time = datetime.now()
		print('Duration: {}'.format(end_time - start_time))
		i += 1
	cv2.waitKey(0)
	cv2.destroyAllWindows()





