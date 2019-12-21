import pytest
import webtest
import ws.thyrida.application
import ws.thyrida.db
import zope.component


@pytest.fixture()
def db(tmpdir):
    db = ws.thyrida.db.Database(
        'sqlite:///%s' % (tmpdir / 'test.db'), testing=True)
    zope.component.provideUtility(db)
    db.initialize_database()
    yield db
    zope.component.getSiteManager().unregisterUtility(db)


@pytest.fixture()
def application(db):
    return ws.thyrida.application.app_factory(None, **{
        'sqlalchemy.url': db.engine.url,
    })


@pytest.fixture()
def httpclient(application):
    return webtest.TestApp(application)
