
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Date, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import BLOB

from corelibs import db


class Test(db.Model):
    """Model for tests."""

    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, default=datetime.now)

    testers = relationship('Tester', lazy='noload')


class Tester(db.Model):
    """Model for testers."""

    __tablename__ = 'testers'

    id = Column(Integer, primary_key=True)
    test_id = Column(ForeignKey('tests.id'), nullable=False, index=True)
    time = Column(DateTime, nullable=False)
    phone_manufacturer = Column(String(32), nullable=False)
    phone_model = Column(String(32), nullable=False)
    phone_screen_height = Column(String(10), nullable=False)
    phone_screen_width = Column(String(10), nullable=False)

    test = relationship('Test', lazy='noload')


class Image(db.Model):
    """Model for images."""

    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    tester_id = Column(ForeignKey('testers.id'), nullable=False)
    height = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    filename = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
    content = Column(BLOB, nullable=False)

    tester = relationship('Tester', lazy='noload')


class Video(db.Model):
    """Model for videos."""

    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    duration = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)

    file = relationship('VideoFile', lazy='noload')


class VideoFile(db.Model):
    """Model for video files."""

    __tablename__ = 'video_files'

    video_id = Column(ForeignKey('videos.id'), primary_key=True, nullable=False)
    format = Column(String(6), primary_key=True, nullable=False)
    blob_id = Column(BLOB, nullable=False)
    size = Column(Integer, nullable=False)

    video = relationship('Video', lazy='noload')
