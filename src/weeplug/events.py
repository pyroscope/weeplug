# -*- coding: utf-8 -*-
""" weeplug – Event classes.
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

import datetime

from weeplug import coretypes


class PrintEvent(object):
    """ A text message on a channel / buffer.
    """

    def __init__(self, script, args):
        """ Store `hook_print` callback arguments.

            ('cb__plugin__func__123456', '0x123456', 2L, 'freenode.#weeplug', '#weeplug',
             '1407345499', 'irc_privmsg,notify_message,nick_pyroscope,log1',
             True, False, '@pyroscope', 'test 123')
        """
        # Split args
        self.data, _buffer, _timestamp, self.tags, _displayed, _hilighted, self.prefix, self.message = args

        # Validate args
        self.buffer = coretypes.Buffer(script, _buffer)
        self.timestamp = int(_timestamp)
        self.tags = set(self.tags.split(','))
        self.displayed = bool(int(_displayed))
        self.hilighted = bool(int(_hilighted))


    @property
    def time_iso(self):
        """Return event's timestamp in ISO-8601 format."""
        return datetime.datetime.fromtimestamp(self.timestamp).isoformat(' ')


    def __repr__(self):
        """ Stringify this print event.
        """
        return ("<{_name} {_time} #{buffer.number} {buffer.name} prefix='{prefix}' message='{message}'"
            " {_displayed}{_hilighted} tags={tags}>".format(
                _name=self.__class__.__name__,
                _time=self.time_iso,
                _displayed="VISIBLE" if self.displayed else "HIDDEN",
                _hilighted=" HILITE" if self.hilighted else "",
                **vars(self)
        ))
