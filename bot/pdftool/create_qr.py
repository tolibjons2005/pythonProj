import qrcode
import os
# import qrcode.image.svg
def create_directory(name):
    directory = f"id{name}"

    # Parent Directories
    parent_dir = "D:/pythonProject/bot/pdftool/qrcodes"

    # Path
    path = os.path.join(parent_dir, directory)

    # Create the directory
    # 'Nikhil'
    try:
        os.makedirs(path)
    except FileExistsError:
    # directory already exists
        pass
def create_qr_f(id, name):


    # Leaf directory

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=15, border=0)

    qr.add_data(id)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')
    img.save(f'D:/pythonProject/bot/pdftool/qrcodes/id{name}/id{id}.png')

# factory = qrcode.image.svg.SvgPathImage
# svg_img = qrcode.make('SALOM', image_factory=factory)
# svg_img.save('advanced.svg')