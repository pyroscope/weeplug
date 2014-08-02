# -*- coding: utf-8 -*-
#
# Script loader shim
#
import os
import sys

try:
    import weechat
except ImportError, exc:
    raise RuntimeError("This script must be run under WeeChat - get it at http://www.weechat.org/ ({0})".format(exc))

# Activate the virtualenv (once)
if not any('/.weechat/venv/' in i for i in sys.path):
    venv_activate = os.path.expanduser('~/.weechat/venv/bin/activate_this.py')
    execfile(venv_activate, dict(__file__=venv_activate))

try:
    import weeplug
except ImportError, exc:
    raise RuntimeError("Package 'weeplug' not found,"
        " did you read 'https://github.com/pyroscope/weeplug#installation'? ({0})".format(exc))

if __name__ == "__main__":
    weeplug.load_script(__file__, globals())
