
import magic
import os
from datetime import datetime

from flask import Blueprint, request
from flask_io import fields

from api.schemas import ImageSchema, TesterSchema, VideoSchema
from corelibs.models import Image, Video
from corelibs.persistors import TesterPersisor, ImagePersisor, VideoPersisor
from api import io


app = Blueprint('importer', __name__, url_prefix='/importer')


@app.route('/tester', methods=['POST'])
@io.marshal_with(TesterSchema)
@io.from_body('tester', TesterSchema)
def import_tester(tester):
    """
    Import a user with a json body, see TesterSchema for input types.

    :param tester:
    :return:
    """
    tester_persistor = TesterPersisor()
    tester_persistor.add_tester(tester)

    return tester


@app.route('/images', methods=['POST'])
@io.marshal_with(ImageSchema, envelope='images')
@io.from_header('tester_id', fields.Integer(required=True))
@io.from_body('image_data', ImageSchema(many=True))
def import_images(tester_id, image_data):
    """
    Import images for a tester, see ImageSchema for input types.

    Can import multiple images at once.
    The path will have to be './images/xx.png'

    Note: The function of this is poor, as the images are expected to be in the project folder...
          In hindsight, choosing a serialisation package/library that better handles bulk files should have been a
          priority.
    :param tester_id:
    :param image_data:
    :return:
    """
    image_persistor = ImagePersisor()

    images = []
    for entry in image_data:
        image = Image()
        image.tester_id = tester_id
        image.height = entry.get('height')
        image.width = entry.get('width')
        image.time = datetime.fromtimestamp(entry.get('time') / 1e9)

        if not os.path.exists(entry.get('image_path')):
            continue

        with open(entry.get('image_path'), 'rb') as image_file:
            image.content = image_file.read()
            image.mimetype = magic.from_buffer(image.content, mime=True)

        image.filename = os.path.basename(entry.get('image_path'))

        image_persistor.add_image(image)
        images.append(image)

    return images


@app.route('/video', methods=['POST'])
@io.marshal_with(VideoSchema)
@io.from_header('tester_id', fields.Integer(required=True))
@io.from_form('duration', fields.Integer(required=True))
@io.from_form('time', fields.Integer(required=True))
def import_video(tester_id, duration, time):
    """
    Import a video from a tester with a form-data body.

    :param tester_id:
    :param duration:
    :param time:
    :return:
    """
    file = request.files.get('file')
    if file is None:
        return io.bad_request('Missing file')

    video = Video()
    video.tester_id = tester_id
    video.duration = duration

    video.time = datetime.fromtimestamp(time / 1e9)
    video.filename = file.filename
    video.mimetype = file.mimetype
    video.content = file.read()

    VideoPersisor().add_video(video)

    return video
