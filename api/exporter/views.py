

from flask import Blueprint
from flask_io import fields, Error

from corelibs.persistors import TesterPersisor, ImagePersisor, VideoPersisor
from api.services import build_file_response
from api.schemas import TesterSchema, ImageSchema
from api import io


app = Blueprint('exporter', __name__, url_prefix='/exporter')


@app.route('/<tester_id>/metadata', methods=['GET'])
@io.marshal_with(TesterSchema)
def get_tester_metadata(tester_id):
    persistor = TesterPersisor()

    if not persistor.ensure_tester_is_valid(tester_id):
        return io.bad_request('Tester must have at least one image and video.')

    tester = persistor.get_tester(tester_id)

    if not tester:
        return io.bad_request(f'Tester not found: {tester_id}')

    tester, images_count = tester
    setattr(tester, 'images_count', images_count)

    return tester


@app.route('/<tester_id>/images', methods=['GET'])
@io.marshal_with(ImageSchema, envelope='images')
def get_images(tester_id):
    persistor = ImagePersisor()

    if not persistor.ensure_tester_is_valid(tester_id):
        return io.bad_request('Tester must have at least one image and video.')

    return ImagePersisor().get_images(tester_id)


@app.route('/image/<image_id>', methods=['GET'])
@io.from_header('tester_id', fields.Integer(required=True))
def download_image(image_id, tester_id):
    persistor = ImagePersisor()

    if not persistor.ensure_tester_is_valid(tester_id):
        return io.bad_request('Tester must have at least one image and video.')

    image = persistor.get_image(image_id)

    if not image:
        return io.bad_request(f'Image not found: {image_id}')

    if tester_id != image.tester_id:
        return io.forbidden(Error('You are not allowed to perform this action.', 'forbidden'))

    return build_file_response(image)


@app.route('/video/<video_id>', methods=['GET'])
@io.from_header('tester_id', fields.Integer(required=True))
def download_video(video_id, tester_id):
    persistor = VideoPersisor()

    if not persistor.ensure_tester_is_valid(tester_id):
        return io.bad_request('Tester must have at least one image and video.')

    video = persistor.get_video(video_id)

    if not video:
        return io.bad_request(f'Video not found: {video_id}')

    if tester_id != video.tester_id:
        return io.forbidden(Error('You are not allowed to perform this action.', 'forbidden'))

    return build_file_response(video)


@app.route('/testers/<test_id>', methods=['GET'])
@io.marshal_with(TesterSchema, envelope='testers')
def get_testers(test_id):
    return TesterPersisor().get_testers(test_id)
