"""
Encoding WiFi credentials in a QR code

Example Inputs:
SSID (a.k.a. Network Name): Family Guest Network
Password: vn8h2sncu093y3nd!
Security Type (one of WPA or WEP): WPA

"""

import pyqrcode as pq
ssid = "Family Guest Network"
security = "WPA"
password = "vn8h2sncu093y3nd!"

# Create the QR code and print it to terminal
qr = pq.create(f'WIFI:S:{ssid};T:{security};P:{password};;')
print(qr.terminal())

# Save the QR code to a PNG
qr.png('home_guest_wifi.png')