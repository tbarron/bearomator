import json
import os
import re
import tbx
from bear import verinfo

"""
a - entry added
b - doc copied
c - doc formatted
d - function written
e - function tested

/add-file         a b c d
/add-text         a b c d e
/archive          a b c d
/change-font      + + + +
/change-theme     + + + +
/create           + + + + +
/delete-tag       + + + +
/grab-url         + + +
/open-note        + + + +
/open-tag         a b c d e
/rename-tag       a b c d
/search           + + + +
/tags             + + + +
/today            + + +
/todo             + + +
/trash            + + + +
/untagged         + + +
"""


def version():
    """
    Return version info at the module level
    """
    return verinfo._v


class Bear(object):
    """
    This object provides an interface to the bear app through the program xcall
    (https://github.com/martinfinke/xcall).

    A hook is defined for each of the Bear entrypoints described at

        https://bear.app/faq/X-callback-url%20Scheme%20documentation/

    as of 2019-01-09.
    """

    # -------------------------------------------------------------------------
    def __init__(self):
        """
        Initialize the object
        """
        pass

    # -------------------------------------------------------------------------
    def add_file(self, id=None, title=None, content=None, header=None,
                 filename=None, mode=None):
        """
        /add-file
            append or prepend a file to a note identified by its title or id.

        parameters
            id (optional): note unique identifier.
            title (optional): note title.
            file (required): base64 representation of a file.
            header (optional): if specified add the file to the corresponding
                header inside the note.
            filename (required): file name with extension. Both file and
                filename are required to successfully add a file.
            mode (optional): the allowed values are prepend, append,
                replace_all and replace (keep the note's title untouched).
            open_note (optional): if no do not display the new note in Bear's
                main or external window.
            new_window (optional): if yes open the note in an external window
                (MacOS only).
            show_window (optional): if no the call don't force the opening of
                bear main window (MacOS only).
            edit (optional): if yes place the cursor inside the note editor.

        x-success
            note: note text

        example
            bear://x-callback-url/add-file?filename=test.gif
                &id=4EDAF0D1-2EFF-4190-BC1D-67D9BAE49BA9-28433-000187BAA3D182EF
                &mode=append
                &file=R0lGODlhAQABAIAAAP%2F%2F%2F%2F%2F%2F%2FyH5BAEKAAEAL
                      AAAAAABAAEAAAICTAEAOw%3D%3D

        notes
            The base64 file parameter has to be encoded when passed as an url
            parameter.
        """
        if content is None:
            raise Bearror("add_file requires content argument")
        if filename is None:
            raise Bearror("add_file requires filename argument")

        kw = {}
        # args = {'note_id': 'id',
        #         'title': 'title',
        #         'content': 'file',
        #         'header': 'header',
        #         'filename': 'filename',
        #         'mode': 'mode'}
        # locals = local()
        # for item in args:
        #     if item in locals:
        #         kw[item] = locals[item]

        if id:
            kw['id'] = id
        if title:
            kw['title'] = title
        if content:
            kw['file'] = content
        if header:
            kw['header'] = header
        if filename:
            kw['filename'] = filename
        if mode:
            kw['mode'] = mode
        kw['open_note'] = "no"
        kw['show_window'] = "no"

        result = self._url_xcall('add-file', **kw)
        return result

    # -------------------------------------------------------------------------
    def add_text(self, id=None, title=None, text=None, mode=None, tags=None):
        """
        /add-text
            append or prepend text to a note identified by its title or id.

        parameters
            id (optional): note unique identifier.
            title (optional): title of the note.
            text: (required) text to add.
            header: (optional) if specified add the text to the corresponding
                header inside the note.
            mode: (optional) the allowed values are prepend, append,
                replace_all and replace (keep the note's title untouched).
            tags: (optional) a comma separated list of tags.
            exclude_trashed: (optional) if yes exclude trashed notes.
            open_note: (optional) if no do not display the new note in Bear's
                main or external window.
            new_window: (optional) if yes open the note in an external window
                (MacOS only).
            show_window: (optional) if no the call don't force the opening of
                bear main window (MacOS only).
            edit: (optional) if yes place the cursor inside the note editor.
            timestamp: (optional) if yes prepend the current date and time to
                the text

        x-success
            note: note text.
            title: note title.

        example
            bear://x-callback-url/add-text?text=new%20line&id=4EDAF0D1&
                mode=append
        """
        if text is None:
            raise Bearror("add_text requires argument text")
        if id is None and title is None:
            raise Bearror("either id or title is required")
        if mode not in ["prepend", "append", "replace", "replace_all"]:
            raise Bearror("mode must be 'prepend', 'append', 'replace', or "
                          "'replace_all'")

        kw = {}
        kw['text'] = text
        if id:
            kw['id'] = id
        if title:
            kw['title'] = title
        if mode:
            kw['mode'] = mode
        if tags:
            kw['tags'] = tags
        kw['exclude_trashed'] = 'yes'
        kw['open_note'] = 'no'
        kw['new_window'] = 'no'
        kw['show_window'] = 'no'

        result = self._url_xcall('add-text', **kw)
        return result

    # -------------------------------------------------------------------------
    def archive(self, id=None, search=None):
        """
        /archive
            Move a note to bear archive and select the Archive sidebar item.

        parameters
            id (optional): note unique identifier.
            search (optional): string to search.
            show_window (optional): if 'no' the call don't force the opening of
                bear main window (MacOS only).

        example
            bear://x-callback-url/archive?id=7E4B681B
            bear://x-callback-url/archive?search=projects

        notes
            The search term is ignored if an id is provided
        """
        if id is None and search is None:
            raise Bearror("Without id or search, there's nothing to do")

        kw = {'show_window': "no"}
        if id:
            kw['id'] = id
        if search:
            kw['search'] = search

        result = self._url_xcall('archive', **kw)
        return result

    # -------------------------------------------------------------------------
    def change_font(self, font):
        """
        /change-font
            Change the selected Bear Font.

        parameters
            font (required).
            show_window (optional): if no the call don't force the opening of
                bear main window (MacOS only).

        available values
            Avenir Next           System         Helvetica Neue
            Menlo                 Georgia        Courier
            Open Dyslexic

        example
            bear://x-callback-url/change-font?font=Helvetica%20Neue
        """
        if font not in ["Avenir Next", "System", "Helvetica Neue",
                        "Menlo", "Georgia", "Courier", "Open Dyslexic"]:
            raise Bearror("Font '{}' is not supported".format(font))
        result = self._url_xcall('change-font', font=self._url_quote(font))
        return result

    # -------------------------------------------------------------------------
    def change_theme(self, theme):
        """
        /change-theme
            Change the selected Bear theme. Some themes may require a Bear Pro
                subscription.

        parameters
            theme (required).
            show_window optional if no the call don't force the opening of bear
                main window (MacOS only).

        available values
            Red Graphite     Charcoal         Solarized Light    Solarized Dark
            Panic Mode       Dracula          Gotham             Toothpaste
            Cobalt           Duotone Light    Duotone Snow       Dieci
            Ayu              Dark Graphite    Duotone Heat

        example
            bear://x-callback-url/change-theme?theme=Solarized%20Dark
        """
        if theme not in ["Red Graphite", "Charcoal", "Solarized Light",
                         "Solarized Dark", "Panic Mode", "Dracula",
                         "Gotham", "Toothpaste", "Cobalt", "Duotone Light",
                         "Duotone Snow", "Dieci", "Ayu", "Dark Graphite",
                         "Duotone Heat"]:
            raise Bearror("Theme '{}' is not supported".format(theme))
        result = self._url_xcall('change-theme', theme=self._url_quote(theme))
        return result

    # -------------------------------------------------------------------------
    def create(self, title=None, text=None, tags=None, file=None,
               filename=None, pin=None, timestamp=None,
               open_note=None, new_window=None):
        """
        /create
            Create a new note and return its unique identifier. Empty notes are
            not allowed.

        parameters
            title (optional): note title.
            text (optional): note body.
            tags (optional): a comma separated list of tags.
            file (optional): base64 representation of a file.
            filename (optional): file name with extension. Both file and
                filename are required to successfully add a file.
            open_note (optional): if no do not display the new note in Bear's
                main or external window.
            new_window (optional): if yes open the note in an external window
                (MacOS only).
            show_window (optional): if no the call don't force the opening of
                bear main window (MacOS only).
            pin (optional): if yes pin the note to the top of the list.
            edit (optional): if yes place the cursor inside the note editor.
            timestamp (optional): if yes prepend the current date and time to
                the text

        x-success
            identifier: note unique identifier.
            title: note title.

        example
            bear://x-callback-url/create?title=My%20Note%20Title
                &text=First%20line
                &tags=home,home%2Fgroceries

        notes
            The base64 file parameter have to be encoded when passed as an url
            parameter.
        """
        kw = {'open_note': 'no', 'show_window': 'no'}
        if title:
            kw['title'] = title
        if text:
            kw['text'] = text
        if tags:
            kw['tags'] = tags
        if file:
            kw['file'] = file
        if filename:
            kw['filename'] = filename
        if pin:
            kw['pin'] = pin
        if timestamp:
            kw['timestamp'] = timestamp
        if open_note:
            kw['open_note'] = open_note
        if new_window:
            kw['new_window'] = new_window

        result = self._url_xcall('create', **kw)
        return result

    # -------------------------------------------------------------------------
    def delete_tag(self, name=None):
        """
        /delete-tag
            Delete an existing tag.

        parameters
            name (required): tag name.
            show_window (optional): if no the call don't force the opening of
                bear main window (MacOS only).

        example
            bear://x-callback-url/delete-tag?name=todo
        """
        if name is None:
            raise Bearror("(tag) name is required")

        result = self._url_xcall('delete-tag', name=name, show_window="no")
        return result

    # -------------------------------------------------------------------------
    def grab_url(self, url, tags=None, pin=None, wait=None):
        """
        /grab-url
            Create a new note with the content of a web page.

        parameters
            url (required): url to grab.
            images (optional): grab or not the page images.
            tags (optional): a comma separated list of tags.
            pin (optional): if yes pin the note to the top of the list.

            wait (optional): if no, x-success is immediately called without
                identifier and title.

        x-success
            identifier: note unique identifier.
            title: note title.

        available values
            yes no

        example
            bear://x-callback-url/grab-url?url=https://bear.app
        """
        pass

    # -------------------------------------------------------------------------
    def has_tag(self, id, tag):
        """
        Open the note and check for the tag. If it is present, return True.
        Otherwise, return False.
        """
        if tag[0] != "#":
            tag = "#" + tag
        content = self.open_note(id=id)
        return tag in content["note"]

    # -------------------------------------------------------------------------
    def idemp_add(self, id=None, tag=None):
        """
        Open the note and check for the tag. If it is present, do nothing and
        return False. Otherwise, add the tag to the note and return True.
        """
        rval = False
        if tag is None or id is None:
            return rval
        t_hash = "#"
        content = self.open_note(id=id)
        if t_hash + tag not in content["note"]:
            rval = True
            self.add_text(id=id, text="", tags=tag, mode="append")
        return rval

    # -------------------------------------------------------------------------
    def open_note(self, id=None, title=None, new_window=None, show_window=None,
                  exclude_trashed=None):
        """
        /open-note
            Open a note identified by its title or id and return its content.

        parameters
            id (optional): note unique identifier.
            title (optional): note title.
            header (optional): an header inside the note.
            exclude_trashed (optional): if yes exclude trashed notes.
            new_window (optional): if yes open the note in an external window
                (MacOS only).
            float (optional): if yes makes the external window float on top
                (MacOS only).
            show_window (optional): if no the call don't force the opening of
                bear main window (MacOS only).
            edit optional if yes place the cursor inside the note editor.

        x-success
            note: note text.
            identifier: note unique identifier.
            title: note title.
            is_trashed: yes if the note is trashed.
            modificationDate: note modification date in ISO 8601 format.
            creationDate: note creation date in ISO 8601 format.

        example
            bear://x-callback-url/open-note?id=7E4B681B
            bear://x-callback-url/open-note?id=7E4B681B
                &header=Secondary%20Ttitle
        """
        if id is None and title is None:
            raise Bearror("either id or title is required")

        kw = {}
        if id:
            kw['id'] = id
        if title:
            kw['title'] = title

        kw['exclude_trashed'] = "yes"
        if exclude_trashed:
            kw['exclude_trashed'] = exclude_trashed

        kw['show_window'] = "no"
        if show_window:
            kw['show_window'] = show_window

        if new_window:
            kw['new_window'] = new_window

        result = self._url_xcall('open-note', **kw)
        return result

    # -------------------------------------------------------------------------
    def open_tag(self, name):
        """
        /open-tag
            Get a list of all the notes which have a selected tag in bear.

        parameters
            name (required): tag name.
            token (optional): application token.

        x-success
            notes: json array representing the tag's notes.
                [{ title, identifier, modificationDate, creationDate, pin },
                ...]

            If token is not provided nothing is returned.

        example
            bear://x-callback-url/open-tag?name=work
            bear://x-callback-url/open-tag?name=todo%2Fwork

        Notes
         * exclude_trashed does not work for open_tag, though it does not cause
           the API function to fail
        """
        try:
            result = self._url_xcall('open-tag',
                                     name=name,
                                     token=self._token())
        except Bearror as err:
            if "The tag could not be found" in str(err):
                raise Bearror("Tag '{}' was not found".format(name))
        return result

    # -------------------------------------------------------------------------
    def raw_url(self, url):
        """
        process a raw url
        """
        result = self._xcall(url)
        return result

    # -------------------------------------------------------------------------
    def rename_tag(self, old, new):
        """
        /rename-tag
            Rename an existing tag.

        parameters
            name (required): tag name.
            new_name (required): new tag name.
            show_window (optional): if no the call don't force the opening of
                bear main window (MacOS only).

        example
            bear://x-callback-url/rename-tag?name=todo&new_name=done
        """
        result = self._url_xcall('rename-tag', name=old, new_name=new,
                                 show_window='no')
        return result

    # -------------------------------------------------------------------------
    def search(self, term=None, tag=None, show_window=None):
        """
        /search
            Show search results in Bear for all notes or for a specific tag.

        parameters
            term (optional): string to search.
            tag (optional): tag to search into.
            show_window (optional): if no the call don't force the opening of
                bear main window (MacOS only).
            token (optional): application token.

        x-success
            notes: json array representing the note results of the search.
                [{title, identifier, modificationDate, creationDate, pin },
                 ...]

            If token is not provided nothing is returned.

        example
            bear://x-callback-url/search?term=nemo&tag=movies
        """
        kw = {}
        if term:
            kw['term'] = term
        if tag:
            kw['tag'] = tag
        if show_window:
            kw['show_window'] = show_window
        else:
            kw['show_window'] = "no"
        kw['token'] = self._token()
        result = self._url_xcall('search', **kw)
        return result

    # -------------------------------------------------------------------------
    def tags(self):
        """
        /tags
            Return all the tags currently displayed in Bear's sidebar.

        parameters
            token (required): application token.

        x-success
            tags: json array representing tags. [{ name }, ...]

        example
            bear://x-callback-url/tags?token=123456-123456-123456
        """
        result = self._url_xcall('tags', token=self._token())
        tags_l = [_['name'] for _ in result]
        return tags_l

    # -------------------------------------------------------------------------
    def today(self, search=None):
        """
        /today
            Select the Today sidebar item.

        parameters
            search (optional): string to search.
            show_window (optional): if no the call don't force the opening of
                bear main window (MacOS only).
            token (optional): application token.

        x-success
            notes: json array representing the today notes.
            [{ title, identifier, modificationDate, creationDate, pin },
             ...]

            If token is not provided nothing is returned.

        example
            bear://x-callback-url/today?search=family
        """
        pass

    # -------------------------------------------------------------------------
    def todo(self, search=None):
        """
        /todo
            Select the Todo sidebar item.

        parameters
            search (optional): string to search.
            show_window (optional): if no the call don't force the opening of
                bear main window (MacOS only).
            token (optional): application token.

        x-success
            notes: json array representing the todo notes.
            [{ title, identifier, modificationDate, creationDate, pin },
             ...]

            If token is not provided nothing is returned.

        example
            bear://x-callback-url/todo?search=home
        """
        pass

    # -------------------------------------------------------------------------
    def trash(self, id=None, search=None):
        """
        /trash
            Move a note to bear trash and select the Trash sidebar item.

        parameters
            id (optional): note unique identifier.
            search (optional): string to search. ignored if id present.
            show_window (optional): if no the call don't force the opening of
                bear main window (MacOS only).

        example
            bear://x-callback-url/trash?id=7E4B681B
            bear://x-callback-url/trash?search=old

        notes
            The search term is ignored if an id is provided.
        """
        if id is None and search is None:
            raise Bearror("Without id or search, there's nothing to do")

        kw = {'show_window': "no"}
        if id:
            kw['id'] = id
        if search:
            kw['search'] = search
        result = self._url_xcall('trash', **kw)
        return result

    # -------------------------------------------------------------------------
    def untagged(self, search=None):
        """
        /untagged
            Select the Untagged sidebar item.

        parameters
            search (optional): string to search.
            show_window (optional): if no the call don't force the opening of
                bear main window (MacOS only).
            token (optional): application token.

        x-success
            notes: json array representing the untagged notes.
            [{ title, identifier, modificationDate, creationDate, pin },
             ...]

            If token is not provided nothing is returned.

        example
            bear://x-callback-url/untagged?search=home
        """
        pass

    # -------------------------------------------------------------------------
    @classmethod
    def version(cls):
        """
        Return version info at the object instance level
        """
        return verinfo._v

    # -------------------------------------------------------------------------
    def _token(self):
        """
        Retrieve and cache the bear token
        """
        if not hasattr(self, 'token_value'):
            with open("token", 'r') as rbl:
                self.token_value = rbl.read().strip()
        rval = self.token_value
        return rval

    # -------------------------------------------------------------------------
    def _url_xcall(self, cmd, **kw):
        """
        Build the url and pass it to xcall
        """
        url = self._url(cmd, **kw)
        result = self._xcall(url)
        return result

    # -------------------------------------------------------------------------
    def _url(self, cmd, **kw):
        """
        Build a bear url
        """
        rval = "bear://x-callback-url/{}".format(cmd)
        sep = "?"
        for key in kw:
            rval += "{}{}={}".format(sep, key, self._url_quote(kw[key]))
            sep = "&"
        return rval

    # -------------------------------------------------------------------------
    def _url_quote(self, kv):
        """
        Encode *kv* so that it won't freqk out Bear's URL processor
        """
        hexf = "%{:02x}"

        # characters that have been tested and do not need url quoting (at
        # least for add_text): /, =, ', [, ], (, ), ., $, <comma>, *, -,
        #                      !, @, +, ?, ~
        clist = ["%", " ", "#", "\"", "\n", "\t", ">",
                 "<", "^", "&", "{", "}", "|", "\\", "`"]
        replables = {_: hexf.format(ord(_)) for _ in clist}
        for char in replables:
            if isinstance(kv, bytes):
                kv = kv.replace(char.encode(), replables[char].encode())
            else:
                kv = kv.replace(char, replables[char])
        return kv

    # -------------------------------------------------------------------------
    def _xcall(self, url):
        """
        Run xcall and pass it a url
        """
        result = tbx.run("{} -url \"{}\"".format(self._xcall_path(), url))
        if result == '':
            return result
        while type(result) == str:
            result = json.loads(result)
        if 'errorMessage' in result:
            msg = result['errorMessage']
            if 'tag' in msg:
                q = re.findall("tag=([^&]+)", url)
                if q:
                    tag = q[0]
                    msg = msg.replace('tag ', 'tag ' + tag + ' ')
            raise Bearror(msg)
        elif 'note' in result:
            pass
        elif '' in result.keys() and len(result) == 2:
            [other] = [_ for _ in result.keys() if _ != '']
            result = json.loads(result[other])
        return result

    # -------------------------------------------------------------------------
    def _xcall_path(self):
        """
        This method stores and provides the path to the xcall program
        """
        path = os.path.join("$HOME/prj/bear/ulysses-python-client/lib",
                            "xcall.app", "Contents", "MacOS", "xcall")
        return os.path.expandvars(path)


class Bearror(Exception):
    pass
