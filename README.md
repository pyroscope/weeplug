# weeplug

A collection of WeeChat Python scripts.

To make writing these scripts easier, `weeplug` provides the plumbing and helpers to
write them in an object-oriented style, and hides the gory (C) details of the Python plugin
as far as possible, like manual memory management and so-called ‘pointers’.
`weeplug` also makes it easy to use a Python virtualenv,
to provide your WeeChat scripts with external dependencies.


## Installation

`weeplug` is a normal Python package and uses a standard Python project layout. The package is
installed into a *virtualenv* dedicated to WeeChat, and then shoehorned into the Python plugin's
loading mechanism by means of a shim file.

```sh
/usr/bin/virtualenv ~/.weechat/venv
~/.weechat/venv/bin/pip install -e "git+https://github.com/pyroscope/weeplug.git#egg=weeplug"
```

To directly use the code from a git working directory at another location, additionally call this command:

```sh
~/.weechat/venv/bin/python ./setup.py develop -U
```

**TODO** add `weeplug link` helper command to do this

Finally, to make the `weeplug` scripts available within your WeeChat configuration, symlink the `shim.py` file
to the default script location for each script.

```sh
weeplug_base="$(dirname $(~/.weechat/venv/bin/python -c 'import weeplug; print weeplug.__file__'))"
for script in "$weeplug_base/scripts"/[^_]*.py; do
    ln -nfs "$weeplug_base/data/shim.py" ~/.weechat/python/"$(basename $script)"
done
```


## Usage

### 'fluxfeed' Script

**TODO**


## References

 * [WeeChat Homepage](http://weechat.org/)
 * [WeeChat Scripting Guide](http://weechat.org/files/doc/devel/weechat_scripting.en.html)
 * [WeeChat Plugin API Reference](http://weechat.org/files/doc/devel/weechat_plugin_api.en.html)
 * [WeeChat Scripts Repository](http://weechat.org/scripts/)
 * [Arch Linux Wiki](https://wiki.archlinux.org/index.php/WeeChat)


## Related Projects

**GitHub**

 * [WeeChat](https://github.com/weechat/weechat)
 * [Official Scripts for WeeChat](https://github.com/weechat/scripts)
 * [jnbek's WeeChat Configs & Scripts](https://github.com/jnbek/_weechat)
 * [Nils Görs' Scripts](https://github.com/weechatter/weechat-scripts)
