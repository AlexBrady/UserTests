
from flask_io import fields, Schema, post_load

from corelibs.models import Tester, Image


class TesterSchema(Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.Integer(required=True)
    time = fields.DateTime(required=True)
    phone_manufacturer = fields.String(required=True)
    phone_model = fields.String(required=True)
    phone_screen_height = fields.String(required=True)
    phone_screen_width = fields.String(required=True)

    @post_load
    def _make_object(self, data):
        return Tester(**data)


class ImageSchema(Schema):
    id = fields.Integer(dump_only=True)
    height = fields.Integer(required=True)
    width = fields.Integer(required=True)
    time = fields.Integer(required=True)
    pic_num = fields.Integer(required=True)
    image_path = fields.String(required=True)


class ImporterSchema(Schema):
    tester = fields.Nested(TesterSchema, required=True)
    image_data = fields.Nested(ImageSchema, required=True, many=True)


