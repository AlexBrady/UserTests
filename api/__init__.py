from flask import Flask
from flask_io import FlaskIO

from .config import Base

__version__ = '1.0.0'

app = Flask(__name__)
app.config.from_object(Base)

io = FlaskIO()
io.init_app(app)
