from qrcode.main import QRCode

def generate_qr_code(url):
    qr = QRCode(
        version=1,
        box_size=10,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img