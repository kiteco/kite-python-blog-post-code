import numpy as np
import pyqrcode as pq


def wifi_qr(ssid: str, security: str, password: str):
    """
    Creates the WiFi QR code object.
    """
    qr = pq.create(f"WIFI:S:{ssid};T:{security};P:{password};;")
    return qr


def qr2array(qr):
    """
    Convert a QR code object into its array representation.
    """
    arr = []
    for line in qr.text().split("\n"):
        if line:
            arr.append(list(map(int, line)))
    return np.vstack(arr)


def png_b64(qr, scale: int = 10):
    """
    Return the base64 encoded PNG of the QR code.
    """
    return qr.png_data_uri(scale=scale)
