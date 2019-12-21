from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
import ws.thyrida.db


class Domain(ws.thyrida.db.Object):

    __tablename__ = 'domains'

    name = Column(String(255))
    mailboxes = relationship('Mailbox', backref='domain')


class Mailbox(ws.thyrida.db.Object):

    __tablename__ = 'mailboxes'

    domain_id = Column(Integer, ForeignKey('domains.id'))

    local_part = Column(String(50))
    dotted_address = Column(String(255))

    login = Column(String(255))
    password = Column(String(50))

    forward = Column(String(255))
    has_mailbox = Column(Integer, server_default='0')
    has_vacation = Column(Integer, server_default='0')
    has_spamfilter = Column(Integer, server_default='0')

    vacation_subject = Column(String(255))
    vacation_body = Column(Text)

    action = Column(String(255))
    mailbox_path = Column(String(255))

    uid = Column(Integer, server_default='1')
    gid = Column(Integer, server_default='1')
