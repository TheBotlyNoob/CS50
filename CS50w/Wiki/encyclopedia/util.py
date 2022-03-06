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
    def headers(m: re.Match):
        header_tag = f"h{len(m.group(1))}"

        return f"<{header_tag}>{m.group(2)}</{header_tag}>"

    # parse headers
    s = re.sub(r"^([#]{1,6})[ ](.*)", headers, s, 0, re.MULTILINE)

    # parse links
    s = re.sub(r"\[(.*?)\]\((.*?)\)",
               lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)

    # parse bold face
    s = re.sub(r"\*\*(.*?)\*\*", lambda m: f"<strong>{m.group(1)}</strong>", s)

    # parse unordered lists
    s = re.sub(r"^[ ]*?\-  (.*)",
               lambda m: f"<ul><li>{m.group(1)}</li></ul>", s, 0, re.MULTILINE)

    print(s)

    return s
