from pyramid.view import view_config
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
import crypt
import hmac
import sqlalchemy.exc
import ws.thyrida.db
import wtforms


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

    @classmethod
    def find_by_login(cls, login):
        return cls.db().query(cls).filter_by(login=login).one()

    def authenticate(self, entered_password):
        return hmac.compare_digest(
            crypt.crypt(entered_password, self.password), self.password)

    def set_password(self, password):
        self.password = crypt.crypt(password, crypt.METHOD_SHA512)


@view_config(
    route_name='change_password',
    renderer='templates/password.html')
def change_password(request):
    form = ChangePasswordForm(request.POST)
    result = {'form': form}
    if request.method == 'POST':
        if form.validate():
            form.errors['current_password'] = 'Invalid username or password'
            try:
                mailbox = Mailbox.find_by_login(form.email.data)
            except sqlalchemy.exc.InvalidRequestError:
                return result
            if mailbox.authenticate(form.current_password.data):
                mailbox.set_password(form.new_password.data)
                result['form'] = 'success'
    return result


class ChangePasswordForm(wtforms.Form):

    email = StringField('Email address', validators=[DataRequired()])
    current_password = PasswordField(
        'Current Password', validators=[DataRequired()])
    new_password = PasswordField(
        'New Password', validators=[
            DataRequired(),
            EqualTo('confirm_password',
                    message='Does not match confirmation')])
    confirm_password = PasswordField('Confirm', validators=[DataRequired()])
