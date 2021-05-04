
import magic
import os
from datetime import datetime

from flask import Blueprint, request
from flask_io import fields

from .schemas import ImageSchema, TesterSchema
from corelibs.models import Image, Video
from corelibs import db
from api import io


app = Blueprint('testers', __name__, url_prefix='/testers')


@app.route('/', methods=['POST'])
@io.marshal_with(TesterSchema)
@io.from_body('tester_data', TesterSchema)
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


@app.route('/video', methods=['POST'])
@io.from_header('tester_id', fields.Integer(required=True))
@io.from_form('duration', fields.Integer(required=True))
@io.from_form('time', fields.Integer(required=True))
def upload_video(tester_id, duration, time):
    file = request.files.get('file')
    if file is None:
        return io.bad_request('Missing file')

    video = Video()
    video.tester_id = tester_id
    video.duration = duration
    print(datetime.fromtimestamp(time / 1e9))

    video.time = datetime.fromtimestamp(time / 1e9)
    video.filename = file.filename
    video.mimetype = file.mimetype
    video.content = file.read()

    db.session.add(video)
    db.session.commit()
