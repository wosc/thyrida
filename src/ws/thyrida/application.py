from pyramid.view import view_config
import pkg_resources
import pyramid.config
import pyramid.paster
import pyramid.registry
import pyramid_jinja2
import re
import ws.thyrida
import ws.thyrida.db
import ws.thyrida.interfaces
import zope.component
import zope.interface


class Application(object):

    DONT_SCAN = [re.compile('tests$').search]

    def __call__(self, global_conf, **settings):
        self.configure_pyramid(settings)
        self.configure_routes()
        return self.config.make_wsgi_app()

    def configure_pyramid(self, settings):
        self.settings = Settings()
        self.settings.update(settings)
        self.settings['version'] = pkg_resources.get_distribution(
            'ws.thyrida').version
        zope.component.provideUtility(
            self.settings, ws.thyrida.interfaces.ISettings)

        db = ws.thyrida.db.Database(self.settings['sqlalchemy.url'])
        zope.component.provideUtility(db)

        registry = pyramid.registry.Registry(
            bases=(zope.component.getGlobalSiteManager(),))
        c = self.config = pyramid.config.Configurator(registry=registry)
        c.setup_registry(settings=self.settings)
        # setup_registry() insists on copying the settings mapping into a new
        # `pyramid.config.settings.Settings` instance, sigh.
        self.settings.update(c.registry.settings)
        c.registry.settings = self.settings

        c.include('pyramid_tm')
        self.configure_jinja()

    def configure_jinja(self):
        c = self.config

        # We don't use include('pyramid_jinja2') since that already sets up a
        # renderer for `.jinja2` files which we don't want.
        c.add_directive(
            'add_jinja2_renderer', pyramid_jinja2.add_jinja2_renderer)
        c.add_directive(
            'add_jinja2_search_path', pyramid_jinja2.add_jinja2_search_path)
        c.add_directive(
            'add_jinja2_extension', pyramid_jinja2.add_jinja2_extension)
        c.add_directive(
            'get_jinja2_environment', pyramid_jinja2.get_jinja2_environment)

        c.add_jinja2_renderer('.html')
        c.add_jinja2_search_path('ws.thyrida:', '.html')

        c.commit()

    def configure_routes(self):
        c = self.config

        c.add_route('home', '/')
        c.add_route('change_password', '/password')

        c.scan(package=ws.thyrida, ignore=self.DONT_SCAN)


app_factory = Application()


@zope.interface.implementer(ws.thyrida.interfaces.ISettings)
class Settings(dict):
    pass


@view_config(route_name='home', renderer='string')
def home(request):
    return 'OK'
