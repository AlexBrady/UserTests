import typing

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from corelibs.models import Tester, Image, Video
from corelibs import db


class BasePersistor:

    def __init__(self, scoped_session: bool = False):
        self.db = db
        self.scoped_session = scoped_session

    def _add(self, value):
        self.db.session.add(value)

        if not self.scoped_session:
            self.db.session.commit()

    def ensure_tester_is_valid(self, tester_id: str) -> bool:
        return bool(
            self.db.session.query(Tester)
                           .join(Image)
                           .join(Video)
                           .filter(Tester.id == tester_id,
                                   Image.tester_id == tester_id,
                                   Video.tester_id == tester_id)
                           .first()
            )


class TesterPersisor(BasePersistor):

    def __init__(self, scoped_session=False):
        """Initialize."""
        super().__init__(scoped_session)

    def add_tester(self, tester: Tester):
        self._add(tester)

    def get_tester(self, tester_id: str) -> typing.Tuple[Tester, int]:
        count_query = (
            self.db.session.query(func.count(1))
                           .filter(Image.tester_id == tester_id)
                           .as_scalar()
            )

        query = (
            self.db.session.query(Tester, count_query)
                           .filter_by(id=tester_id)
                           .options(joinedload(Tester.images))
            )

        return query.first()

    def get_testers(self, test_id: str):
        return (
            self.db.session.query(Tester)
                           .filter_by(test_id=test_id)
                           .options(joinedload(Tester.images))
                           .all()
            )


class ImagePersisor(BasePersistor):

    def __init__(self, scoped_session=False):
        """Initialize."""
        super().__init__(scoped_session)

    def add_image(self, image: Image):
        self._add(image)

    def get_images(self, tester_id: str):
        return self.db.session.query(Image).filter_by(tester_id=tester_id).all()

    def get_image(self, image_id: str):
        return self.db.session.query(Image).filter_by(id=image_id).first()


class VideoPersisor(BasePersistor):

    def __init__(self, scoped_session=False):
        """Initialize."""
        super().__init__(scoped_session)

    def add_video(self, video: Video):
        self._add(video)

    def get_video(self, video_id: str):
        return self.db.session.query(Video).filter_by(id=video_id).first()
