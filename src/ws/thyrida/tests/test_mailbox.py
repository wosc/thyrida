from ws.thyrida.mailbox import Domain, Mailbox
import transaction


def test_orm_setup_works(db):
    domain = Domain(name='example.com')
    db.session.add(domain)
    mailbox = Mailbox(
        domain=domain, local_part='test',
        login='test', password='secret', action='none', mailbox_path='none')
    db.session.add(mailbox)
    transaction.commit()
    db.session.close()
    mailbox = Mailbox.find_by_id(1)
    assert mailbox.local_part == 'test'
    assert mailbox.domain.name == 'example.com'


def test_change_password_sucessfully(db, httpclient):
    domain = Domain(name='example.com')
    db.session.add(domain)
    mailbox = Mailbox(
        domain=domain, local_part='test',
        login='test@example.com', action='none', mailbox_path='none')
    mailbox.set_password('secret')
    db.session.add(mailbox)
    transaction.commit()
    assert mailbox.authenticate('secret')

    r = httpclient.post('/password', {
        'email': 'test@example.com',
        'current_password': 'secret',
        'new_password': 'changed',
        'confirm_password': 'changed'
    })
    assert 'Password changed successfully' in r.text

    mailbox = Mailbox.find_by_login('test@example.com')
    assert mailbox.authenticate('changed')
