from django import forms
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.files.storage import default_storage
import random

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

def entry(request, entry):
	markdown = util.get_entry(entry)
	if markdown:
		html = markdown2.markdown(markdown)
		return render(request, 'encyclopedia/entry.html', {
			"entry": entry,
			"html": html
		})
	elif markdown is None:
		return render(request, 'encyclopedia/error.html', {
			'error': "This page doesn't exist"
		})

class NewPageForm(forms.Form):
    title_form = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder': 'Enter Title'}))
    body_form = forms.CharField(label="Body", widget=forms.Textarea(attrs={
        'placeholder': 'Enter Markdown', 
        "style": "height: auto; width: 75%;"
        }))

def newpage(request):
    if request.method == "POST":
        new_form = NewPageForm(request.POST)
        if new_form.is_valid():
            title_new = new_form.cleaned_data["title_form"]
            body_new = new_form.cleaned_data["body_form"]
            if title_new not in util.list_entries():
                util.save_entry(title_new, body_new)
                return HttpResponseRedirect(f"wiki/{title_new}")
            else:
                return render(request, "encyclopedia/error.html", {
                    "error": "This page already exists!"
                })
    return render(request, "encyclopedia/newpage.html", {
        "new_form": NewPageForm()
    })

class EditPageForm(forms.Form):
    edit_body_form = forms.CharField(widget=forms.Textarea(attrs={
        "style": "height: auto; width: 75%;"
        }))

def edit(request, title_edit):
    if request.method == "POST":
        edit_form = EditPageForm(request.POST)
        if edit_form.is_valid():
            body_edit = edit_form.cleaned_data["edit_body_form"]
            util.save_entry(title_edit, body_edit)
            return redirect(entry, title_edit)
        else:
            return render(request, "encyclopedia/error.html", {
                "error": "Oops!"
            })
    elif request.method == "GET":
        content = util.get_entry(title_edit)
        edit_form = EditPageForm(initial={'edit_body_form': content})
        return render(request, "encyclopedia/edit.html", {
            "title_edit": title_edit,
            "edit_form": edit_form
    })

def randompage(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect(entry, random_entry)