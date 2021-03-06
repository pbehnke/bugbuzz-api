from __future__ import unicode_literals

from ... import models
from ..events.resources import EventIndexResource
from ..breaks.resources import BreakIndexResource
from ..files.resources import FileIndexResource
from ..base import ResourceBase


class SessionIndexResource(ResourceBase):

    def __getitem__(self, key):
        session = models.Session.query.get(key)
        if session is None:
            return
        return SessionResource(
            self.request,
            parent=self,
            name=key,
            entity=session,
        )


class SessionResource(ResourceBase):
    def __getitem__(self, key):
        if key == 'actions':
            return SessionActionResource(
                self.request,
                parent=self,
                name=key,
                entity=self.entity,
            )
        elif key == 'events':
            return EventIndexResource(
                self.request,
                parent=self,
                name=key,
                entity=self.entity,
            )
        elif key == 'breaks':
            return BreakIndexResource(
                self.request,
                parent=self,
                name=key,
                entity=self.entity,
            )
        elif key == 'files':
            return FileIndexResource(
                self.request,
                parent=self,
                name=key,
                entity=self.entity,
            )


class SessionActionResource(ResourceBase):
    pass
