from django.shortcuts import redirect, render

from markdown2 import markdown

import random as random_

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(
            request,
            "encyclopedia/entry.html",
            {"title": title, "entry": markdown(entry).replace("\n", "<br>")},
        )
    else:
        return util.error(request, "Entry not found.")


def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()

    if query in entries:
        return redirect("entry", title=query)
    else:
        return render(
            request,
            "encyclopedia/search.html",
            {"results": [entry for entry in entries if query in entry], "query": query},
        )


def random(request):
    entries = util.list_entries()

    return redirect("entry", title=random_.choice(entries))


def edit(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(
            request, "encyclopedia/edit.html", {"title": title, "entry": entry}
        )
    else:
        return util.error(request, "Entry not found.")


def new(request):
    return render(request, "encyclopedia/new.html")
