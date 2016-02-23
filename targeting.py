# targeting.py
#
# Module for target detection and Head's Up Display (HUD)

"""
U-SHAPE REFERENCE

 -  6-5 <- 2" wide   2-1
 |  | |              | |
 |  | |              | |
 |  | |              | |
14" | |              | |
 |  | |              | |
 |  | 4--------------3 |
 -  7------------------0 (start)
    |------- 18"-------|
"""

from __future__ import division  # always use floating point division
import cv2


