# Just Open

Simple, configurable script to open files.

One can just give any file as a parameter, and it's then opened in the
preferred application.
It's configurable, so one can define their favourite apps,
and just open the files like they want.

## Requirements

- Python 3.x

Other Python versions might work, but are unsupported.

## Configuration file

The configuration file should be stored as:

    ~/.just-open.json

As the extension says, it's just plain JSON file. It should be formatted as:

    {
        "runners": {
        },
        "extmap": {
        }
    }

Those two sections should contain specific mappings, see definitions below or
see [just-open.sample.json](just-open.sample.json) for example.

### Runners

First "runners" should have mimetypes mapped for application or command.
The mimetype should be JSON string just like "text/plain".
Command should be string or list. For example:

    "runners": {
        "text/plain": "vim",
        "inode/directory": ["ls", "-la", "--color=tty"],
    }

This would mean that all files detected as "text/plain" are opened with "vim",
so that command would be:

    vim filename

Then all files that are detected to be "inode/directory" are opened as:

    ls -la --color=tty filename

In case the filename should not be the last, use "$F" which is expaned to be
the filename:

    "runners": {
        "inode/directory": ["find", "$F", "-type", "f"],
    }

Becomes:

    find filename -type f


### Extmap

Extmap maps simply extension to a mime type. This is simple string to string
mapping.  Extensions are split on every dot, and all possibilities are tried,
thus test.tar.gz will be tested first for "tar.gz" and then for "gz".

If there's a match in "extmap", the matchin mimetype is used.  After that
the mimetype is searched from the "runners" list. If there's no specification
for it, fallback method is used to open the file.

### Fallback

Fallback method for now is "xdg-open" which should utilize proper system
configuration to open the file. This behaves similarly than clicking the file
in (graphical) file browser. For non-graphicals enviroment this might not work
and the method fails.

## Installation

To install it to you $HOME/bin just do:

    make install

In order to install it under another folder, like /usr/local/bin:

    make install DESTDIR=/usr/local
