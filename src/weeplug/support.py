# -*- coding: utf-8 -*-
""" weeplug – WeeChat script helpers.
"""
# Copyright ⓒ  2014 pyroscope <pyroscope.project@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
from collections import namedtuple


ScriptRegistration = namedtuple('ScriptRegistration', 'name, author, version, license, description, shutdown_function, charset')


class ScriptBase(object):
    """ Base class for WeeChat scripts.
    """

    @classmethod
    def load_via_shim(cls, namespace):
        """ Load a script from a shim file.
        """
        # TODO: Lookup / import entry point
        script = WeePlugScriptBase(namespace)

        if not script.api.register(*script.registration):
            return

        weechat_version = int(script.api.info_get('version_number', '') or 0)
        if weechat_version < 0x00030700:
            script.log('need WeeChat version 0.3.7 or higher', prefix='error')
            script.api.command('', '/wait 1ms /python unload {0}'.format(script.name))
        else:
            script.on_load()


    def __init__(self, namespace, **kwargs):
        """ Initialize script object.
        """
        import weechat

        # This allows later additions / putting up a facade
        self.api = weechat

        # Fix 'prnt' abomination
        if not hasattr(self.api, 'print_'):
            self.api.print_ = self.api.prnt
            #self.api.print_date = self.api.prnt_date
            #self.api.print_tags = self.api.prnt_tags
            self.api.print_date_tags = self.api.prnt_date_tags
            self.api.print_y = self.api.prnt_y

        self.namespace = namespace
        self.name = os.path.splitext(os.path.basename(self.namespace['__file__']))[0]
        self.registration = ScriptRegistration(
            self.name,
            getattr(self, 'AUTHOR', 'anonymous <devnull@example.com>'),
            getattr(self, 'VERSION', '0.0.0'),
            getattr(self, 'LICENSE', 'N/A'),
            self.__class__.__doc__.split('.')[0].strip(),
            self.callback('on_unload'),
            getattr(self, 'CHARSET', ''), # default is UTF-8
        )


    def callback(self, func, name=None):
        """ Return a callback name for the given method name or callable in `func`.

            Note that you'll cause a memory leak of you call this repeatedly
            with ever-changing callables (like lambdas). Pass a unique id
            in `name` in such cases.
        """
        try:
            func + ''
        except TypeError:
            func_obj = func # assume a callable
        else:
            func_obj = getattr(self, func)

        cb_name = ['cb', self.name]
        try:
            cb_name.append(func_obj.__name__)
        except AttributeError:
            pass
        cb_name.append(name or str(id(func_obj)))

        func_name = '__'.join(cb_name)
        self.namespace.setdefault(func_name, func_obj)

        return func_name


    def log(self, msg, *args, **kwargs):
        """ Write an informational or error message to the core buffer.

            The keyword argument `prefix` can be 'error' and other values as listed at
            http://weechat.org/files/doc/stable/weechat_plugin_api.en.html#_weechat_prefix
            in the API reference.
        """
        self.api.print_('', '{0}{1}: {2}'.format(
            self.api.prefix(kwargs.get('prefix', 'default')), self.registration.name, msg.format(*args, **kwargs)
        ))


    def on_load(self):
        """ Template method called after registration.
        """
        weechat_version = self.api.info_get('version', '') or 'N/A'
        self.log('loaded shim {1} into WeeChat version {0}', weechat_version, self.namespace['__file__'], prefix='join')

        return self.api.WEECHAT_RC_OK


    def on_unload(self):
        """ Template method called during unload.
        """
        self.log('unloading WeePlug script "{0}"', self.registration.name, prefix='quit')

        return self.api.WEECHAT_RC_OK


class WeePlugScriptBase(ScriptBase):
    """ Base class for built-in WeePlug scripts.
    """

    def __init__(self, namespace, **kwargs):
        """ Initialize script object.
        """
        import weeplug

        self.AUTHOR = '{0} <{1}>'.format(weeplug.__author__, weeplug.__author_email__)
        self.VERSION = weeplug.__version__
        self.LICENSE = weeplug.__license__

        super(WeePlugScriptBase, self).__init__(namespace, **kwargs)
