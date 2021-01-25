"""
This experiment currently tagged as FAILED.
	encoded image cannot be stored properly in Zenoh Storage
	For example: .tobytes() method from Numpy
"""
from zenoh_service.zenoh_native_put import ZenohNativePut
import sys
import numpy as np
import cv2
import logging

###

L = logging.getLogger(__name__)


###

path = "/demo/image/test1"

# define value for image
root_path = "/home/s010132/devel/eagleeye/data/out1.png"
value = cv2.imread(root_path)
value = value.tobytes()

pub = ZenohNativePut(
	_path=path, _session_type="PUT"
)
pub.init_connection()

# put data
pub.put(value)

# closing Zenoh subscription & session
pub.close_connection()
