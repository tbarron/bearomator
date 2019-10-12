import bcal
from bear import Bear, Bearror
import pytest
import uuid


# -----------------------------------------------------------------------------
@pytest.fixture
def fx_diary_pg():
    """
    Create a function that will take arg *ov_date* (a dt obj) to determine
    whether to create a page for the test or not.
    """
    data = {'nid': None}

    def dp_setup(ov_date=None):
        if ov_date:
           data['nid'] = bcal.create_diary_page(ov_date)

    data['setup'] = dp_setup

    yield data

    cub = Bear()
    cub.trash(id=data['nid'])


# -----------------------------------------------------------------------------
@pytest.fixture
def tnt():
    """
    Create a note with defined content, yield to the test, then trash the note
    """
    tid = uuid.uuid4()
    data = {'title': "pytest tmpnote {}".format(str(tid)),
            'text': "Original text",
            'addtext': ("Added text ='>< # // \"foobar\"\n"
                        "* bullet line\n"
                        "- todo line\n"
                        "+ plus +\n"
                        ". period .\n"
                        ", comma ,\n"
                        "! bang !\n"
                        "? question mark ?\n"
                        "| pipe |\n"
                        "\\ backslash \\\n"
                        "tab\t\t\tline\n"
                        "` grave `\n"
                        "$ dollar line\n"
                        "@ at sign @\n"
                        "^ caret ^\n"
                        "& ampersand &\n"
                        ": colon line\n"
                        "% percent line %\n"
                        "~ tilde ~\n"
                        "{ curly brace }\n"
                        "( parenthesis line )\n"
                        "[ square bracket line ]"),
            'addtags': ["newtag1", "newtag2"],
            'cub': Bear(),
            'unique_tag': tid.hex,
            'tags': "pytest,tmpnote,testing," + tid.hex}

    result = data["cub"].create(title=data['title'],
                                text=data['text'],
                                tags=data['tags'])
    note = data["cub"].open_note(id=result['identifier'], show_window="no")
    data['id'] = result['identifier']
    data['pre'] = note['note']
    (data['hdr'], data['body']) = note['note'].split("\n", 1)
    yield data
    data["cub"].trash(id=data['id'])
