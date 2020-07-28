from django.shortcuts import render
from django.http import HttpResponseRedirect

from markdown2 import Markdown

from . import util


def index(request):
                q = request.GET.get('q')
                if q is None:
                        return render(request, "encyclopedia/index.html", {
                        "entries": util.list_entries()
                    })
                elif q is not None:
                        results = util.get_entry(q)
                        if results:
                            return HttpResponseRedirect(f'wiki/{q}')
                        elif results is None:
                            entries = util.list_entries()
                            entries = [i for i in entries if i.lower().find(q.lower()) != -1]
                            return render(request, 'encyclopedia/search.html', {
                                'entries': entries
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
