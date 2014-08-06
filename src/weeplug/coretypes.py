# -*- coding: utf-8 -*-
""" weeplug – Core WeeChat types.
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

class Buffer(object):
    """ A WeeChat buffer.
    """

    def __init__(self, script, bufptr):
        """Create a buffer from its pointer."""
        self._script = script
        self._bufptr = bufptr

    @property
    def number(self):
        """Number of this buffer."""
        return int(self._script.api.buffer_get_integer(self._bufptr, "number"))

    @property
    def name(self):
        """Name of this buffer (e.g. "server.#channel")."""
        return self._script.api.buffer_get_string(self._bufptr, "name")

    @property
    def short_name(self):
        """Short name of this buffer (e.g. "#channel")."""
        return self._script.api.buffer_get_string(self._bufptr, "short_name")

    @property
    def server(self):
        """Server moniker of this buffer (for IRC buffers)."""
        return self.name.rsplit('.', 1)[0]

    @property
    def irc_nick(self):
        """Own nick for this buffer (for IRC buffers)."""
        return self._script.api.info_get("irc_nick", self.server) or None


    def __repr__(self):
        """ Stringify this buffer.
        """
        return '<{0} #{1} "{2}">'.format(self.__class__.__name__, self.number, self.name)


    def print_(self, text):
        """Print given text to buffer."""
        if text.startswith('/'):
            text = ' ' + text
        self._script.api.command(self._bufptr, text)


    def command(self, cmd, *args):
        """Execute a command in this buffer."""
        self._script.api.command(self._bufptr, '/{0}{1}{2}'.format(
            cmd.lstrip('/'), ' ' if args else '', ' '.join(str(i) for i in args)
        ))

#
