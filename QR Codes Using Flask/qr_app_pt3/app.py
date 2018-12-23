from flask import Flask, render_template, request

from qrwifi.functions import wifi_qr

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html.j2")

@app.route("/create", methods=["POST"])
def create():
    res = request.form
    qr = wifi_qr(ssid=res["ssid"], password=res["password"], security=res["security"])
    # qr_b64 = qr.png_as_base64_str(scale=10)
    qr_b64 = qr.png('static/file.png', scale=10)
    return render_template("qr.html.j2", qr_b64=qr_b64)

def run():
    app.run(debug=True, port=5690, host="0.0.0.0")

if __name__ == "__main__":
    run()