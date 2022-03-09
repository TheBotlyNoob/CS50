import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render


def list_entries() -> list:
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(
        sorted(
            re.sub(r"\.md$", "", filename)
            for filename in filenames
            if filename.endswith(".md")
        )
    )


def save_entry(title: str, content: str) -> None:
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title: str) -> str | None:
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def error(request, message):
    "Render message as an apology to user."

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """

        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "'"),
        ]:
            s = s.replace(old, new)
        return s

    return render(request, "encyclopedia/error.html", {"message": escape(message)})


def parse_markdown(s: str) -> str:
    """
    Converts a Markdown string into HTML.
    """

    # parse bold face
    s = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", s)

    # parse headings
    s = re.sub(
        r"^(#{1,6}) (.*)",
        lambda m: rf"<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>",
        s,
        flags=re.MULTILINE,
    )

    # parse links
    s = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', s)

    # parse unordered lists
    s = re.sub(r"^[ ]*?-[ ]*(.*)", r"<li>\1</li>", s, flags=re.MULTILINE)

    # very sorry about this, but I could't figure out how to add the <ul> tag before the groups of lists.
    s = "<ul>" + s + "</ul>"

    return s
