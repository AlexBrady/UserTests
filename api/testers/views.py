
import magic
import os

from flask import Blueprint, Response
from flask_io import fields

from .schemas import ImporterSchema, ImageSchema
from corelibs.models import Image
from corelibs import db
from api import io


app = Blueprint('testers', __name__, url_prefix='/testers')


@app.route('/', methods=['POST'])
@io.marshal_with(ImporterSchema)
@io.from_body('tester_data', ImporterSchema)
def import_tester(tester_data):
    db.session.add(tester_data)
    db.session.commit()

    return tester_data


@app.route('/images', methods=['POST'])
@io.from_header('tester_id', fields.Integer(required=True))
@io.from_body('image_data', ImageSchema(many=True))
def upload_images(tester_id, image_data):
    for entry in image_data:
        image = Image()
        image.tester_id = tester_id
        image.height = entry.get('height')
        image.width = entry.get('width')
        image.time = entry.get('time')

        if not os.path.exists(entry.get('image_path')):
            continue

        with open(entry.get('image_path'), 'rb') as image_file:
            image.content = image_file.read()
            image.mimetype = magic.from_buffer(image.content, mime=True)
        image.filename = os.path.basename(entry.get('image_path'))
        db.session.add(image)

    db.session.commit()
