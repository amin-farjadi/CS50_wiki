from django.shortcuts import render
from . import util
import markdown
from django import forms
import re


def index(request, entries = util.list_entries()):
    hrefs = [f"wiki/{entry}" for entry in entries]
    entries_info = zip(entries, hrefs)
    return render(request, "encyclopedia/index.html", {
        "entries_info": entries_info,
    })

def title(request, title):
    
    # Retrieve the markdown format of the title
    md = util.get_entry(title)
    if not md:
        return render(request, "encyclopedia/error.html", {"msg": "Title not found"})

    entries = markdown.markdown(md)
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "entries": entries,
        })

def search(request):
    if request.method == "GET":
        return index(request)

    search = []
    form = request.POST
    search = form["search"]
    entries = util.list_entries()
    found = []

    # searched title is in wiki
    r = re.compile(f"{search}", re.IGNORECASE)
    found = list(filter(r.match, entries))
    if found:
        return title(request, title=found[0])

    # searched title partially matched entries
    r = re.compile(rf".*{search}.*", re.IGNORECASE)
    found = list(filter(r.match, entries))
    if found:
        return index(request, entries=found)

    return render(request, "encyclopedia/error.html", {"msg": "Title not found"})