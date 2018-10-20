# -*- coding: utf-8 -*-

from typing import Tuple
import cv2


def delete(cnts, index):
    seen = set()
    for value in index:
        seen.add(value)
    ls = []
    for i in range(0, len(cnts)):
        if i not in seen:
            ls.append(cnts[i])
    return ls


def point_on_line(line, p):
    epsilon = 0.001
    if abs(line[1][0] - line[0][0]) < epsilon:
        if abs(p[0] - line[0][0]) < epsilon:
            return True
        else:
            return False
    else:
        a = (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])
        b = line[0][1] - a * line[0][0]
        if abs(p[1] - (a * p[0] + b)) < epsilon:
            return True
        return False


def contour_center(contour) -> Tuple[int, int]:
    match = cv2.moments(contour)
    if match['m00'] == 0:
        return -1, -1
    cx = int(match['m10'] / match['m00'])
    cy = int(match['m01'] / match['m00'])
    return cx, cy
