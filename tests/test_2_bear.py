"""
Questions

 - In add_text(), either id or title can be used to identify the note being
   updated. If both are provided, which takes precedence? If a title matches
   multiple notes, do they all get updated?

 - Can we open a note by id that has been archived?
   >> yes, but there's no indication that it's in the archive. Notes do have an
      'is_trashed' attribute

 - Can we open a note by id that has been trashed?
   >> yes, but arg 'exclude_trash' must be passed as 'no'
"""
import base64
from bear import Bear, Bearror
from bear.util import comma
from fixtures import tnt                                           # noqa: F401
import pytest
import random
import string
import uuid


bt_text = ("Bibbedy bobbedy boo\n"
           "Fribble frooble\n"
           "Whippety whoppety\n")
bt_tags = "beartest, deleteme, froofroo"


# -----------------------------------------------------------------------------
def beartest_title():
    return "BearTest note " + str(uuid.uuid4())


# -----------------------------------------------------------------------------
def test_rename_tag():
    """
    Test for bear.rename_tag(). Use fixture tnt.
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_add_file():
    """
    Test bear.create() with file and filename arguments. Use fixture tnt.
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_create_file():
    """
    Test bear.create() with file and filename arguments
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_delete_tag():
    """
    Test bear.delete_tag(). Use fixture tnt.
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_grab_url():
    """
    Test bear.grab_url(url)
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_search():
    """
    Test bear.search([term], [tag])
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_tags():
    """
    Test bear.tags()
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_today():
    """
    Test bear.today()
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_todo():
    """
    Test bear.todo()
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_untagged():
    """
    Test bear.untagged()
    """
    pytest.skip('construction')


# -----------------------------------------------------------------------------
def test_instantiate():
    """
    Make sure pytest is working
    """
    pytest.dbgfunc()
    cub = Bear()
    assert 'open_note' in dir(cub)


# -----------------------------------------------------------------------------
def test_add_text_bt_x_app(tnt):                                   # noqa: F811
    """
    select by title, append text
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(title=tnt["title"], mode="append",
                               text=tnt["addtext"])
    assert tnt["addtext"] not in tnt["pre"]
    assert "\n".join([tnt["hdr"], tnt["body"], tnt["addtext"]]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bt_x_pre(tnt):                                   # noqa: F811
    """
    select by title, prepend text
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(title=tnt["title"], mode="prepend",
                               text=tnt["addtext"])
    assert tnt["addtext"] not in tnt["pre"]
    assert tnt["addtext"] in post["note"]
    assert "\n".join([tnt["hdr"], tnt["addtext"], tnt["body"]]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bt_x_rep(tnt):                                   # noqa: F811
    """
    select by title, replace body
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(title=tnt["title"], mode="replace",
                               text=tnt["addtext"])
    assert tnt["addtext"] not in tnt["pre"]
    assert tnt["addtext"] in post["note"]
    assert tnt["body"] not in post["note"]
    assert tnt["hdr"] in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bt_x_ral(tnt):                                   # noqa: F811
    """
    select by title, replace all text including header
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(title=tnt["title"], mode="replace_all",
                               text=tnt["addtext"])
    assert tnt["addtext"] not in tnt["pre"]
    assert tnt["addtext"] in post["note"]
    assert tnt["body"] not in post["note"]
    assert tnt["hdr"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bt_g_app(tnt):                                   # noqa: F811
    """
    select by title, append tags
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(title=tnt["title"], mode="append",
                               text="", tags=comma(tnt["addtags"]))
    for tag in tnt["addtags"]:
        assert tag not in tnt["pre"]
        assert tag in post["note"]
    assert "\n".join([tnt["hdr"],
                      tnt["body"],
                      hashed(tnt["addtags"])]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bt_g_pre(tnt):                                   # noqa: F811
    """
    select by title, prepend tags
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(title=tnt["title"], mode="prepend",
                               text="", tags=comma(tnt["addtags"]))
    for tag in tnt["addtags"]:
        assert tag not in tnt["pre"]
        assert tag in post["note"]
    assert "\n".join([tnt["hdr"],
                      hashed(tnt["addtags"]),
                      tnt["body"]]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bt_g_rep(tnt):                                   # noqa: F811
    """
    select by title, replace body with tags
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(title=tnt['title'], mode="replace",
                               text="", tags=comma(tnt["addtags"]))
    for tag in tnt["addtags"]:
        assert tag not in tnt["pre"]
        assert tag in post["note"]
    assert "\n".join([tnt["hdr"], hashed(tnt["addtags"])]) in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bt_g_ral(tnt):                                   # noqa: F811
    """
    select by title, replace header and body with tags
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(title=tnt['title'], mode="replace_all",
                               text="", tags=comma(tnt["addtags"]))
    for tag in tnt["addtags"]:
        assert tag not in tnt["pre"]
        assert tag in post["note"]
    assert hashed(tnt["addtags"]) in post["note"]
    assert tnt["hdr"] not in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bi_x_app(tnt):                                   # noqa: F811
    """
    select by id, append text
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], mode="append",
                               text=tnt["addtext"])
    assert tnt["addtext"] not in tnt["pre"]
    assert "\n".join([tnt["hdr"], tnt["body"], tnt["addtext"]]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bi_x_pre(tnt):                                   # noqa: F811
    """
    select by id, prepend text
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], mode="prepend",
                               text=tnt["addtext"])
    assert tnt["addtext"] not in tnt["pre"]
    assert "\n".join([tnt["hdr"], tnt["addtext"], tnt["body"]]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bi_x_rep(tnt):                                   # noqa: F811
    """
    select by id, replace body
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], mode="replace",
                               text=tnt["addtext"])
    assert tnt["addtext"] not in tnt["pre"]
    assert "\n".join([tnt["hdr"], tnt["addtext"]]) in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bi_x_ral(tnt):                                   # noqa: F811
    """
    select by id, replace header and body
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], mode="replace_all",
                               text=tnt["addtext"])
    assert tnt["addtext"] not in tnt["pre"]
    assert tnt["addtext"] in post["note"]
    assert tnt["hdr"] not in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bi_g_app(tnt):                                   # noqa: F811
    """
    select by id, append tags
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], mode="append", text="",
                               tags=comma(tnt["addtags"]))
    assert hashed(tnt["addtags"]) not in tnt["pre"]
    assert "\n".join([tnt["hdr"],
                      tnt["body"],
                      hashed(tnt["addtags"])]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bi_g_pre(tnt):                                   # noqa: F811
    """
    select by id, prepend tags
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], mode="prepend", text="",
                               tags=comma(tnt["addtags"]))
    assert hashed(tnt["addtags"]) not in tnt["pre"]
    assert "\n".join([tnt["hdr"],
                      hashed(tnt["addtags"]),
                      tnt["body"]]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bi_g_rep(tnt):                                   # noqa: F811
    """
    select by id, replace body
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], mode="replace", text="",
                               tags=comma(tnt["addtags"]))
    assert hashed(tnt["addtags"]) not in tnt["pre"]
    assert "\n".join([tnt["hdr"], hashed(tnt["addtags"])]) in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bi_g_ral(tnt):                                   # noqa: F811
    """
    select by id, replace header and body
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], mode="replace_all",
                               text="", tags=comma(tnt["addtags"]))
    assert hashed(tnt["addtags"]) not in tnt["pre"]
    assert hashed(tnt["addtags"]) in post["note"]
    assert tnt["hdr"] not in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bi_xg_app(tnt):                                  # noqa: F811
    """
    select by id, append text and tags

    Note: bear puts an extra newline between the added text and tags, so we
    need an empty string in the list of items expected in post['note'].
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], mode="append",
                               text=tnt["addtext"], tags=comma(tnt["addtags"]))
    for item in [hashed(tnt["addtags"]), tnt["addtext"]]:
        assert item not in tnt["pre"]
    assert "\n".join([tnt["hdr"], tnt["body"], tnt["addtext"], "",
                      hashed(tnt["addtags"])]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bi_xg_pre(tnt):                                  # noqa: F811
    """
    select by id, prepend text and tags

    Note: bear puts an extra newline between the added text and tags, so we
    need an empty string in the list of items expected in post['note'].
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], mode="prepend",
                               text=tnt["addtext"], tags=comma(tnt["addtags"]))
    for item in [hashed(tnt["addtags"]), tnt["addtext"]]:
        assert item not in tnt["pre"]
    assert "\n".join([tnt["hdr"], tnt["addtext"], "",
                      hashed(tnt["addtags"]), tnt["body"]]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bi_xg_rep(tnt):                                  # noqa: F811
    """
    select by id, replace body

    Note: bear puts an extra newline between the added text and tags, so we
    need an empty string in the list of items expected in post['note'].
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], mode="replace",
                               text=tnt["addtext"], tags=comma(tnt["addtags"]))
    for item in [hashed(tnt["addtags"]), tnt["addtext"]]:
        assert item not in tnt["pre"]
    assert "\n".join([tnt["hdr"], tnt["addtext"], "",
                      hashed(tnt["addtags"])]) in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bi_xg_ral(tnt):                                  # noqa: F811
    """
    select by id, replace header and body

    Note: bear puts an extra newline between the added text and tags, so we
    need an empty string in the list of items expected in post['note'].
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], mode="replace_all",
                               text=tnt["addtext"], tags=comma(tnt["addtags"]))
    for item in [hashed(tnt["addtags"]), tnt["addtext"]]:
        assert item not in tnt["pre"]
    assert "\n".join([tnt["addtext"], "",
                      hashed(tnt["addtags"])]) in post["note"]
    assert tnt["hdr"] not in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bit_x_app(tnt):                                  # noqa: F811
    """
    select by id/title, append text
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], title=tnt["title"],
                               mode="append", text=tnt["addtext"])
    assert tnt["addtext"] not in tnt["pre"]
    assert "\n".join([tnt["hdr"], tnt["body"], tnt["addtext"]]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bit_x_pre(tnt):                                  # noqa: F811
    """
    select by id/title, prepend text
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], title=tnt["title"],
                               mode="prepend", text=tnt["addtext"])
    assert tnt["addtext"] not in tnt["pre"]
    assert nljoin(tnt["hdr"], tnt["addtext"], tnt["body"]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bit_x_rep(tnt):                                  # noqa: F811
    """
    select by id/title, replace body
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], title=tnt["title"],
                               mode="replace", text=tnt["addtext"])
    assert tnt["addtext"] not in tnt["pre"]
    assert nljoin(tnt["hdr"], tnt["addtext"]) in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bit_x_ral(tnt):                                  # noqa: F811
    """
    select by id/title, replace header & body
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], title=tnt["title"],
                               mode="replace_all", text=tnt["addtext"])
    assert tnt["addtext"] not in tnt["pre"]
    assert tnt["addtext"] in post["note"]
    assert tnt["hdr"] not in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bit_g_app(tnt):                                  # noqa: F811
    """
    select by id/title, append text
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], title=tnt["title"], mode="append",
                               text="", tags=comma(tnt["addtags"]))
    assert hashed(tnt["addtags"]) not in tnt["pre"]
    assert nljoin(tnt["hdr"], tnt["body"],
                  hashed(tnt["addtags"])) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bit_g_pre(tnt):                                  # noqa: F811
    """
    select by id/title, prepend tags
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], title=tnt["title"], text="",
                               mode="prepend", tags=comma(tnt["addtags"]))
    assert hashed(tnt["addtags"]) not in tnt["pre"]
    assert nljoin(tnt["hdr"],
                  hashed(tnt["addtags"]), tnt["body"]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bit_g_rep(tnt):                                  # noqa: F811
    """
    select by id/title, replace body with tags
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], title=tnt["title"], text="",
                               mode="replace", tags=comma(tnt["addtags"]))
    assert hashed(tnt["addtags"]) not in tnt["pre"]
    assert nljoin(tnt["hdr"], hashed(tnt["addtags"])) in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bit_g_ral(tnt):                                  # noqa: F811
    """
    select by id/title, replace body and header with tags
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], title=tnt["title"], text="",
                               mode="replace_all", tags=comma(tnt["addtags"]))
    assert hashed(tnt["addtags"]) not in tnt["pre"]
    assert hashed(tnt["addtags"]) in post["note"]
    assert tnt["hdr"] not in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bit_xg_app(tnt):                                 # noqa: F811
    """
    select by id/title, append text and tags
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], title=tnt["title"], mode="append",
                               text=tnt["addtext"], tags=comma(tnt["addtags"]))
    for item in [hashed(tnt["addtags"]), tnt["addtext"]]:
        assert item not in tnt["pre"]
    assert nljoin(tnt["hdr"], tnt["body"], tnt["addtext"], "",
                  hashed(tnt["addtags"])) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bit_xg_pre(tnt):                                 # noqa: F811
    """
    select by id/title, prepend text and tags
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], title=tnt["title"],
                               mode="prepend",
                               text=tnt["addtext"], tags=comma(tnt["addtags"]))
    for item in [hashed(tnt["addtags"]), tnt["addtext"]]:
        assert item not in tnt["pre"]
    assert nljoin(tnt["hdr"], tnt["addtext"], "", hashed(tnt["addtags"]),
                  tnt["body"]) in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bit_xg_rep(tnt):                                 # noqa: F811
    """
    select by id/title, replace body with text and tags
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], title=tnt["title"],
                               mode="replace",
                               text=tnt["addtext"], tags=comma(tnt["addtags"]))
    for item in [hashed(tnt["addtags"]), tnt["addtext"]]:
        assert item not in tnt["pre"]
    assert nljoin(tnt["hdr"], tnt["addtext"], "",
                  hashed(tnt["addtags"])) in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_add_text_bit_xg_ral(tnt):                                 # noqa: F811
    """
    select by id/title, replace body and header with text and tags
    """
    pytest.dbgfunc()
    post = tnt["cub"].add_text(id=tnt["id"], title=tnt["title"],
                               text=tnt["addtext"],
                               mode="replace_all", tags=comma(tnt["addtags"]))
    for item in [hashed(tnt["addtags"]), tnt["addtext"]]:
        assert item not in tnt["pre"]
    assert nljoin(tnt["addtext"], "", hashed(tnt["addtags"])) in post["note"]
    assert tnt["hdr"] not in post["note"]
    assert tnt["body"] not in post["note"]


# -----------------------------------------------------------------------------
def test_archive(tnt):                                             # noqa: F811
    """
    Test bear.archive(). If a note has been archived, search won't find it but
    it can still be opened by id with open_note().
    """
    pytest.dbgfunc()
    found = tnt["cub"].search(term=tnt["title"])
    assert found

    result = tnt["cub"].archive(id=tnt['id'])
    assert result == {}

    found = tnt["cub"].search(term=tnt["title"])
    assert found == []

    foo = tnt["cub"].open_note(id=tnt["id"])
    assert foo


# -----------------------------------------------------------------------------
@pytest.mark.parametrize("title, text, tags, ts", [
    pytest.param(beartest_title(), None, None, None, id="001"),
    pytest.param(None, bt_text, None, "yes", id="002"),
    pytest.param(None, None, bt_tags, "no", id="003"),
    pytest.param(None, bt_text, bt_tags, None, id="004"),
    pytest.param(beartest_title(), None, bt_tags, "no", id="005"),
    pytest.param(beartest_title(), bt_text, None, "no", id="006"),
    pytest.param(beartest_title(), bt_text, bt_tags, "yes", id="007"),
    ])
def test_create_tttp(title, text, tags, ts):
    """
    Test the create function with different possible arg combinations
    """
    pytest.dbgfunc()
    cub = Bear()
    kw = {}
    if title:
        kw['title'] = title
    if text:
        kw['text'] = text
    if tags:
        kw['tags'] = tags
    if ts:
        kw['timestamp'] = ts
    note = cub.create(**kw)
    if not note:
        pytest.fail("create returned empty result")
    cub.trash(id=note['identifier'])


# -----------------------------------------------------------------------------
def test_idemp_add_f(tnt):                                         # noqa: F811
    """
    Call idemp_add to add a tag that is present in the note. It should not
    change the note and should return False
    """
    result = tnt["cub"].idemp_add(id=tnt["id"], tag="tmpnote")
    post = tnt["cub"].open_note(id=tnt["id"])
    assert result is False
    assert post["note"] == tnt["pre"]


# -----------------------------------------------------------------------------
def test_idemp_add_t(tnt):                                         # noqa: F811
    """
    Call idemp_add to add a tag that is not present in the note. It should add
    the tag and return True
    """
    result = tnt["cub"].idemp_add(id=tnt["id"], tag="newtag")
    post = tnt["cub"].open_note(id=tnt["id"])
    assert result is True
    assert post["note"] == nljoin(tnt["pre"], "#newtag")


# -----------------------------------------------------------------------------
def tzst_create_file_only(tmpdir):
    """
    create a note with just a file (filename required).

    Creating a note with just a file and no title or text fails on the note
    being empty. After creating the note as here, there's no evidence of the
    file in the note.

    Aha! I was overwriting the file content with the file name. Let's try it
    again...

    Well, when I pass both file and filename, with the file content base64
    encoded, what I get is 'File not in a valid base64 form'. It's not clear
    what the problem is. Guess I'll need to reach out to bear again.
    """
    pytest.dbgfunc()
    cub = Bear()
    testfile = tmpdir.join("bear-test-data")
    # data = "".join(["This is a file for testing bear\n",
    #                 "It contains a couple of lines\n",
    #                 "and is going to be inserted into a bear note\n"])
    data = "A"
    testfile.write(data)
    frob = base64.b64encode(data.encode())
    note = cub.create(title=beartest_title(),
                      file=frob,
                      filename=testfile.strpath)
    if not note:
        pytest.fail("create returned empty result")
    cub.trash(id=note['identifier'])


# -----------------------------------------------------------------------------
def test_has_tag(tnt):                                             # noqa: F811
    """
    Test for bear.has_tag(). Use fixture tnt.
    """
    pytest.dbgfunc()
    assert tnt["cub"].has_tag(tnt["id"], "testing")
    assert not tnt["cub"].has_tag(tnt["id"], "newtag2")


# -----------------------------------------------------------------------------
def test_open_note_id_fail(tnt):                                   # noqa: F811
    """
    Test for bear.open_note()
    """
    pytest.dbgfunc()
    with pytest.raises(Bearror) as err:
        tnt["cub"].open_note(id=tnt["id"] + "xxx")
    assert "The note could not be found" in str(err)


# -----------------------------------------------------------------------------
def test_open_note_id_succ(tnt):                                   # noqa: F811
    """
    Test for bear.open_note()
    """
    pytest.dbgfunc()
    by_id = tnt["cub"].open_note(id=tnt["id"])
    assert by_id['title'] == tnt['title']
    assert by_id['identifier'] == tnt['id']


# -----------------------------------------------------------------------------
def test_open_note_title_fail(tnt):                                # noqa: F811
    """
    Test for bear.open_note()
    """
    pytest.dbgfunc()
    with pytest.raises(Bearror) as err:
        tnt["cub"].open_note(title=tnt["title"] + "foobar")
    assert "The note could not be found" in str(err)


# -----------------------------------------------------------------------------
def test_open_note_title_succ(tnt):                                # noqa: F811
    """
    Test for bear.open_note()
    """
    pytest.dbgfunc()
    by_title = tnt["cub"].open_note(title=tnt["title"])
    assert by_title['title'] == tnt['title']


# -----------------------------------------------------------------------------
def test_open_tag_fail():
    """
    Test for bear.open_tag(). Use fixture tnt.
    """
    pytest.dbgfunc()
    cub = Bear()
    with pytest.raises(Bearror) as err:
        cub.open_tag(name="no such tag")
    assert "Tag 'no such tag' was not found" in str(err)


# -----------------------------------------------------------------------------
def test_open_tag_succ(tnt):                                       # noqa: F811
    """
    Test for bear.open_tag().

    Note: bear.open_tag() retrieves notes in Archive and Trash but gives no
    indication which notes are which. The argument 'exclude_trashed', which
    works for open-note, does not work for open-tag().
    """
    pytest.dbgfunc()
    notes = tnt["cub"].open_tag(name="testing")
    assert notes


# -----------------------------------------------------------------------------
def test_trash(tnt):                                               # noqa: F811
    """
    Test bear.trash()
    """
    pytest.dbgfunc()
    tnt["cub"].trash(id=tnt["id"])

    found = tnt["cub"].search(term=tnt["title"])
    assert found == []

    note = tnt["cub"].open_note(id=tnt["id"], exclude_trashed="no")
    assert note["is_trashed"] == "yes"


# -----------------------------------------------------------------------------
def hashed(tag_l):
    """
    Given a list of tag names, return a space separated list of hashed tags
    (i.e., given ['foo', 'bar', 'funk'], return the string '#foo #bar #funk')
    """
    return " ".join(["#{}".format(_) for _ in tag_l])


# -----------------------------------------------------------------------------
def nljoin(*args):
    """
    Join the elements of *args* with '\n' as a separator
    """
    return "\n".join(args)


# -----------------------------------------------------------------------------
def randword(wlen):
    """
    Generate a random 'word' of length *wlen*
    """
    return ''.join([random.choice(string.ascii_lowercase)
                    for w in range(wlen)])


# -----------------------------------------------------------------------------
def randtext(length):
    """
    Generate *length* bytes of random text and return the string
    """
    sep = rval = ""
    while len(rval) < length:
        rval += sep + randword(random.randrange(1, 15))
        sep = " "
    return rval
