# -*- coding: utf-8 -*-
""" weeplug – InfluxDB events feed.
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

from weeplug import events
from weeplug.support import WeePlugScriptBase


class FluxFeedScript(WeePlugScriptBase):
    """ Scan channels for events and feed them into an InfluxDB time series.

        For tracing, use
            /set plugins.var.python.fluxfeed.trace on
    """
    PRINT_HOOKS = dict(scanner=None)

    def scanner(self, *args):
        """ Scan text for event matches.

            ('cb__fluxfeed__scanner__39486640', '0x234eef0', 2L, 'freenode.#weeplug', '#weeplug',
             '1407345499', 'irc_privmsg,notify_message,nick_pyroscope,log1', True, False, '@pyroscope', 'test 123')
        """
        self.trace('scanner: {0}', events.PrintEvent(self, args))
        return self.api.WEECHAT_RC_OK
