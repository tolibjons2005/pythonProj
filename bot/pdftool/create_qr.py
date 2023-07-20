import qrcode
import os

from db.user import get_n_test


# import qrcode.image.svg
def create_directory(name):
    directory = f"id{name}"

    # Parent Directories
    parent_dir = "/root/cardbot/pythonProject/bot/pdftool/qrcodes"

    # Path
    path = os.path.join(parent_dir, directory)

    # Create the directory
    # 'Nikhil'
    try:
        os.makedirs(path)
    except FileExistsError:
    # directory already exists
        pass
def create_qr_f(id, name, n, test_type):

    # Leaf directory
    if test_type == '90':
        n=n[0]
    if test_type == '30':
        n=n[1]


    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=15, border=0)
    idn=test_type+ str(id)+n

    qr.add_data(idn)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')
    img.save(f'/root/cardbot/pythonProject/bot/pdftool/qrcodes/id{name}/id{id}.png')

async def create_qr_fo(id, test_type=None, channel_name=None):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=15, border=0)
    if test_type:
        idn = '6'+test_type + str(id)

        qr.add_data(idn)
        qr.make(fit=True)

        img = qr.make_image(fill_color='black', back_color='white')
        img.save(f'/root/cardbot/pythonProject/bot/pdftool/qrcodes/channel_link/t_id{id}.png')
    else:

        qr.add_data(channel_name)
        qr.make(fit=True)

        img = qr.make_image(fill_color='black', back_color='white')
        img.save(f'/root/cardbot/pythonProject/bot/pdftool/qrcodes/channel_link/id{id}.png')
# factory = qrcode.image.svg.SvgPathImage
# svg_img = qrcode.make('SALOM', image_factory=factory)
# svg_img.save('advanced.svg')
