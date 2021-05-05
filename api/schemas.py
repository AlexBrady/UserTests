
from datetime import datetime
from flask_io import fields, Schema, post_load, pre_load, post_dump, pre_dump

from corelibs.models import Tester, Image


class ImageSchema(Schema):
    id = fields.Integer(dump_only=True)
    height = fields.Integer(required=True)
    width = fields.Integer(required=True)
    time = fields.Integer(required=True)
    timestamp = fields.DateTime(dump_only=True)
    pic_num = fields.Integer(required=True)
    filename = fields.String(dump_only=True)
    image_path = fields.String(required=True, load_only=True)

    @pre_dump
    def _pre_dump(self, obj):
        obj.timestamp = obj.time


class TesterSchema(Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.Integer(required=True)
    time = fields.DateTime(required=True)
    phone_manufacturer = fields.String(required=True)
    phone_model = fields.String(required=True)
    phone_screen_height = fields.String(required=True)
    phone_screen_width = fields.String(required=True)
    images_count = fields.Integer(dump_only=True)
    images = fields.Nested(ImageSchema, many=True, dump_only=True)

    @post_load
    def _make_object(self, data):
        return Tester(**data)
