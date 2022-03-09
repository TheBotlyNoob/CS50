from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

import random as random_

from . import util


@require_http_methods(["GET"])
def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


@require_http_methods(["GET"])
def entry(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(
            request,
            "encyclopedia/entry.html",
            {"title": title, "entry": util.parse_markdown(entry).replace("\n", "<br>")},
        )
    else:
        return util.error(request, "Entry not found.")


@require_http_methods(["GET"])
def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()

    if query.lower() in [entry.lower() for entry in entries]:
        return redirect("entry", title=query)
    else:
        return render(
            request,
            "encyclopedia/search.html",
            {
                "results": [
                    entry for entry in entries if query.lower() in entry.lower()
                ],
                "query": query,
            },
        )


@require_http_methods(["GET"])
def random(request):
    entries = util.list_entries()

    return redirect("entry", title=random_.choice(entries))


@require_http_methods(["POST", "GET"])
def edit(request, title):
    entry = util.get_entry(title)

    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            util.save_entry(title, content)
            return redirect("entry", title=title)

    if entry:
        return render(
            request, "encyclopedia/edit.html", {"title": title, "entry": entry}
        )
    else:
        return util.error(request, "Entry not found.")


@require_http_methods(["POST", "GET"])
def new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if util.get_entry(title):
            return util.error(request, "Entry already exists.")

        if title and content:
            util.save_entry(title, content)

            return redirect("entry", title=title)
        else:
            return util.error(request, "Please enter both title and content.")
    else:
        return render(request, "encyclopedia/new.html")
