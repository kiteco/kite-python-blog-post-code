"""
Create a CLI interface such that...

$ qrwifi --ssid ”<SSID_NAME>” \
          --security ”<SECURITY>” \
          --password ”<PASSWORD>” \
          [terminal|png --filename ”<FILEPATH>”]


"""

import click

# Depending on your IDE settings ...
# from .functions import wifi_qr, qr2array

from qrwifi.functions import wifi_qr


@click.group()
@click.option("--ssid", help="WiFi network name.")
@click.option("--security", type=click.Choice(["WEP", "WPA", ""]))
@click.option("--password", help="WiFi password.")
@click.pass_context
def main(ctx, ssid: str, security: str = "", password: str = ""):
    qr = wifi_qr(ssid=ssid, security=security, password=password)
    ctx.obj["qr"] = qr


@main.command()
@click.pass_context
def terminal(ctx):
    """Print QR code to the terminal."""
    print(ctx.obj["qr"].terminal())


@main.command()
@click.option("--filename", help="full path to the png file")
@click.pass_context
def png(ctx, filename, scale: int = 10):
    """Create a PNG file of the QR code."""
    ctx.obj["qr"].png(filename, scale)


def start():
    main(obj={})


if __name__ == "__main__":
    start()
