import os
import pathlib
from PIL import Image
from flask import current_app


def upload_picture(picture, user_id, output_size=(200, 200), folder=''):
    filename = picture.filename
    # Grab extension type .jpg or .png
    # ext_type = filename.split('.')[-1]
    storage_filename = str(user_id) + '/' + filename

    pathlib.Path(current_app.root_path, 'static/images', folder, str(user_id)).mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(current_app.root_path, 'static/images', folder, storage_filename)

    # Open the picture and save it
    pic = Image.open(picture)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename
