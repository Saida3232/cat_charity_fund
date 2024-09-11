from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import BaseModelProject


class Donation(BaseModelProject):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)