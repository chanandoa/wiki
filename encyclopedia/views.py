from django.shortcuts import render

from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show_page(request, entry):

    markymark = Markdown()

    try:
        html = markymark.convert(util.get_entry(entry))
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "html": html
        })
    except TypeError:
        return render(request, "encyclopedia/error.html", {
            "error": f"{entry} doesn't exist!"
        })
