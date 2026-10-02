import qrcode


def generate_qr_image(data, file_path):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image()
    image.save(file_path)