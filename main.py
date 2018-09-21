import pyqrcode as pq
import numpy as np
from solid import color, cube, scad_render, translate, union


def create_wifi_qr(ssid: str, security: str, password: str):
    qr = pq.create(f'WIFI:S:{ssid};T:{security};P:{password};;')
    return qr


def qr2array(qr):
    arr = []
    for line in qr.text().split():
        if line:
            arr.append([int(bit) for bit in line])
    return np.vstack(arr)


def make_solid(arr):
    HEIGHT = 1
    SCALE = 2  # output defaults to 1 mm per unit; this lets us increase the size of objects proportionally.
    cubes = [translate([i * SCALE, j * SCALE, 0])(color('black')(cube(size=[SCALE, SCALE, HEIGHT])))
             for i, row in enumerate(arr)
             for j, col in enumerate(row)
             if arr[i, j] == 1]

    base_plate = color('white')(cube(size=(arr.shape[0] * SCALE, arr.shape[1] * SCALE, HEIGHT / 2)))
    qrobj = union()(*cubes, base_plate)
    return qrobj


def main():
    ssid = "Family Guest Network"
    security = "WPA"
    password = "vn8h2sncu093y3nd!"
    qr = create_wifi_qr(ssid, security, password)
    arr = qr2array(qr)
    solid_object = make_solid(arr)
    print(scad_render(solid_object))


if __name__ == '__main__':
    main()