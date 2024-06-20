import cv2 as cv
import numpy as np


def GetCorners(img):
    points = []

    def mouseHandler(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            points.append([x, y])
            img[y][x] = (255, 255, 255)
            print("klik")

    cv.namedWindow("img")
    cv.setMouseCallback("img", mouseHandler)

    while len(points) < 4:
        cv.imshow("img", img)
        cv.waitKey(1)

    cv.setMouseCallback("img", lambda e, x, y, f, p: None)

    return points


def Lerp(a, b, scale):
    return a + (b - a) * scale


def Skew(img, skew):
    corners = GetCorners(img)

    width = corners[2][0] - corners[0][0]
    height = corners[2][1] - corners[0][1]

    skew = cv.resize(skew, (width, height))

    for r in range(height):
        for c in range(width):
            r_percent = r/height
            c_percent = c/width

            # TL -> TR
            a_r = (Lerp(corners[0][1], corners[3][1], c_percent))
            a_c = (Lerp(corners[0][0], corners[3][0], c_percent))

            # BL -> BR
            b_r = (Lerp(corners[1][1], corners[2][1], c_percent))
            b_c = (Lerp(corners[1][0], corners[2][0], c_percent))

            r_lerp = int(Lerp(a_r, b_r, r_percent))
            c_lerp = int(Lerp(a_c, b_c, r_percent))

            img[r_lerp][c_lerp] = skew[r][c]

    return img


def UnSkew(img):
    corners = GetCorners(img)

    width = corners[2][0] - corners[0][0]
    height = corners[2][1] - corners[0][1]

    img2 = np.zeros(img.shape, "uint8")

    for r in range(height):
        for c in range(width):
            r_percent = r/height
            c_percent = c/width

            # TL -> TR
            a_r = (Lerp(corners[0][1], corners[3][1], c_percent))
            a_c = (Lerp(corners[0][0], corners[3][0], c_percent))

            # BL -> BR
            b_r = (Lerp(corners[1][1], corners[2][1], c_percent))
            b_c = (Lerp(corners[1][0], corners[2][0], c_percent))

            r_lerp = int(Lerp(a_r, b_r, r_percent))
            c_lerp = int(Lerp(a_c, b_c, r_percent))

            img2[r][c] = img[r_lerp][c_lerp]

    return img2
