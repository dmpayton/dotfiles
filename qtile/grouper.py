import gobject

import libqtile.hook
from libqtile.manager import Key
from libqtile.command import lazy


class Match(object):
    ''' Match for dynamic groups
        it can match by title, class or role
    '''

    def __init__(self, title=[], wm_class=[], role=[], wm_type=[]):
        self._rules = [('title', t) for t in title]
        self._rules += [('wm_class', w) for w in wm_class]
        self._rules += [('role', r) for r in  role]
        self._rules += [('wm_type', r) for r in  wm_type]

    def __repr__(self):
        return '<Match:%s>' % self._rules

    def compare(self, client):
        for _type, rule in self._rules:
            match_func = getattr(rule, 'match', None) or \
                         getattr(rule, 'count')

            if _type == 'title':
                value = client.name
            elif _type == 'wm_class':
                value = client.window.get_wm_class()
                if value:
                    value = value[1]
            elif _type == 'wm_type':
                value = client.window.get_wm_type()
            else:
                value = client.window.get_wm_window_role()

            if value and match_func(value):
                return True
        return False


class AppGrouper(object):
    ''' Send new windows to a specific group when created '''

    def __init__(self, qtile, apps):
        self.qtile = qtile
        self.apps = apps
        libqtile.hook.subscribe.client_new(self._add)

    def _add(self, client):
        #open(os.path.expanduser('~/window-classes'), 'a').write('{0}\n'.format(str(client.window.get_wm_class())))
        for app in self.apps:
            if app['match'].compare(client):
                client.togroup(app['group'])
