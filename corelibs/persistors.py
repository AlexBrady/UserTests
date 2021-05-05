import typing

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


class TesterPersisor(BasePersistor):

    def __init__(self, scoped_session=False):
        """Initialize."""
        super().__init__(scoped_session)

    def add_tester(self, tester: Tester):
        self._add(tester)

