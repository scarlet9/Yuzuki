from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from model.base import Base
from helper.pbkdf2 import pbkdf2, pbkdf2_check


class User(Base):
    __tablename__ = "user"
    uid = Column(Integer(), primary_key=True)
    username = Column(String(255), index=True, unique=True, nullable=False)
    nickname = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    groups = relationship("Group", secondary="assoc_user_group")
    pd_realname = Column(String(255), nullable=False)
    pd_email = Column(String(255))
    pd_address = Column(String(255))
    pd_phone = Column(String(255))
    pd_bunryu = Column(Integer(), ForeignKey("group.uid"), nullable=False)
    pd_bio = Column(Text())
    created_at = Column(DateTime(), default=datetime.now)
    is_admin = Column(Boolean, default=False)

    def __init__(self, username, nickname, password, pd_realname, pd_email, pd_address, pd_phone, pd_bunryu, pd_bio):
        self.username = username
        self.nickname = nickname
        self.password = pbkdf2(password)
        self.pd_realname = pd_realname
        self.pd_email = pd_email
        self.pd_address = pd_address
        self.pd_phone = pd_phone
        self.pd_bunryu = pd_bunryu
        self.pd_bio = pd_bio

    def check_password(self, password):
        return pbkdf2_check(password, self.password)

    def __repr__(self):
        return "<User name=%s>" % self.username