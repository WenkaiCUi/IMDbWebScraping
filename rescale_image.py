# -*- coding: utf-8 -*-
"""

@author: Wenkai Cui
@email: wkcui@bu.edu
Created on Sun Nov  4 20:51:11 2018

"""
import numpy as np

def CreateMask(map_image):
    def _transform_format(val):
        if val == 0:
            return 255
        if val == 255:
            return 0
        else:
            return val
        
    transformed_map = np.ndarray((map_image.shape[0],map_image.shape[1]), np.int32)
    
    for i in range(len(map_image)):
        transformed_map[i] = list(map(_transform_format, map_image[i]))
    return transformed_map
