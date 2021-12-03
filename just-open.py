#!/usr/bin/env python3

# Copyright 2021 Jouni Roivas
# MIT License, see LICENSE

import json
import os
import subprocess
import sys

# Reading config from ~/.just-open.json
# Can define default config here
runners = {
}

extmap = {
}


def expandFileName(name):
    name = os.path.expanduser(name)
    name = os.path.expandvars(name)
    return name


def loadConfig(conf, runners, extmap):
    try:
        with open(expandFileName(conf)) as fd:
            cfg = json.loads(fd.read())
        if cfg:
            runners.update(cfg.get('runners', {}))
            extmap.update(cfg.get('extmap', {}))
    except Exception as e:
        print(e)
        pass

    return runners, extmap


def runPipe(cmd):
    r = subprocess.run(cmd, stdout=subprocess.PIPE)
    if not r or r.returncode:
        return None
    return r.stdout


def iterExtensions(fname):
    """
    >>> list(iterExtensions("test.tar.gz"))
    ['tar.gz', 'gz']
    >>> list(iterExtensions("a.b.c.d.e"))
    ['b.c.d.e', 'c.d.e', 'd.e', 'e']
    >>> list(iterExtensions("a..b"))
    ['.b', 'b']
    >>> list(iterExtensions("a"))
    []
    >>>
    """
    parts = fname.split('.')
    partlen = len(parts)
    if not parts or partlen == 1:
        return None

    i = 1
    while i < partlen:
        yield '.'.join(parts[i:])
        i += 1
    return None


def detectExt(fname):
    for ext in iterExtensions(fname):
        mime = extmap.get(ext, None)
        if mime is not None:
            return mime

    return None


def detectFile(fname):
    piperes = runPipe(['file', '-i', fname])
    if piperes is None:
        return None

    file_info = str(piperes).split(':')
    if not file_info:
        return None

    file_mime = file_info[1].split(';')
    mime = None
    if file_mime:
        mime = file_mime[0].strip()
    if mime:
        return mime

    return None


"""
def detectFileType(fname):
    try:
        import filetype

        r = filetype.guess(fname)
        if not r:
            return None
        return r.mime
    except:
        return None
    """


def detect(fname):
    f = detectExt(fname)
    if f:
        return f

    # Can add alternative detection methods here
    # For example filetype module

    f = detectFile(fname)
    if f:
        return f

    return None


def getRunner(ftype):
    r = runners.get(ftype, None)
    if r:
        return r

    parts = ftype.split('/')
    if parts:
        ftype_wildcard = parts[0] + '/*'
        r = runners.get(ftype_wildcard, None)
        if r:
            return r

    # sys.stderr.write('ERROR: No runner specified for %s\n' % ftype)
    return None


def replaceFilename(s, fname):
    res = ''
    escape = False
    dollar = False
    replaced = False
    for i in s:
        if i == '\\':
            escape = True
        elif escape and i == '$':
            res += '$'
            escape = False
        elif not escape and i == '$':
            dollar = True
        elif dollar and i == 'F':
            replaced = True
            res += fname
            dollar = False
        elif dollar:
            res += '$' + i
            dollar = False
        else:
            res += i
            escape = False
    return res, replaced


def runnerAppendFilename(runner, fname):
    appended = False
    res = []
    if type(runner) != list:
        runner = [runner]

    for i in runner:
        if "$F" in i:
            name, replaced = replaceFilename(i, fname)
            res.append(name)
            if replaced:
                appended = True
        else:
            res.append(i)

    if not appended:
        res.append(fname)

    return res


def doRun(runner, fname):
    cmd = runnerAppendFilename(runner, fname)

    subprocess.run(cmd)


def fallbackRunner(fname):
    try:
        doRun('xdg-open', fname)
    except:  # noqa: E722
        sys.stderr.write('ERROR: Can\'t find runner for %s\n' % fname)


def openFile(fname):
    global runners, extmap

    fn = expandFileName(fname)

    ok = False
    ft = detect(fn)
    if ft:
        r = getRunner(ft)
        if r:
            doRun(r, fn)
            ok = True

    if not ok:
        fallbackRunner(fn)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Usage: %s file' % sys.argv[0])
        sys.exit(1)

    runners, extmap = loadConfig('~/.just-open.json', runners, extmap)
    i = 1
    largs = len(sys.argv)

    while i < largs:
        openFile(sys.argv[i])
        i += 1
