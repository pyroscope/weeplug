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


def load_script(shimfile, namespace):
    """ Load a script from a shim file.
    """
    import weechat
    import weeplug

    registration = ScriptRegistration(
        os.path.splitext(os.path.basename(shimfile))[0],
        "{0} <{1}>".format(weeplug.__author__, weeplug.__author_email__),
        weeplug.__version__,
        weeplug.__license__,
        weeplug.__doc__.split('.')[0].strip(), # TODO: Use script class docstring
        '', # name of function called when script is unloaded (can be empty string)
        '', # default is UTF-8
    )
    if not weechat.register(*registration):
        return

    def error(msg, *args, **kwargs):
        "helper"
        weechat.prnt("", "{0}{1}: {2}".format(weechat.prefix("error"), registration.name, msg.format(*args, **kwargs)))

    version = int(weechat.info_get("version_number", "") or 0)
    if version < 0x00030700:
        error("need WeeChat version 0.3.7 or higher")
        weechat.command("", "/wait 1ms /python unload {0}".format(registration.name))
    else:
        error("version={0} shim={1}", hex(version), namespace['__file__'])
