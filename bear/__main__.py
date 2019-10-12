"""
Usage:
    bear permit
    bear sample_url
    bear token
    bear tags [-d] [-v]
    bear rename-tag [-d] OLD NEW
    bear trash [-d] [-t TITLE | -i NOTE_ID]

Need to write:
    bear open-note
    bear create
    bear add-text
    bear add-file
    bear open-tag
    bear delete-tag
    bear trash
    bear archive
    bear untagged
    bear todo
    bear today
    bear search
    bear grab-url
    bear change-theme
    bear change-font

"""
from docopt_dispatch import dispatch

import json
import os
import pdb
import tbx


# -----------------------------------------------------------------------------
@dispatch.on('trash')
def bear_trash(**kw):
    """
    Trash the note(s) matched by kw['NOTE_ID'] or kw['TITLE']
    """
    if kw['d']:
        pdb.set_trace()
    if kw['TITLE']:
        print("title: {}".format(kw['TITLE']))
        url = bear_url('trash', term=kw['TITLE'])
        print(url)
        result = xcall(url)
        print(result)
    elif kw['NOTE_ID']:
        print("note id: {}".format(kw['NOTE_ID']))
        url = bear_url('trash', id=kw['NOTE_ID'], new_window="yes")
        print(url)
        result = xcall(url)
        print(result)
    else:
        print("-t TITLE or -i NOTE_ID is required")




# -----------------------------------------------------------------------------
@dispatch.on('rename-tag')
def bear_rename_tag(**kw):
    """
    Issue the 'rename-tag' command to bear and display the response
    """
    if kw['d']:
        pdb.set_trace()
    url = bear_url('rename-tag', name=kw['OLD'], new_name=kw['NEW'])
    xcall(url)


# -----------------------------------------------------------------------------
@dispatch.on('tags')
def bear_tags(**kw):
    """
    Issue the 'tags' command to bear and display the response
    """
    if kw['d']:
        pdb.set_trace()
    url = bear_url('tags', token=bear_token())
    json_r = xcall(url)
    tags = json.loads(json_r)
    tagl = json.loads(tags['tags'])
    if kw['v']:
        tagnames = [_['name'] for _ in tagl]
        maxl = max(len(_) for _ in tagnames)
        line = ""
        for tag in tagnames:
            line = "{}{:{width}s}".format(line, tag, width=maxl+1)
            if 65 < len(line):
                print(line)
                line = ""
        if line:
            print(line)

    print("{} tags found".format(len(tagl)))


# -----------------------------------------------------------------------------
def bear_url(cmd, **kw):
    """
    Build and return a bear url
    """
    rval = "bear://x-callback-url/"
    rval += cmd
    sep = "?"
    for key in kw:
        rval += "{}{}={}".format(sep, key, kw[key])
        sep = "&"
    return rval


# -----------------------------------------------------------------------------
@dispatch.on('permit')
def permit(**kw):
    """
    This must be run to allow xcall to run on MacOS
    """
    cmd = "xattr -dr com.apple.quarantine \"lib/xcall.app\""
    print(cmd)
    tbx.run(cmd)


# -----------------------------------------------------------------------------
@dispatch.on('token')
def showtok(**kw):
    """
    Just display our API token
    """
    print(bear_token())


# -----------------------------------------------------------------------------
@dispatch.on('sample_url')
def sample_url(**kw):
    """
    Build and show a bear url

    eg: bear://x-callback-url/tags?token=123456-123456-123456
    """
    scheme = "bear"
    protocol = "x-callback-url"
    cmd = "tags"
    arg = "token="
    rval = "{}://{}/{}/{}{}".format(scheme, protocol, cmd, arg, bear_token())
    print(rval)


# -----------------------------------------------------------------------------
def xcall(url):
    """
    Call program xcall with *url*
    """
    path = os.path.join("$HOME/prj/bear/ulysses-python-client/lib/xcall.app",
                        "Contents", "MacOS", "xcall")
    # path = os.path.join("$HOME/prj/bear/bear-python-client/lib/xcall.app",
    #                     "Contents", "MacOS", "xcall")
    path = os.path.expandvars(path)
    result = tbx.run("{} -url \"{}\"".format(path, url))
    return result


# -----------------------------------------------------------------------------
def bear_token():
    """
    This function holds our API token for bear
    """
    return "710124-D107AF-A0B87D"


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    dispatch(__doc__)
