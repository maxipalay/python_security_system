# Tutorials followed:
#   comparing two images using MSE - https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/

import numpy as np

def compare_images(imageA, imageB):
    ''' Computes the mean squared error between two images and returns it. '''
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err
