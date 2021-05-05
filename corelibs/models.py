
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import BLOB

from corelibs import db


class Tester(db.Model):
    """Model for tester."""

    __tablename__ = 'tester'

    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, nullable=False)
    time = Column(DateTime, nullable=False)
    phone_manufacturer = Column(String(32), nullable=False)
    phone_model = Column(String(32), nullable=False)
    phone_screen_height = Column(String(10), nullable=False)
    phone_screen_width = Column(String(10), nullable=False)

    images = relationship('Image', back_populates='tester', lazy='noload')
    videos = relationship('Video', back_populates='tester', lazy='noload')


class Image(db.Model):
    """Model for images."""

    __tablename__ = 'images'

    __table_args__ = (
        UniqueConstraint('tester_id', 'time'),
        )

    id = Column(Integer, primary_key=True)
    tester_id = Column(ForeignKey('tester.id'), nullable=False)
    height = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    time = Column(DateTime, nullable=False)
    filename = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
    content = Column(BLOB, nullable=False)

    tester = relationship('Tester', lazy='noload')


class Video(db.Model):
    """Model for videos."""

    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    tester_id = Column(ForeignKey('tester.id'), nullable=False)
    duration = Column(Integer, nullable=False)
    time = Column(DateTime, nullable=False)
    filename = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
    content = Column(BLOB, nullable=False)

    tester = relationship('Tester', lazy='noload')
