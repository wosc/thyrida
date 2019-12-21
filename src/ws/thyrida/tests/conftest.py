import pytest
import ws.thyrida.db
import zope.component


@pytest.fixture()
def db(request):
    db = ws.thyrida.db.Database('sqlite:///', testing=True)
    zope.component.provideUtility(db)
    db.initialize_database()
    yield db
    zope.component.getSiteManager().unregisterUtility(db)
