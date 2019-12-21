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
