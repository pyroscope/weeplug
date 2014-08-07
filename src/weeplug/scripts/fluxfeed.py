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

import re
import time

try:
    import json
except ImportError:
    import simplejson as json

import requests
from requests.exceptions import RequestException
from pyrobase.parts import Bunch

from weeplug import events
from weeplug.support import BuiltinsScriptBase


class FluxFeedScript(BuiltinsScriptBase):
    """ Scan channels for events and feed them into an InfluxDB time series.

        Pushes fields to a given timeseries, extracted via a regex trigger that matches a line.

        For tracing, use
            /set plugins.var.python.fluxfeed.trace on
    """
    SETTINGS = dict(
        influxdb_url = ('http://localhost:8086/', 'Base URL of the InfluxDB REST API'),
        influxdb_user = ('root', 'Account used for pushing data'),
        influxdb_password = ('root', 'Credentials used for pushing data'),
        triggers = ('', 'Trigger definitions of the form'
            ' [«nick»@]«server».#«channel»/«regex with named groups»/[i]->«dbname».«series»[+«sysattr»...]'),
        dry_run = ('off', 'Only log data, instead of pushing it'),
    )
    PRINT_HOOKS = dict(scanner=None)

    TRIGGER_RE = re.compile((
        r'(?:(?P<nick>[^@]+)@)?'
        r'(?P<buffer_name>[^{delims}]+?)'
        r'(?P<delim>[{delims}])(?P<regex>.+?)(?P=delim)(?P<flags>i)?'
        r'->(?P<dbname>[^.]+)\.(?P<series>[^+]+)'
        r'(?P<sysattr>(?:\+[^+]+)*)').format(delims="/~%"))


    def _parse_triggers(self):
        """ Parse trigger definitions from config.
        """
        # TODO: Load triggers from their own file (INI or YAML), and watch it with a timer?!
        self.triggers = []
        for trigger in (self.api.config_get_plugin("triggers") or '').split():
            parts = self.TRIGGER_RE.match(trigger)
            if parts:
                triggerdef = Bunch(nick=None, flags='', sysattr='')
                triggerdef.update(parts.groupdict())
                triggerdef.sysattr = set(triggerdef.sysattr.strip('+').split('+'))
                try:
                    triggerdef.regex = re.compile(triggerdef.regex, re.I if 'i' in triggerdef.flags else 0)
                except re.error, exc:
                    self.log('Ignoring trigger with malformed regex ({1}): {0}', trigger, exc, prefix='warn')
                else:
                    self.triggers.append(triggerdef)
                    self.trace("trigger#{0} = {1} ", len(self.triggers), triggerdef)
            else:
                self.log('Ignoring malformed trigger: {0}', trigger, prefix='warn')


    def _influxdb_url(self, dbname):
        """ Return REST API URL to access time series on the given DB.
        """
        url = "{0}/db/{1}/series?time_precision=u".format(self.api.config_get_plugin("influxdb_url").rstrip('/'), dbname)

        user = self.api.config_get_plugin("influxdb_user")
        password = self.api.config_get_plugin("influxdb_password")
        if user and password:
            url += "&u={0}&p={1}".format(user, password)

        return url


    def _push_event(self, ev, trigger, match):
        """ Push an event to InfluxDB.
        """
        data = dict(source=ev.buffer.name, prefix=ev.prefix, timestamp=ev.timestamp)
        data = dict((k, v) for k, v in data.iteritems() if k in trigger.sysattr)
        data.update(match.groupdict())

        if self.is_true('dry_run'):
            self.log("scanner: match {0}", data)
        else:
            fluxurl = self._influxdb_url(trigger.dbname)
            fluxdata = json.dumps([dict(
                time = int(time.time() * 1000000), # works in Linux, good enough for me
                name = trigger.series,
                columns = data.keys(),
                points = [data.values()]
            )])
            self.trace("POST to {0} with {1}", fluxurl.split('?')[0], fluxdata)

            try:
                # TODO: Possibly needs to be in a thread, as to not block WeeChat; but will do for now
                requests.post(fluxurl, data=fluxdata, timeout=0.010)
            except RequestException, exc:
                self.log("InfluxDB POST error: {0}", exc, prefix='error')


    def scanner(self, *args):
        """ Look out for events that a trigger matches.
        """
        ev = events.PrintEvent(self, args)
        mynick = ev.buffer.irc_nick
        if not mynick or 'nick_' + mynick in ev.tags:
            # Always ignore non-IRC and own text, to avoid endless loops
            ##self.trace('scanner: Ignored {0}', ev)
            return self.api.WEECHAT_RC_OK

        self.trace('scanner[{1}]: {0}', ev, mynick)

        for trigger in self.triggers:
            if trigger.buffer_name == ev.buffer.name and (not trigger.nick or 'nick_' + trigger.nick in ev.tags):
                match = trigger.regex.search(ev.message)
                if match:
                    self._push_event(ev, trigger, match)

        return self.api.WEECHAT_RC_OK


    def on_load(self):
        """ Load configuration.
        """
        rc = super(FluxFeedScript, self).on_load()
        if rc != self.api.WEECHAT_RC_OK:
            return rc

        # TODO: reload on config changes
        self._parse_triggers()

        return self.api.WEECHAT_RC_OK
