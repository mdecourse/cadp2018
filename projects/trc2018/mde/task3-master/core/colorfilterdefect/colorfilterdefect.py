# -*- coding: utf-8 -*-

from typing import Tuple, List, Optional
import cv2 as cv
import numpy as np
import math
from collections import Counter
from core.colorfilterdefect import cvtool


def cp_list(mat, contours):
    cs = []
    for i in range(0, len(contours)):
        cs.append(ContourProperty(mat, contours[i]))
    return cs


def mark_contour(verticallist, horizontallist, src):
    height, width = src.shape

    for i in range(0, len(verticallist)):
        cv.line(src, (verticallist[i], 0), (verticallist[i], height - 1), 250, 2)
    #        print('ver',i)
    for i in range(0, len(horizontallist)):
        cv.line(src, (0, horizontallist[i]), (width - 1, horizontallist[i]), 250, 2)


def set_hv(verticallist, horizontallist, vspacelist, hspacelist, mat, contours, accu, plot):
    height, width = mat.shape
    cscopy = contours.copy()
    cs = np.vstack(cscopy).squeeze()
    xlist = [p[0] for p in cs]
    ylist = [p[1] for p in cs]
    xcounts = Counter(xlist)
    sortedx = sorted(xcounts.items(), key=lambda kv: kv[1], reverse=True)
    if accu:
        verticallist.extend(
            [key for key, value in sortedx if (value > height / 2 and width * 0.01 < key < width * 0.98)])
    else:
        verticallist = [key for key, value in sortedx if
                        (value > height / 2 and width * 0.01 < key < width * 0.98)]
    ycounts = Counter(ylist)
    sortedy = sorted(ycounts.items(), key=lambda kv: kv[1], reverse=True)
    if accu:
        horizontallist.extend(
            [key for key, value in sortedy if (value > width / 2 and height * 0.01 < key < height * 0.98)])
    else:
        horizontallist = [key for key, value in sortedy if
                          (value > width / 2 and height * 0.01 < key < height * 0.98)]
    verticallist.sort()
    horizontallist.sort()
    vspacelist.clear()
    for i in range(0, len(verticallist) - 1):
        vspacelist.append(verticallist[i + 1] - verticallist[i])
    hspacelist.clear()
    for i in range(0, len(horizontallist) - 1):
        hspacelist.append(horizontallist[i + 1] - horizontallist[i])
    if plot:
        for i in range(0, len(verticallist) - 1):
            cv.line(mat, verticallist[i], verticallist[i + 1], (255, 0, 0), 1)
        for i in range(0, len(horizontallist) - 1):
            cv.line(mat, horizontallist[i], horizontallist[i + 1], (255, 0, 0), 1)


def mask_hv(vspacelist, verticallist, hspacelist, horizontallist, src, small):
    for i in range(0, len(verticallist) - 1):
        if vspacelist[i] < 100:
            src[verticallist[i] - small:verticallist[i + 1] + small, :] = 0
    for i in range(0, len(horizontallist) - 1):
        if hspacelist[i] < 100:
            src[:, horizontallist[i] - small:horizontallist[i + 1] + small] = 0


def on_hv(verticallist, horizontallist, p, small):
    for i in range(0, len(verticallist)):
        if abs(p[0] - verticallist[i]) <= small:
            return True
    for i in range(0, len(horizontallist)):
        if abs(p[1] - horizontallist[i]) <= small:
            return True
    return False


def near_vertical_line(verticallist, d):
    small = 50
    for i in verticallist:
        if abs(d - i) <= small:
            return True
    return False


class ContourProperty:

    def __init__(self, mat, contour):
        self.contourde_hv: Optional[np.ndarray] = None
        self.mat = mat
        self.height, self.width = mat.shape
        self.contour = contour
        self.rectx, self.recty, self.rectw, self.recth = cv.boundingRect(self.contour)
        rotbox = cv.minAreaRect(contour)
        self.rotx, self.roty = rotbox[0]
        self.rotwidth, self.rotheight = rotbox[1]
        self.rotpts = cv.boxPoints(rotbox)
        self.angle = rotbox[2]
        if self.rotwidth < self.rotheight:
            self.angle = 90 + self.angle

        self.center = cvtool.contour_center(self.contour)
        self.area = cv.contourArea(self.contour)

    def de_hv(self, verticallist, horizontallist, small, ratio, left, right, top, bottom):
        contourde_hv = np.array(self.contour)
        insidecount = 0
        count = 0
        index = []
        for k in range(0, len(contourde_hv)):
            if ((left < contourde_hv[k][0][0] < (self.width - right - small)) and (
                    top < contourde_hv[k][0][1] < (self.height - bottom - small))):
                insidecount = insidecount + 1
            for v in verticallist:
                if abs(contourde_hv[k][0][0] - v) <= small:
                    index.append(k)
                    count = count + 1
                    break
            for h in horizontallist:
                if abs(contourde_hv[k][0][1] - h) <= small:
                    index.append(k)
                    count = count + 1
                    break
        seen = set()
        for value in index:
            seen.add(value)
        hv = []
        for i in range(0, len(contourde_hv)):
            if i not in seen:
                hv.append([contourde_hv[i][0][0], contourde_hv[i][0][1]])
        contourde_hv = np.array(hv, dtype=np.int32)
        if insidecount < len(self.contour) * 0.5:
            del contourde_hv
            return
        if 1.0 * count / len(self.contour) > ratio:
            del contourde_hv
            return
        if contourde_hv is not None and len(contourde_hv) > 0:
            self.contourde_hv = contourde_hv


enableprocess1 = True
enableprocess2 = True
enableprocess3 = True
enableprocess4 = True
enableprocess5 = True
enableprocess6 = True
show = False


def rotate(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
    return result


def process1(gray, left, right, top, bottom, verticallist, horizontallist, vspacelist, hspacelist):
    height, width = gray.shape
    bw = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 15, -2)
    vertical = np.array(bw)
    elementv = cv.getStructuringElement(cv.MORPH_RECT, (1, 20))
    vertical = cv.erode(vertical, elementv)
    vertical = cv.dilate(vertical, elementv)
    helement = cv.getStructuringElement(cv.MORPH_RECT, (60, 1))
    vertical = cv.dilate(vertical, helement)
    vertical = cv.erode(vertical, helement)
    velement = cv.getStructuringElement(cv.MORPH_RECT, (1, 20))
    vertical = cv.dilate(vertical, velement)
    vertical = cv.erode(vertical, velement)
    edges = cv.adaptiveThreshold(vertical, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, -2)
    im2, cnts, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    if cnts is None or len(cnts) == 0:
        return cnts
    cplist = cp_list(edges, cnts)
    set_hv(verticallist, horizontallist, vspacelist, hspacelist, edges, cnts, False, False)
    dehvlist = []
    for i in range(0, len(cnts)):
        c = cplist[i]

        if on_hv(verticallist, horizontallist, c.center, 10):
            continue
        if c.rectw > width / 8 or c.recth > height / 8:
            continue
        if c.area < 30:
            continue
        c.de_hv(verticallist, horizontallist, 1, 0.3, left, right, top, bottom)
        if c.contourde_hv is None or len(c.contourde_hv) == 0:
            continue
        else:
            dehvlist.append(c.contourde_hv)
    return dehvlist


def process2(gray, left, right, top, bottom, verticallist, horizontallist, vspacelist, hspacelist):
    height, width = gray.shape
    gray = cv.bitwise_not(gray)
    bw = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 15, -2)
    vertical = np.array(bw)
    elementv = cv.getStructuringElement(cv.MORPH_RECT, (1, 25))
    vertical = cv.erode(vertical, elementv)
    vertical = cv.dilate(vertical, elementv)
    helement = cv.getStructuringElement(cv.MORPH_RECT, (25, 1))
    vertical = cv.dilate(vertical, helement)
    vertical = cv.erode(vertical, helement)
    velement = cv.getStructuringElement(cv.MORPH_RECT, (1, 25))
    vertical = cv.dilate(vertical, velement)
    vertical = cv.erode(vertical, velement)
    edges = cv.adaptiveThreshold(vertical, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, -2)
    im2, cnts, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    if cnts is None or len(cnts) == 0:
        return cnts
    cplist = cp_list(edges, cnts)
    set_hv(verticallist, horizontallist, vspacelist, hspacelist, edges, cnts, True, False)
    mark_contour(verticallist, horizontallist, edges)
    dehvlist = []
    for i in range(0, len(cnts)):
        c = cplist[i]
        if on_hv(verticallist, horizontallist, c.center, 10):
            continue
        if c.rectw > width / 8 or c.recth > height / 8:
            continue
        if c.rectw / c.recth > 5 or c.recth / c.rectw > 5:
            continue
        if abs(c.angle) <= 0.01 or (89.8 <= abs(c.angle) <= 90.2):
            continue
        c.de_hv(verticallist, horizontallist, 1, 0.3, left, right, top, bottom)
        if c.contourde_hv is None or len(c.contourde_hv) == 0:
            continue
        else:
            dehvlist.append(c.contourde_hv)
    return dehvlist


def process3(gray):
    height, width = gray.shape
    ret, bw = cv.threshold(gray, 40, 255, cv.THRESH_BINARY_INV)

    edges = cv.adaptiveThreshold(bw, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, -2)
    im2, cnts, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    if cnts is None or len(cnts) == 0:
        return cnts
    cplist = cp_list(edges, cnts)
    index = []
    for i in range(0, len(cnts)):
        c = cplist[i]
        if c.rectw > width / 8 or c.recth > height / 8:
            index.append(i)
            continue
        if c.rectw / c.recth > 5 or c.recth / c.rectw > 5:
            index.append(i)
            continue
        if (
            abs(c.angle) <= 0.01 or
            (89.8 <= abs(c.angle) <= 90.2) and
            (c.rectw / c.recth > 2 or c.recth / c.rectw > 2)
        ):
            index.append(i)
            continue
    cnts = cvtool.delete(cnts, index)
    return cnts


def process4(gray, left, right, top, bottom, verticallist, horizontallist, vspacelist, hspacelist):
    height, width = gray.shape
    bw = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 15, -2)
    vertical = np.array(bw)
    elementv = cv.getStructuringElement(cv.MORPH_RECT, (1, 15))
    vertical = cv.erode(vertical, elementv)
    vertical = cv.dilate(vertical, elementv)
    edges = cv.adaptiveThreshold(vertical, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, -2)
    im2, cnts, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    if cnts is None or len(cnts) == 0:
        return cnts
    cplist = cp_list(edges, cnts)
    set_hv(verticallist, horizontallist, vspacelist, hspacelist, edges, cnts, True, False)
    dehvlist = []
    for i in range(0, len(cnts)):
        c = cplist[i]
        if on_hv(verticallist, horizontallist, c.center, 10):
            continue
        if c.rectw > width / 8 or c.recth > height / 8:
            continue
        if c.area < 30:
            continue
        c.de_hv(verticallist, horizontallist, 5, 0.3, left, right, top, bottom)
        if c.contourde_hv is None or len(c.contourde_hv) == 0:
            continue
        else:
            dehvlist.append(c.contourde_hv)
    return dehvlist


def distance(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx * dx + dy * dy)


def merge_contours(contours):
    cdel = []
    for i in range(0, len(contours)):
        cdel.append(False)
    for i in range(0, len(contours)):
        c1 = contours[i]
        p1 = cvtool.contour_center(c1)
        for j in range(i + 1, len(contours)):
            c2 = contours[j]
            p2 = cvtool.contour_center(c2)
            if distance(p1, p2) < 10:
                if cv.contourArea(c1) > cv.contourArea(c2):
                    cdel[j] = True
                else:
                    cdel[i] = True
    cnts = []
    for i in range(0, len(contours)):
        if not cdel[i]:
            cnts.append(contours[i])
    return cnts


def all_lines(cnts):
    lines = []
    for i in range(0, len(cnts)):
        p1 = cvtool.contour_center(cnts[i])
        for j in range(i + 1, len(cnts)):
            p2 = cvtool.contour_center(cnts[j])
            line = [p1, p2]
            lines.append(line)
    return lines


def point_in_line(p, line):
    for i in range(0, len(line)):
        if p[0] == line[i][0] and p[1] == line[i][1]:
            return True
    return False


def populate_lines(lines, cnts):
    for line in lines:
        for c in cnts:
            p = cvtool.contour_center(c)
            if p[0] == line[0][0] and p[1] == line[0][1]:
                continue
            if p[0] == line[1][0] and p[1] == line[1][1]:
                continue
            if cvtool.point_on_line(line, p):
                line.append(p)
                continue
    return lines


def merge2lines(line1, line2):
    if len(line1) > len(line2):
        notin = False
        for p in line2:
            if not point_in_line(p, line1):
                notin = True
                break
        if notin:
            return -1
        else:
            return 1
    else:
        notin = False
        for p in line1:
            if not point_in_line(p, line2):
                notin = True
                break
        if notin:
            return -1
        else:
            return 0


def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def merge_lines(lines):
    index = []
    for i in range(0, len(lines)):
        for j in range(i + 1, len(lines)):
            n = merge2lines(lines[i], lines[j])
            if n == 0:
                index.append(i)
            if n == 1:
                index.append(j)
    index = remove_duplicates(index)
    index.sort()
    ls = cvtool.delete(lines, index)
    return ls


def process5(gray, verticallist, horizontallist, vspacelist, hspacelist):
    gray = cv.bitwise_not(gray)
    bw = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 15, -2)
    vertical = np.array(bw)
    elementv = cv.getStructuringElement(cv.MORPH_RECT, (1, 20))
    vertical = cv.erode(vertical, elementv)
    vertical = cv.dilate(vertical, elementv)

    edges = cv.adaptiveThreshold(vertical, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, -2)
    im2, cnts, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    if cnts is None or len(cnts) == 0:
        return cnts
    set_hv(verticallist, horizontallist, vspacelist, hspacelist, edges, cnts, True, False)
    mark_contour(verticallist, horizontallist, edges)

    bw = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 15, -2)
    helement = cv.getStructuringElement(cv.MORPH_RECT, (20, 1))
    bw = cv.erode(bw, helement)
    velement = cv.getStructuringElement(cv.MORPH_RECT, (1, 20))
    bw = cv.dilate(bw, velement)
    bw = cv.bitwise_not(bw)

    mask_hv(vspacelist, verticallist, hspacelist, horizontallist, bw, 20)
    edges = cv.adaptiveThreshold(bw, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, -2)
    im2, cnts, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    if cnts is None or len(cnts) == 0:
        return cnts
    cnts = merge_contours(cnts)

    clist = [cvtool.contour_center(c) for c in cnts]
    index = []
    array = range(0, len(clist))
    for i in reversed(array):
        c = cnts[i]
        rx, ry, rw, rh = cv.boundingRect(c)
        if near_vertical_line(verticallist, rx) or near_vertical_line(verticallist, rx + rw):
            index.append(i)
            continue
        if rw * rh < 30:
            index.append(i)
            continue
    for i in range(0, len(cnts)):
        for j in range(i + 1, len(cnts)):
            if abs(clist[i][1] - clist[j][1]) <= 0:
                index.append(i)
                index.append(j)
    cnts = cvtool.delete(cnts, index)
    lines = all_lines(cnts)
    lines = populate_lines(lines, cnts)
    lines = merge_lines(lines)
    index = []
    for i in range(0, len(cnts)):
        p = cvtool.contour_center(cnts[i])
        inline = False
        for line in lines:
            for k in range(0, len(line)):
                if line[k][0] == p[0] and line[k][1] == p[1]:
                    inline = True
                    break
            if inline:
                break
        if not inline:
            index.append(i)
    cnts = cvtool.delete(cnts, index)
    return cnts


def process6(gray, verticallist, horizontallist, vspacelist, hspacelist):
    height, width = gray.shape
    kernel = np.array([-1, 1, 0])
    kernel.shape = (1, 3)
    gray = cv.filter2D(gray, -1, kernel)
    ret, bw = cv.threshold(gray, 30, 255, cv.THRESH_BINARY)
    edges = cv.adaptiveThreshold(bw, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, -2)
    im2, cnts, hierarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    if cnts is None or len(cnts) == 0:
        return cnts
    set_hv(verticallist, horizontallist, vspacelist, hspacelist, edges, cnts, True, False)
    mark_contour(verticallist, horizontallist, edges)
    index = []
    for i in range(0, len(cnts)):
        c = cnts[i]
        rx, ry, rw, rh = cv.boundingRect(c)
        if rw > width / 8 or rh > height / 8:
            index.append(i)
            continue
        if rw / rh > 5 or rh / rw > 5:
            index.append(i)
            continue
        rotbox = cv.minAreaRect(c)
        rotwidth, rotheight = rotbox[1]
        if rotwidth * rotheight / (rw * rh) > 0.9:
            index.append(i)
            continue
        p = cvtool.contour_center(c)
        if on_hv(verticallist, horizontallist, p, 10):
            index.append(i)
            continue
    cnts = cvtool.delete(cnts, index)
    cnts = merge_contours(cnts)
    return cnts


def line_angle(mat):
    gray = cv.cvtColor(mat, cv.COLOR_BGR2GRAY)
    canny = cv.Canny(gray, 255, 100)
    lines = cv.HoughLinesP(canny, 1, np.pi / 180, 220, 220, 220, 20)
    if lines is None or len(lines) == 0:
        return 0
    angs = []
    for line in lines[0]:
        ang = math.atan2(line[3] - line[1], line[2] - line[0]) * 180 / np.pi
        angs.append(ang)
    counts = Counter(angs)
    asorted = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
    return asorted[0][0]


def process(img):
    verticallist = []
    horizontallist = []
    vspacelist = []
    hspacelist = []

    height, width, channels = img.shape
    mat = np.array(img)
    percent = 0.05
    left = int(width * percent)
    right = int(width * percent)
    top = int(height * percent)
    bottom = int(height * percent)
    reflect = cv.copyMakeBorder(mat, top, bottom, left, right, cv.BORDER_REFLECT)
    angle = line_angle(reflect)
    rotated = rotate(reflect, angle)
    gray = cv.cvtColor(rotated, cv.COLOR_BGR2GRAY)

    cmap = np.zeros(gray.shape, dtype=gray.dtype)
    if enableprocess1:
        contours1 = process1(
            np.array(gray),
            left,
            right,
            top,
            bottom,
            verticallist,
            horizontallist,
            vspacelist,
            hspacelist
        )
        if (not (contours1 is None)) and len(contours1) > 0:
            cv.drawContours(cmap, contours1, -1, 255)

    if enableprocess2:
        contours2 = process2(
            np.array(gray),
            left,
            right,
            top,
            bottom,
            verticallist,
            horizontallist,
            vspacelist,
            hspacelist
        )
        if (not (contours2 is None)) and len(contours2) > 0:
            cv.drawContours(cmap, contours2, -1, 255)

    if enableprocess3:
        contours3 = process3(np.array(gray))
        if (not (contours3 is None)) and len(contours3) > 0:
            cv.drawContours(cmap, contours3, -1, 255)

    if enableprocess4:
        contours4 = process4(
            np.array(gray),
            left,
            right,
            top,
            bottom,
            verticallist,
            horizontallist,
            vspacelist,
            hspacelist
        )
        if (not (contours4 is None)) and len(contours4) > 0:
            cv.drawContours(cmap, contours4, -1, 255)

    if enableprocess5:
        contours5 = process5(
            np.array(gray),
            verticallist,
            horizontallist,
            vspacelist,
            hspacelist
        )
        if (not (contours5 is None)) and len(contours5) > 0:
            cv.drawContours(cmap, contours5, -1, 255)

    if enableprocess6:
        contours6 = process6(
            np.array(gray),
            verticallist,
            horizontallist,
            vspacelist,
            hspacelist
        )
        if (not (contours6 is None)) and len(contours6) > 0:
            cv.drawContours(cmap, contours6, -1, 255)

    cmap = rotate(cmap, -angle)
    cmap = cmap[top:height + top, left:width + left]
    orgcmap = np.array(cmap)
    edges = cv.adaptiveThreshold(orgcmap, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 3, -2)
    im2, cnts, hierarchy = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    index = []
    for i in range(0, len(cnts)):
        p = cvtool.contour_center(cnts[i])
        if p[0] < 0 or p[0] >= width or p[1] < 0 or p[1] >= height:
            index.append(i)
    cnts = cvtool.delete(cnts, index)
    cv.drawContours(img, cnts, -1, (0, 255, 0))
    for c in cnts:
        cv.circle(img, cvtool.contour_center(c), 6, (0, 0, 255), 3)
        rx, ry, rw, rh = cv.boundingRect(c)
        cv.line(img, (rx, ry), (rx + rw - 1, ry), (255, 0, 0), 3)
        cv.line(img, (rx + rw - 1, ry), (rx + rw - 1, ry + rh - 1), (255, 0, 0), 3)
        cv.line(img, (rx + rw - 1, ry + rh - 1), (rx, ry + rh - 1), (255, 0, 0), 3)
        cv.line(img, (rx, ry + rh - 1), (rx, ry), (255, 0, 0), 3)
    return img, cnts


def image_detect(file_name: str) -> List[Tuple[int, int]]:
    img = cv.imread(file_name + ".jpg")
    if img is None:
        return []
    out, cnts = process(img)
    cv.imwrite(file_name + "-out.jpg", out)
    return [cvtool.contour_center(c) for c in cnts]
