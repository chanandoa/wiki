from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.files.storage import default_storage

import markdown2

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
                            return HttpResponseRedirect(f"wiki/{q}")
                        elif results is None:
                            entries = util.list_entries()
                            entries = [i for i in entries if i.lower().find(q.lower()) != -1]
                            return render(request, "encyclopedia/search.html", {
                                "entries": entries
                            })

def newpage(request):
    return render(request, "encylopedia/newpage.html", {})

def entry(request, entry):
	content = util.get_entry(entry)
	if content:
		html = markdown2.markdown(content)
		return render(request, 'encyclopedia/entry.html', {
			'entry': entry,
			'html': html
		})
	elif content is None:
		return render(request, 'encyclopedia/error.html', {
			'error': "This page doesn't exist"
		})