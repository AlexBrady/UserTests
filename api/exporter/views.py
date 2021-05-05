

from flask import Blueprint, Response
from flask_io import fields, Error
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from corelibs.models import Image, Video, Tester
from api.schemas import TesterSchema, ImageSchema
from corelibs import db
from api import io


app = Blueprint('exporter', __name__, url_prefix='/exporter')


@app.route('/<tester_id>/metadata', methods=['GET'])
@io.marshal_with(TesterSchema)
def get_tester_metadata(tester_id):
    count_query = db.session.query(func.count(1)).filter(
        Image.tester_id == tester_id).as_scalar()
    query = db.session.query(Tester, count_query).filter_by(id=tester_id).options(joinedload(Tester.images))
    result = query.first()

    if not result:
        return io.bad_request(f'Tester not found: {tester_id}')

    result, images_count = result
    setattr(result, 'images_count', images_count)

    return result


@app.route('/<tester_id>/images', methods=['GET'])
@io.marshal_with(ImageSchema, envelope='images')
def get_images(tester_id):
    query = db.session.query(Image).filter_by(tester_id=tester_id)
    result = query.all()

    return result


@app.route('/image/<image_id>', methods=['GET'])
@io.from_header('tester_id', fields.Integer(required=True))
def download_image(image_id, tester_id):
    query = db.session.query(Image).filter_by(id=image_id)
    image = query.first()

    if not image:
        return io.bad_request(f'Image not found: {image_id}')

    if tester_id != image.tester_id:
        return io.forbidden(Error('You are not allowed to perform this action.', 'forbidden'))

    response = Response(image.content)
    response.headers['Content-Disposition'] = f'attachment; filename={image.filename}'
    response.content_type = image.mimetype

    return response


@app.route('/video/<video_id>', methods=['GET'])
@io.from_header('tester_id', fields.Integer(required=True))
def download_video(video_id, tester_id):
    query = db.session.query(Video).filter_by(id=video_id)
    video = query.first()

    if not video:
        return io.bad_request(f'Video not found: {video_id}')

    if tester_id != video.tester_id:
        return io.forbidden(Error('You are not allowed to perform this action.', 'forbidden'))

    response = Response(video.content)
    response.headers['Content-Disposition'] = f'attachment; filename={video.filename}'
    response.content_type = video.mimetype

    return response


@app.route('/testers/<test_id>', methods=['GET'])
@io.marshal_with(TesterSchema, envelope='testers')
def get_testers(test_id):
    query = db.session.query(Tester).filter_by(test_id=test_id).options(joinedload(Tester.images))
    testers = query.all()

    return testers
